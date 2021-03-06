# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:15:08 2018

@author: LvLab_ZR
之前的操作已经得到了各个细胞的连通区域坐标，接下来可以对Align之后的数据进行spike Train的操作了
这一步操作之后，希望得到一个list，结构是Cell_Reaction(Cell_Index,dR/R of different frames)
由于一些变量未重新声称，这一步骤应该在Step1/Step2之后进行。
dF/F算法是：（对齐之后的细胞亮度之和-目标图片的亮度）/对齐之后的细胞亮度之和

使用的前文变量：
save_folder/aligned_tif_name/graph_after_align
"""

#%% Read in
import cv2
import numpy as np
#save_folder = r'D:\datatemp\180508_L14\Run02_spon\1-002\save_folder_for_py'#这一行最后要改
import pickle
import functions_OD as pp
save_folder = save_folder
fr = open(save_folder+'\\cell_group','rb')
cell_group = pickle.load(fr)
aligned_frame_folder = save_folder+'\Aligned_Frames' #保存对齐过后图片的文件夹
#%% 整个流程由大循环完成，第一层循环是不同的细胞区域
''' 旧代码
import numpy as np
spike_train = np.zeros(shape = (len(cell_group),len(aligned_tif_name)))
for i in range(0,len(cell_group)):
    cell_location = cell_group[i].coords
    x_list = cell_location[:,1] #这个细胞的全部X坐标
    y_list = cell_location[:,0] #这个细胞的全部Y坐标
    cell_area = len(cell_location) #这个细胞占据的pixel大小。
    #之后对每个细胞面积的亮度和与均值作dR/R，观察不同帧下的平均差别
    #%%这里得到这个神经元的基准亮度
    F_base = 0
    for j in range(0,cell_area):
        F_base = F_base+graph_before_align[y_list[j],x_list[j]]
    #%%这一层循环计算得到目标神经元的dF/F
    for j in range(0,len(aligned_tif_name)):
        temp_frame = cv2.imread(aligned_tif_name[j],-1)
        F_temp = 0
        for k in range(0,cell_area):#得到目标神经元亮度
            F_temp = F_temp + temp_frame[y_list[k],x_list[k]]
        dF = (F_temp-F_base)/F_base#这一帧的dF
        spike_train[i,j] = dF'''
#%% 改变循环顺序，提高运行效率。
spike_train = np.zeros(shape = (len(cell_group),len(aligned_tif_name)))
#首先得到基准帧
base_F = np.zeros(shape = len(cell_group))
for i in range(0,len(cell_group)):
    base_F[i] = pp.sum_a_frame(graph_after_align,cell_group[i])
#之后读取每一帧，并对这一帧做一样的运算
for i in range(0,len(aligned_tif_name)):# 减少读取次数，每次将一张图的细胞数目读取完
    current_frame = cv2.imread(aligned_tif_name[i],-1)
    target_F = np.zeros(shape = len(cell_group))
    for j in range(0,len(cell_group)):
        target_F[j] = pp.sum_a_frame(current_frame,cell_group[j])
    dF_per_frame = (target_F-base_F)/base_F
    spike_train[:,i] =dF_per_frame 

#%% 保存变量
fw = open((save_folder+'\\Spike_Train'),'wb')
pickle.dump(spike_train,fw)#保存细胞连通性质的变量。

#%% 绘图，将每个单独cell的spike_train画出来
#调试部分
'''save_folder = (r'D:\datatemp\L63_LL_OI_2P\180810_L63_2P\Run01_V4_L8910_D240_RG_Spon\for_python')
import pickle
import numpy as np
import function_in_2p as pp
fr = open(save_folder+'\\spike_train','rb')
spike_train = pickle.load(fr)'''
#%%
spike_train_folder = save_folder+'\Spike_Trains'
pp.mkdir(spike_train_folder)
import matplotlib.pyplot as plt
cell_Num,frame_Num = np.shape(spike_train)

for i in range(0,cell_Num):
    plt.figure(figsize = (20,3))
    plt.ylim(-0.5,1.5)
    plt.xlim(0,frame_Num*1.06)
    plt.title('Spike_Train of Cell '+str(i))
    plt.plot(spike_train[i,:])
    #接下来标注均值和两倍、三倍标准差的线。
    mean = np.mean(spike_train[i,:])
    std = np.std(spike_train[i,:])
    plt.axhline(y = mean,color = '#d62728')#红色
    plt.annotate('Average', xy = (frame_Num,mean),xytext=(frame_Num*1.03,mean+0.5),arrowprops=dict(facecolor='black',width = 1,shrink = 0.05,headwidth = 5))#标注均值
    plt.axhline(y = mean+std*2,color = '#00ff00')#绿色
    plt.annotate('Means+2std', xy = (frame_Num,std*2),xytext=(frame_Num*1.03,std*2+0.5),arrowprops=dict(facecolor='black',width = 1,shrink = 0.05,headwidth = 5))#标注阈值
    plt.axhline(y = mean+std*3,color = '#66fff2')#水蓝色
    plt.annotate('Means+3std', xy = (frame_Num,std*3),xytext=(frame_Num*1.03,std*3+0.5),arrowprops=dict(facecolor='black',width = 1,shrink = 0.05,headwidth = 5))#标注阈值
    #%接下来计算超过2std和3std的帧数比例
    over2std = str(round(np.sum(spike_train[i,:]>mean+std*2)/frame_Num*100,5))+'%'
    over3std = str(round(np.sum(spike_train[i,:]>mean+std*3)/frame_Num*100,5))+'%'#百分数形式保留五位小数并转换为str
    plt.annotate((over2std+' Over2std,'+over3std+' Over3std'),xy = (frame_Num*0.75,0), xytext=(frame_Num*0.75,1.6))
    plt.savefig(spike_train_folder+'\Cell'+str(i)+'.png')
    #plt.show()
    plt.close('all')
print('Plot Spike Train Done!')
'''plt.figure()
plt.plot()
plt.savefig()
plt.close('all')'''
#%%保存spike_train为mat文件
import scipy.io
scipy.io.savemat(save_folder+r'\Spike_train.mat', mdict={'Spike_Train': spike_train})