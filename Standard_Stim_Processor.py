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
from Cell_Find_From_Graph import Cell_Find_From_Graph
import My_Wheels.Filters as My_Filter

def Single_Subgraph_Generator(
        all_tif_name,
        A_IDs,B_IDs,
        filter_method = 'Gaussian',
        LP_Para = ((5,5),1.5),
        HP_Para = False,
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
    filter_method : (str), optional
        Can be set False to skip. Filter used before and after subtraction. The default is 'Gaussian'.
    LP_Para: (turple),optional
        Can be set False to skip. Low pass filter parameter. The default is ((5,5),1.5).
    HP_Para: (turple),optional
        Can be set False to skip. High pass filter parameter. The default is False.
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
    F_info_Dics['Average_A_Graph'] = Graph_Tools.Average_From_File(A_Set_Graph_names,LP_Para,HP_Para,filter_method)
    F_info_Dics['Average_B_Graph'] = Graph_Tools.Average_From_File(B_Set_Graph_names,LP_Para,HP_Para,filter_method)
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
            if filter_method != False:
                A_graph_arrays[:,:,i] = My_Filter.Filter_2D(current_a_graph,LP_Para,HP_Para,filter_method)
                B_graph_arrays[:,:,i] = My_Filter.Filter_2D(current_b_graph,LP_Para,HP_Para,filter_method)
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
        dF_F_train,
        cell_information,
        clip,
        A_IDs,
        B_IDs,
        ):
    graph_shape = np.shape(cell_information[0]._label_image)
    sub_cell_graph = np.zeros(shape = (graph_shape+(3,)),dtype = 'u1')# color graph,BGR.
    t_cell_graph = np.zeros(shape = (graph_shape+(3,)),dtype = 'u1')
    cell_info_dic = {}
    # Calculation first, then we draw graph. Seperate to do norm and align easier.
    cell_Num = len(cell_information)
    cell_dF_F_array = np.zeros(cell_Num,dtype = 'f8')
    cell_t_array = np.zeros(cell_Num,dtype = 'f8')
    cell_p_array = np.zeros(cell_Num,dtype = 'f8')
    for i in range(cell_Num):
        current_cell_spike_train = dF_F_train[i]
        A_dFs = current_cell_spike_train[A_IDs]
        B_dFs = current_cell_spike_train[B_IDs]
        cell_dF_F_array[i] = A_dFs.mean()-B_dFs.mean()
        import random
        from scipy.stats import ttest_rel
        sample_size = min(len(A_dFs),len(B_dFs))
        selected_A = random.sample(list(A_dFs),sample_size)
        selected_B = random.sample(list(B_dFs),sample_size)
        cell_t_array[i],cell_p_array[i] = ttest_rel(selected_A,selected_B)
    cell_info_dic['origin_subcell'] = cell_dF_F_array
    cell_info_dic['max_dF_F'] = np.max(abs(cell_dF_F_array))
    cell_info_dic['origin_t_map'] = cell_t_array
    cell_info_dic['p_map'] = cell_p_array
    # Process t map and sub map. Clip and normalize.
    clipped_cell_dF_F_array = Graph_Tools.EZClip(cell_dF_F_array,clip)
    sig_array = cell_p_array<0.05
    sig_t_array = sig_array*cell_t_array
    clipped_cell_t_array = Graph_Tools.EZClip(sig_t_array,clip)
    normed_cell_dF_F_array = clipped_cell_dF_F_array/np.max(abs(clipped_cell_dF_F_array))
    normed_cell_t_array = clipped_cell_t_array/np.max(abs(clipped_cell_t_array))
    # Finally, we can plot graphs here.
    for i in range(cell_Num):
        current_cell_info = cell_information[i]
        y_list,x_list = current_cell_info.coords[:,0],current_cell_info.coords[:,1]
        if normed_cell_dF_F_array >0:
            sub_cell_graph[y_list,x_list,2] = normed_cell_dF_F_array[i]*255
        else:
            sub_cell_graph[y_list,x_list,0] = abs(normed_cell_dF_F_array[i])*255
        if normed_cell_t_array >0:
            t_cell_graph[y_list,x_list,2] = normed_cell_t_array[i]*255
        else:
            t_cell_graph[y_list,x_list,0] = abs(normed_cell_t_array[i])*255
    
    return sub_cell_graph,t_cell_graph,cell_info_dic


