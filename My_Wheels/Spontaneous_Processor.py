# -*- coding: utf-8 -*-
"""
Created on Fri May 21 15:05:52 2021

@author: ZR
"""
import OS_Tools_Kit as ot
import Filters
import pandas as pd
import numpy as np
import cv2
from sklearn import decomposition
import seaborn as sns
import matplotlib.pyplot as plt
import Graph_Operation_Kit as gt
from scipy import stats
import Statistic_Tools as st
import random


class Spontaneous_Processor(object):
    
    name = 'Spontaneous_Processor'
    
    def __init__(self,day_folder,spon_run = 'Run001',fps = 1.301,passed_band = (0.05,0.5)):
        fp = fps/2
        if passed_band[0] != False:
            HP_par = passed_band[0]/fp
        else:
            HP_par = False
        if passed_band[1] != False:
            LP_par = passed_band[1]/fp
        else:
            LP_par = False
        self.save_folder = day_folder+r'\_All_Results\Spon_Analyze'
        ot.mkdir(self.save_folder)
        self.base_graph = cv2.imread(day_folder+r'\Global_Average.tif',-1)
        self.fps = fps
        cell_file_name = ot.Get_File_Name(day_folder,'.ac')[0]
        cell_dic = ot.Load_Variable(cell_file_name)
        all_cell_name = list(cell_dic.keys())
        spon_train_F = {}
        spon_train_dF = {}
        self.all_cell_info = {}
        for i in range(len(all_cell_name)):
            tc = cell_dic[all_cell_name[i]]
            self.all_cell_info[all_cell_name[i]] = tc['Cell_Info']
            if tc['In_Run'][spon_run]:
                c_name = tc['Name']
                c_train = tc[spon_run]['F_train']
                # do filter
                filted_c_train = Filters.Signal_Filter(c_train,filter_para = (HP_par,LP_par))
                spon_train_F[c_name] = filted_c_train
                average_F = filted_c_train.mean()
                c_dF_series = (filted_c_train-average_F)/average_F
                c_dF_series = np.clip(c_dF_series,c_dF_series.mean()-c_dF_series.std()*3,c_dF_series.mean()+c_dF_series.std()*3)
                spon_train_dF[c_name] = c_dF_series
        self.Spon_Data_Frame_Raw = pd.DataFrame(spon_train_F).T
        self.Spon_Data_Frame_centered = pd.DataFrame(spon_train_dF).T
        self.spon_cellname = list(self.Spon_Data_Frame_centered.index)
        self.frame_num = self.Spon_Data_Frame_centered.shape[1]
        
        del cell_dic
    
    def Series_Select(self,start_time,end_time,mode = 'processed'):
        if mode == 'processed':
            temp_series = self.Spon_Data_Frame_centered
        elif mode == 'raw':
            temp_series = self.Spon_Data_Frame_Raw
        start_frame = round(start_time*self.fps)
        end_frame = round(end_time*self.fps)
        if end_frame > (self.frame_num-1):
            end_frame = self.frame_num-1
            print('Index exceed, Last Frame: '+str(end_frame))
        selected_series = temp_series.iloc[:,start_frame:end_frame]
        return selected_series
        
    def Do_PCA(self,start_time = 0,end_time = 9999,plot = True,mode = 'processed'):
        '''
        Do PCA Analyze for spon series of given time.

        Parameters
        ----------
        start_time : int, optional
            Second of series ON. The default is 0.
        end_time : TYPE, optional
            Second of series OFF. The default is 9999.
        mode : 'processed' or 'raw', optional
            Which mode we use to plot PCA on. The default is 'processed'.

        Returns
        -------
        PCA_Dic : Dic
            Dictionary of PCA information.

        '''
        print('Do PCA for spontaneous cells')
        PCA_Dic = {}
        data_use = self.Series_Select(start_time, end_time,mode)
        data_for_pca = np.array(data_use).T
        pca = decomposition.PCA()
        pca.fit(data_for_pca)
        
        PCA_Dic['All_Components'] = pca.components_
        PCA_Dic['Variance_Ratio'] = pca.explained_variance_ratio_ 
        PCA_Dic['Variance'] = pca.explained_variance_
        PCA_Dic['Cell_Name_List'] = self.spon_cellname
        # plot ROC curve of PCA results.
        accumulated_ratio = np.zeros(len(PCA_Dic['Variance_Ratio']),dtype = 'f8')
        accumulated_variance = np.zeros(len(PCA_Dic['Variance']),dtype = 'f8')
        random_ratio = np.zeros(len(PCA_Dic['Variance_Ratio']),dtype = 'f8')
        for i in range(len(accumulated_ratio)-1):
            accumulated_ratio[i+1] = accumulated_ratio[i]+PCA_Dic['Variance_Ratio'][i]
            accumulated_variance[i+1] = accumulated_variance[i]+PCA_Dic['Variance'][i]
            random_ratio[i+1] = (i+1)/len(accumulated_ratio)
        PCA_Dic['Accumulated_Variance_Ratio'] = accumulated_ratio
        PCA_Dic['Accumulated_Variance'] = accumulated_variance
        
        if plot == True:
            pca_save_folder = self.save_folder+r'\PC_Graphs'
            ot.mkdir(pca_save_folder)
            for i in range(len(pca.components_[:,0])):
                visual_data,folded_map,gray_graph = self.Component_Visualize(PCA_Dic['All_Components'][i,:])
                fig = plt.figure(figsize = (15,15))
                plt.title('PC'+str(i+1),fontsize=36)
                fig = sns.heatmap(visual_data,square=True,yticklabels=False,xticklabels=False,center = 0)
                fig.figure.savefig(pca_save_folder+'\PC'+str(i+1)+'.png')
                plt.clf()
                cv2.imwrite(pca_save_folder+'\PC'+str(i+1)+'_Folded.tif',folded_map)
                cv2.imwrite(pca_save_folder+'\PC'+str(i+1)+'_Gray.jpg',gray_graph)
            
            fig,ax = plt.subplots(figsize = (8,6))
            plt.title('Accumulated Variance')
            plt.plot(range(len(accumulated_ratio)),accumulated_ratio)
            plt.plot(range(len(accumulated_ratio)),random_ratio)
            plt.savefig(pca_save_folder+'\_ROC.png')
            ot.Save_Variable(pca_save_folder, 'PCA_Dic', PCA_Dic)
        return PCA_Dic
    
    
    def Component_Visualize(self,input_component):# input component shall be a cell combination.
        
        visualize_data = np.zeros(shape = self.base_graph.shape,dtype = 'f8')
        cell_list = self.spon_cellname
        if len(input_component) != len(cell_list):
            raise IOError('Cell number mistach!')
        for i in range(len(cell_list)):
            c_cell = cell_list[i]
            c_weight = input_component[i]
            c_info = self.all_cell_info[c_cell]
            y_list,x_list = c_info.coords[:,0],c_info.coords[:,1]
            visualize_data[y_list,x_list] = c_weight
        # keep zero stable, and normalize.
        norm_visualize_graph = visualize_data/abs(visualize_data).max()
        posi_parts = norm_visualize_graph*(norm_visualize_graph>0)
        nega_parts = norm_visualize_graph*(norm_visualize_graph<0)
        # Then get folded graph.
        folded_map = cv2.cvtColor(self.base_graph,cv2.COLOR_GRAY2RGB)*0.7
        folded_map[:,:,0] += (-nega_parts)*65535
        folded_map[:,:,2] += posi_parts*65535
        folded_map = np.clip(folded_map,0,65535).astype('u2')
        gray_graph = (norm_visualize_graph*127+127).astype('u1')
        
        return visualize_data,folded_map,gray_graph
        
    def Pairwise_Correlation_Core(self,name_lists,start_time,end_time,
                               method = 'spearman',mode = 'processed'):
        '''
        Calculate pair wise correlation of given cells

        Parameters
        ----------
        name_lists : (list)
            List of cell name we used to calculate correlation.
        start_time : (int)
            Time of series start.
        end_time : (int)
            Time of series end.
        method : 'spearman' or 'pearson', optional
            Which correlation we use. The default is 'spearman'.
        mode : 'processed' or 'raw', optional
            Data type of series. The default is 'processed'.

        Returns
        -------
        cross_correlation_data : (list)
            All pair wise correlations.

        '''
        pairwise_correlation_data = []
        cell_num = len(name_lists)
        data_for_cc = self.Series_Select(start_time,end_time,mode).loc[name_lists]
        data_matrix = np.array(data_for_cc)
        for i in range(cell_num):
            A_series = data_matrix[i,:]
            for j in range(i+1,cell_num):
                B_series = data_matrix[j,:]
                if method == 'spearman':
                    pairwise_correlation_data.append(stats.spearmanr(A_series,B_series)[0])
                elif method == 'pearson':
                    pairwise_correlation_data.append(stats.pearsonr(A_series,B_series)[0])
        return pairwise_correlation_data
    
    def Pairwise_Correlation_Plot(self,name_lists,start_time,end_time,label,cor_range = (-0.2,0.2),
                               method = 'spearman',mode = 'processed'):
        cell_num = len(name_lists)
        # Do have cell test
        new_name_list = []
        for i in range(cell_num):
            if name_lists[i] in self.spon_cellname:
                new_name_list.append(name_lists[i])
        real_cell_num = len(new_name_list)
        print('Real Cell Num:'+str(real_cell_num))
        real_data = self.Pairwise_Correlation_Core(new_name_list, start_time, end_time,method,mode)
        rand_cells = random.sample(self.spon_cellname, real_cell_num)
        rand_data = self.Pairwise_Correlation_Core(rand_cells, start_time, end_time,method,mode)
        
        fig,ax = plt.subplots(figsize = (12,8))
        bins = np.linspace(cor_range[0], cor_range[1], 200)
        ax.hist(rand_data,bins,label ='Random',alpha = 0.8)
        ax.hist(real_data,bins,label = label,alpha = 0.8)
        ax.legend(prop={'size': 20})
        t,p,_ = st.T_Test_Ind(real_data, rand_data)
        ax.annotate('t ='+str(round(t,3)),xycoords = 'axes fraction',xy = (0.9,0.7))
        ax.annotate('p ='+str(round(p,7)),xycoords = 'axes fraction',xy = (0.9,0.65))
        fig.savefig(self.save_folder+r'\Pair_Cor_'+label+'.png',dpi=180)
        
        return t,p

    def Seed_Point_Correlation_Map(self,seed_point,start_time,end_time,
                                   seed_brightnes = 0.5,method = 'spearman',mode = 'processed'):
        
        correlation_info = {}
        color_map = np.zeros(self.base_graph.shape+(3,),dtype = 'f8')
        heat_data = np.zeros(self.base_graph.shape,dtype = 'f8')
        data_for_seed_point = self.Series_Select(start_time,end_time,mode)
        base_series = data_for_seed_point.loc[seed_point]
        for i in range(len(self.spon_cellname)):
            c_name = self.spon_cellname[i]
            targ_series = data_for_seed_point.loc[c_name]
            if method == 'spearman':
                c_corr,_ = stats.spearmanr(base_series,targ_series)
            elif method == 'pearson':
                c_corr,_ = stats.pearsonr(base_series,targ_series)
            correlation_info[c_name] = c_corr
                
            # Till now, we get correlation to seed point, then do visualization.
            c_cell_info = self.all_cell_info[c_name]
            y_list,x_list = c_cell_info.coords[:,0],c_cell_info.coords[:,1]
            if c_name == seed_point:
                color_map[y_list,x_list,1] = 255
                heat_data[y_list,x_list] = seed_brightnes
            else:
                heat_data[y_list,x_list] = c_corr
                if c_corr>0:
                    color_map[y_list,x_list,2] = c_corr
                else:
                    color_map[y_list,x_list,0] = c_corr
        # Last,normalize all graph and plot heat map.
        fig = plt.figure(figsize = (15,15))
        plt.title('Correlation to '+seed_point,fontsize=36)
        fig = sns.heatmap(heat_data,square=True,yticklabels=False,xticklabels=False,center = 0)
        fig.figure.savefig(self.save_folder+'\Correlation to '+seed_point+'.png')
        plt.clf()
        normalize_para = max(abs(color_map[:,:,0]).max(),abs(color_map[:,:,2].max()))
        color_map[:,:,0] = color_map[:,:,0]*(-255)/normalize_para
        color_map[:,:,2] = color_map[:,:,2]*255/normalize_para
        color_map = color_map.astype('u1')
        cv2.imwrite(self.save_folder+'\Correlation to '+seed_point+'_Color.jpg',color_map)
        return heat_data,color_map
            
