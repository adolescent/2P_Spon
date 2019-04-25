# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:32:33 2019

@author: ZR
这里操作只是单纯聚类，不对数据进行额外处理。
注意聚类操作需要根据情况进行调整，没有办法一步完成。
"""

import pickle
import functions_cluster as pp
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as clus_h

def read_variable(name):#读取变量用的题头，希望这个可以在后续删掉
    with open(name, 'rb') as file:
        variable = pickle.load(file)
    file.close()
    return variable
#%%
class Cluster():
    
    name = r'Cluster For Spike Trains'#
    
    def __init__(self,spike_train,bins):#初始化变量
        self.spike_train = spike_train
        self.bins = bins
        self.cell_Num,self.Frame_Num = np.shape(self.spike_train)
        
    def bin_spike_data(self):#对结果做bin
        if self.bins ==1:
            self.binned_spike_train = self.spike_train
        else:
            self.binned_spike_train = np.zeros(shape = (self.cell_Num,self.Frame_Num//self.bins))
            for i in range(0,self.Frame_Num//self.bins):
                self.binned_spike_train[:,i] = np.mean(spike_train[:,i*self.bins:(i+1)*self.bins],axis = 1)
                
    def cluster_main(self):#这个是聚类主程序
        self.binned_spike_train = np.transpose(self.binned_spike_train) #转置，每个横行是一个case的不同维度，纵列是不同case
        self.Z = clus_h.linkage(self.binned_spike_train,method = 'ward')#聚类运算,这一步小心内存= =
    def plot_dendrogram(self,p,max_d,annotate_above):
        plt.figure(figsize = (25,10))
        pp.fancy_dendrogram(
            self.Z,
            truncate_mode='lastp',
            p=p, #plot最后多少个节点
            leaf_rotation=90.,
            leaf_font_size=12.,
            show_contracted=True,
            annotate_above=annotate_above,  # 最小标注的距离
            max_d=max_d #水平截止线
        )
        plt.savefig(r'Dendrogram_Node='+str(p)+'.png')
        plt.show()
    def cluster_determination(self,d):#确定最终的截至距离
        
    
    
 #%%   
if __name__ == '__main__':
    start_time = time.time()
    print('Clustering Start...\n')
    spike_train = read_variable('spike_train.pkl')
    cl = Cluster(spike_train,1)
    cl.bin_spike_data()
    cl.cluster_main()
    Z = cl.Z
    cl.plot_dendrogram(500,0,0)