def Standard_Stim_Processor(
             data_folder,
             stim_folder,
             sub_dic,
             show_clip = 3,
             tuning_graph = False,
             cell_method = 'Default',
             filter_method = 'Gaussian',
             LP_Para = ((5,5),1.5),
             HP_Para = False,
             spike_train_path = 'Default',
             spike_train_filter_para = (False,False),
             spike_train_filter_method = False
             ):
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
        all_keys.remove('Original_Stim_Train')
        on_list = []
        for i in range(len(all_keys)):
            on_list.extend(Frame_Stim_Dic[all_keys[i]])
        on_off_graph,_,_ = Single_Subgraph_Generator(aligned_all_tif_name, on_list, off_list,filter_method,LP_Para,HP_Para,t_map = False)
        cell_dic = Cell_Find_From_Graph(on_off_graph,find_thres = 2)
    else:
        cell_dic = OS_Tools.Load_Variable(cell_method)
        
    # Step4, calculate spike_train.
    if spike_train_path != 'Default':
        dF_F_train = OS_Tools.Load_Variable(spike_train_path)
    else:# meaning we need to calculate spike train from the very begining.
        from My_Wheels.Spike_Train_Generator import Spike_Train_Generator
        _,dF_F_train = Spike_Train_Generator(aligned_all_tif_name,cell_dic['All_Cell_Information'],Base_F_type = 'nearest_0',stim_train = Frame_Stim_Dic['Original_Stim_Train'],LP_Para = LP_Para,HP_Para = HP_Para,filter_method = filter_method)
    #Step5, filt spike trains.
    if spike_train_filter_method != False: # Meaning we need to do train filter.
        for i in range(len(dF_F_train)):
            dF_F_train[i] = My_Filter.Signal_Filter(dF_F_train,spike_train_filter_method,spike_train_filter_para)
    # Step6, get each frame graph and cell graph.
    all_graph_keys = list(sub_dic.keys())
    for i in range(len(sub_dic)):
        output_folder = work_folder+r'\Subtraction_Graphs'
        current_key = all_graph_keys[i]
        current_sub_list = sub_dic[current_key]
        A_conds = current_sub_list[0]# condition of A graph
        B_conds = current_sub_list[1]# condition of B graph
        A_IDs = []
        B_IDs = []
        for i in range(len(A_conds)):
            A_IDs.extend(Frame_Stim_Dic[A_conds[i]])
        for i in range(len(B_conds)):
            B_IDs.extend(Frame_Stim_Dic[B_conds[i]])
        # Get frame maps.
        current_sub_graph,current_t_graph,current_F_info = Single_Subgraph_Generator(aligned_all_tif_name, A_IDs, B_IDs,filter_method,LP_Para,HP_Para)
        
        current_sub_graph = Graph_Tools.Clip_And_Normalize(current_sub_graph,show_clip)
        Graph_Tools.Show_Graph(current_sub_graph, current_key+'_SubGraph', output_folder)
        current_t_graph = Graph_Tools.Clip_And_Normalize(current_t_graph,show_clip)
        Graph_Tools.Show_Graph(current_t_graph, current_key+'_T_Graph', output_folder)
        OS_Tools.Save_Variable(output_folder, current_key+'_Sub_Info', current_F_info,extend_name = '.info')
        # Get cell maps
        cell_info = cell_dic['All_Cell_Information']
        
            
    #Step8, calculate cell subgraph and t-graph.
    
        
if __name__ == '__main__' :
    from My_Wheels.Standard_Parameters.Sub_Graph_Dics import Sub_Dic_Generator
    G8_Dic = Sub_Dic_Generator('G8+90')
    print('Test Run')
    