def Cross_Run_Pair_Correlation(day_folder,name_lists,run_A,run_B,
                               start_time_A,end_time_A,start_time_B,end_time_B,label_A,label_B,
                               fps = 1.301,cor_range = (-0.2,0.6),method = 'spearman',mode = 'processed'):
    
    # First get A and B series seperately
    save_folder = day_folder+r'\_All_Results\Spon_Analyze'
    A_SP = Spontaneous_Processor(day_folder,spon_run = run_A)
    B_SP = Spontaneous_Processor(day_folder,spon_run = run_B)
    A_sponcell = A_SP.spon_cellname
    B_sponcell = B_SP.spon_cellname
    used_name_list = []
    for i in range(len(name_lists)):
        cc = name_lists[i]
        if (cc in A_sponcell) and (cc in B_sponcell):
            used_name_list.append(cc)
    real_cellnum = len(used_name_list)
    print('Really used cell num: '+str(real_cellnum))
    A_series = A_SP.Series_Select(start_time_A, end_time_A).loc[used_name_list]
    B_series = B_SP.Series_Select(start_time_B, end_time_B).loc[used_name_list]
    series_length = min(A_series.shape[1],B_series.shape[1])
    A_series = A_series.iloc[:,0:series_length]
    B_series = B_series.iloc[:,0:series_length]
    # Second we calculate pairwise correlation of A and B.
    A_pair_corr = []
    B_pair_corr = []
    A_matrix = np.array(A_series)
    B_matrix = np.array(B_series)
    for i in range(real_cellnum):
        Ai_series = A_matrix[i,:]
        Bi_series = B_matrix[i,:]
        for j in range(i+1,real_cellnum):
            Aj_series = A_matrix[j,:]
            Bj_series = B_matrix[j,:]
            if method == 'spearman':
                A_pair_corr.append(stats.spearmanr(Ai_series,Aj_series)[0])
                B_pair_corr.append(stats.spearmanr(Bi_series,Bj_series)[0])
            elif method == 'pearson':
                A_pair_corr.append(stats.pearsonr(Ai_series,Aj_series)[0])
                B_pair_corr.append(stats.pearsonr(Bi_series,Bj_series)[0])
    # Then plot graphs.
    fig,ax = plt.subplots(figsize = (12,8))
    bins = np.linspace(cor_range[0], cor_range[1], 200)
    ax.hist(A_pair_corr,bins,label = label_A,alpha = 0.8)
    ax.hist(B_pair_corr,bins,label = label_B,alpha = 0.8)
    ax.legend(prop={'size': 20})
    t,p,_ = st.T_Test_Ind(B_pair_corr,A_pair_corr)
    ax.annotate('t ='+str(round(t,3)),xycoords = 'axes fraction',xy = (0.9,0.7))
    ax.annotate('p ='+str(round(p,7)),xycoords = 'axes fraction',xy = (0.9,0.65))
    fig.savefig(save_folder+r'\Cross_Run_Hist.png',dpi=180)
    # Plot joint graph then 
    fig2 = sns.jointplot(x=A_pair_corr, y=B_pair_corr,s = 5,height = 8,xlim = cor_range,ylim = cor_range)
    fig2.set_axis_labels('x', 'y', fontsize=16)
    fig2.ax_joint.set_xlabel(label_A)
    fig2.ax_joint.set_ylabel(label_B)
    fig2.ax_joint.plot([cor_range[0],cor_range[1]],[cor_range[0],cor_range[1]], ls = '--',color = 'gray')
    fig2.savefig(save_folder+r'\Cross_Run_joint.png',dpi=180)
    return A_pair_corr,B_pair_corr
    
        