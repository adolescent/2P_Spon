# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:43:23 2020

@author: ZR
"""

import os
import My_Wheels.OS_Tools_Kit as OS_Tools
import My_Wheels.Graph_Operation_Kit as Graph_Tools
import numpy as np
import cv2
from My_Wheels.Translation_Align_Function import Translation_Alignment

def Single_Subgraph_Generator(
        all_tif_name,
        A_IDs,B_IDs,
        gaussian_parameter = ((5,5),1.5),
        t_map = True
        ):
    '''
    Generate single subtraction map of 2P data. A-B graph is generated.

    Parameters
    ----------
    all_tif_name : (list or nparray)
        All graph name. Usually aligned tif name.
    A_IDs : (list)
        List of A ID.
    B_IDs : (list)
        List of B ID.
    gaussian_parameter : (turple), optional
        Use False to skip. Gaussian filter used before and after subtraction. The default is ((5,5),1.5).
    t_map : (bool), optional
        Whether t map is generated. The default is True.

    Returns
    -------
    sub_graph : (2D array)
        Subtraction dF/F graph. Origin data, clip and normalize shall be done before plot.
    t_graph : (2D array)
        T test graph.0-1 value normalized array. If t_map == False, this will be None.
    F_info_Dics : (Dic)
        Information dictionary. Including origin F & dF/F information of input graph.

    '''
    F_info_Dics = {}
    all_tif_name = np.array(all_tif_name)# Change into nparray to slice.
    A_Set_Graph_names = all_tif_name[A_IDs]
    B_Set_Graph_names = all_tif_name[B_IDs]
    # Calculate sub graph.
    F_info_Dics['Graph_Shape'] = np.shape(cv2.imread(all_tif_name[0],-1))
    F_info_Dics['Origin_Data_Type'] = str((cv2.imread(all_tif_name[0],-1)).dtype)
    F_info_Dics['Average_A_Graph'] = Graph_Tools.Average_From_File(A_Set_Graph_names,gaussian_parameter)
    F_info_Dics['Average_B_Graph'] = Graph_Tools.Average_From_File(B_Set_Graph_names,gaussian_parameter)
    F_info_Dics['dF_Map'] = (F_info_Dics['Average_A_Graph'].astype('f8') - F_info_Dics['Average_B_Graph'].astype('f8'))
    F_info_Dics['Average_dF_value'] = abs(F_info_Dics['dF_Map']).mean()# Average dF value.
    F_info_Dics['Average_dF/F_value'] = F_info_Dics['Average_dF_value']/(F_info_Dics['Average_B_Graph'].mean())
    sub_graph = np.nan_to_num(F_info_Dics['dF_Map']/F_info_Dics['Average_B_Graph'].astype('f8'))
    F_info_Dics['dF/F_Graph'] = sub_graph
    
    # Then calculate F value graph.
    if t_map == False:
        F_info_Dics['t_value_map'] = None
        F_info_Dics['p_value_map'] = None
        t_graph = None
    else:
        import random
        sample_size = min(len(A_Set_Graph_names),len(B_Set_Graph_names))
        selected_A_name = np.array(random.sample(list(A_Set_Graph_names), sample_size))
        selected_B_name = np.array(random.sample(list(B_Set_Graph_names), sample_size))
        A_graph_arrays = np.zeros(shape = (F_info_Dics['Graph_Shape']+(sample_size,)),dtype = 'f8')
        B_graph_arrays = np.zeros(shape = (F_info_Dics['Graph_Shape']+(sample_size,)),dtype = 'f8')
    # Then we will fill filtered data into graph.
        # First, we will read in AB graphs together.
        for i in range(sample_size):
            current_a_graph = cv2.imread(selected_A_name[i],-1)
            current_b_graph = cv2.imread(selected_B_name[i],-1)
            if gaussian_parameter != False:
                A_graph_arrays[:,:,i] = cv2.GaussianBlur(current_a_graph, gaussian_parameter[0], gaussian_parameter[1])
                B_graph_arrays[:,:,i] = cv2.GaussianBlur(current_b_graph, gaussian_parameter[0], gaussian_parameter[1])
            else:
                A_graph_arrays[:,:,i] = current_a_graph
                B_graph_arrays[:,:,i] = current_b_graph
        # After that, we calculate t and p value pix by pix.
        t_value_graph = np.zeros(shape = F_info_Dics['Graph_Shape'],dtype = 'f8')
        p_value_graph = np.zeros(shape = F_info_Dics['Graph_Shape'],dtype = 'f8')
        from scipy.stats import ttest_rel
        for i in range(F_info_Dics['Graph_Shape'][0]):
            for j in range(F_info_Dics['Graph_Shape'][1]):
                t_value_graph[i,j],p_value_graph[i,j] = ttest_rel(A_graph_arrays[i,j,:],B_graph_arrays[i,j,:])
        t_graph = t_value_graph
        F_info_Dics['t_graph'] = t_graph
        F_info_Dics['p_value_of_t_test'] = p_value_graph

    return sub_graph,t_graph,F_info_Dics

def Single_Cellgraph_Generator(
        all_tif_name,
        cell_information,
        A_IDs,
        B_IDs,
        gaussian_parameter = ((5,5),1.5),
        ):
    print('Function Not Finished Yet!')
    sub_cell_graph,t_cell_graph,cell_info_dic =0,0,0
    return sub_cell_graph,t_cell_graph,cell_info_dic


def Standard_Stim_Processor(
             data_folder,
             stim_folder,
             sub_dic,
             tuning_graph = True,
             cell_method = 'Default',
             gaussian_parameter = ((5,5),1.5)
             ):
    '''
    Input part of this module. Althought this model can do align, if you want to align all graphs together, prealign is advised.

    Parameters
    ----------
    graph_folder : (str)
        Input graph folder. If graph has been aligned, this will use aligned graph directly. Else this function will align single run.
    stim_folder : (str)
        Folder of stimulus, or aligned stimulus file name. This will be checked later, if is folder, 
    sub_dic : (dic)
        Subtraction ID dictionary. Standard ID can be acquired from My_Wheels.Standard_Parameters.Sub_Graph_Dics. 
    tuning_graph : (bool), optional
        Whether we produce radar map. The default is True.
    cell_method: ('Default' or cell file path)
        If default, use on-off graph, else you need to give the input path.

    gaussian_parameter : (turple)
        This step can be skipped if you input 'False'. Gaussian blur of graph process. Every graph will be filtered before process. The default is((5,5),1.5),meaning kernel of filter is (5,5), std = 1.5. 
    
    Returns
    -------
    None.

    '''
    # Path Cycle.
    work_folder = data_folder+r'\Results'
    OS_Tools.mkdir(work_folder)
    aligned_frame_folder = work_folder+r'\Aligned_Frames'
    OS_Tools.mkdir(aligned_frame_folder)
    
    # Step1, align graphs. If already aligned, just read 
    if not os.listdir(aligned_frame_folder): # if this is a new folder
        print('Aligned data not found. Aligning here..')
        Translation_Alignment([data_folder])
    aligned_all_tif_name = np.array(OS_Tools.Get_File_Name(aligned_frame_folder)) # Use numpy array, this is easier for slice.
        
    # Step2, get stim fram align matrix. If already aligned, just read in aligned dictionary.
    file_detector = len(stim_folder.split('.'))
    if file_detector == 1:# Which means input is a folder
        print('Frame Stim not Aligned, aligning here...')
        from My_Wheels.Stim_Frame_Align import Stim_Frame_Align
        _,Frame_Stim_Dic = Stim_Frame_Align(stim_folder)
    else: # Input is a file
        Frame_Stim_Dic = OS_Tools.Load_Variable(stim_folder)
        
    # Step3, get cell information 
    if cell_method == 'Default':# meaning we will use On-Off graph to find cell.
        print('Cell information not found. Finding here..')
        off_list = Frame_Stim_Dic[0]
        all_keys = list(Frame_Stim_Dic.keys())
        all_keys.remove(0)
        all_keys.remove(-1)# Remove ISI
        on_list = []
        for i in range(len(all_keys)):
            on_list.extend(Frame_Stim_Dic[all_keys[i]])
            
    else:
        cell_dic = OS_Tools.Load_Variable(cell_method)
        
        
if __name__ == '__main__':
    from My_Wheels.Standard_Parameters.Sub_Graph_Dics import Sub_Dic_Generator
    