# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 15:47:51 2019

@author: ZR

Graph Operation kits, this tool box aims at doing all graph Works
"""

import cv2
import numpy as np
import os

#%% Function1: Graph Average(From File).

def Average_From_File(Name_List):
    """
    Average Graph Files, return an aligned matrix. RGB Graph shall be able to use it (not tested).

    Parameters
    ----------
    Name_List : (list)
        File Name List. all list units shall be a direct file path.

    Returns
    -------
    averaged_graph : (2D ndarray, float64)
        Return averaged graph, data type f8 for convenient.

    """
    graph_num = len(Name_List)
    temple_graph = cv2.imread(Name_List[0],-1)
    averaged_graph = np.zeros(shape = temple_graph.shape,dtype = 'f8')
    for i in range(graph_num):
        current_graph = cv2.imread(Name_List[i],-1).astype('f8')# Read in graph as origin depth, and change into f8
        averaged_graph += current_graph/graph_num
    return averaged_graph

#%% Function2: Clip And Normalize input graph
def Clip_And_Normalize(input_graph,clip_std = 2.5,normalization = True,bit = 'u2'):
    """
    Clip input graph,then normalize them to specific bit depth, output graph be shown directly.
    If not normalize, just return origin dtype.
    
    Parameters
    ----------
    input_graph : (2D ndarray)
        Input graph matrix. Need to be a 2D ndarray.
    clip_std : (float), optional
        How much std will the input graph be clipped into. The default is 2.5, holding 99% data unchanged.
        This Variable can be set to -1 to skip clip.
    normalization : (Bool), optional
        Whether normalization is done here. The default is True, if False, no normalization will be done here.
    bit : ('u2','u1','f8'), optional
        dtype of output graph. This parameter will affect normalization width. The default is 'u2'.

    Returns	
    -------
    processed_graph : (2D ndarray)
        Output graphs.

    """
    origin_dtype = str(input_graph.dtype)
    #Step1, clip
    input_graph = input_graph.astype('f8')
    if clip_std > 0:
        lower_level = input_graph.mean()-clip_std*input_graph.std()
        higher_level = input_graph.mean()+clip_std*input_graph.std()
        clipped_graph = np.clip(input_graph,lower_level,higher_level)
    else:
        print('No Clip Done.')
        clipped_graph = input_graph
        
    #Step2, normalization
    norm_graph = (clipped_graph-clipped_graph.min())/(clipped_graph.max()-clipped_graph.min())
    if normalization == True:
        if bit == 'u2':
            processed_graph = (norm_graph*65535).astype('u2')
        elif bit == 'u1':
            processed_graph = (norm_graph*255).astype('u1')
        elif bit == 'f8':
            print('0-1 Normalize data returned')
            processed_graph = norm_graph
        else:
            raise IOError('Output dtype not supported yet.')
    else:
        print('No Normalization Done.')
        processed_graph = clipped_graph.astype(origin_dtype)
        
    return processed_graph
#%% Function3: Show Graph and Write them.
def Show_Graph(input_graph,graph_name,save_path,show_time = 5000,write = True,graph_formation = '.tif'):
    """
    Show input graph, and write them in ordered path.

    Parameters
    ----------
    input_graph : (2D Ndarray,dtype = 'u1' or 'u2')
        Input graph. Must be plotable dtype, or there will be problems in plotting.
    graph_name : (str)
        Graph name.
    save_path : (str)
        Save path. can be empty is write = False
    show_time : (int), optional
        Graph show time, ms. This value can be set to 0 to skip show.The default is = 5000.
    write : (Bool), optional
        Whether graph is written. If false, show graph only. The default is True.
    graph_formation : (str),optional
        What kind of graph you want to save. The default is '.tif'

    Returns
    -------
    None.

    """
    if show_time != 0:
        cv2.imshow(graph_name,input_graph)
        cv2.waitKey(show_time)
        cv2.destroyAllWindows()
    if write == True:
        
        if os.path.exists(save_path):# If path exists
            cv2.imwrite(save_path+r'\\'+graph_name+graph_formation,input_graph)
        else:# Else, creat save folder first.
            os.mkdir(save_path)
            cv2.imwrite(save_path+r'\\'+graph_name+graph_formation,input_graph)
        
#%% Function 4: Graph Boulder Cut
def Graph_Cut(graph,boulders):
    """
    Cut Graph with specific boulders.

    Parameters
    ----------
    graph : (ndarray)
        Input graph.
    boulders : (list,length = 4,element = int)
        4 element list. Telling cut pix of 4 directions.
        [0]:Up; [1]:Down; [2]:Left; [3]:Right

    Returns
    -------
    cutted_graph : (ndarray)
        Cutted graph. dtype consist with input graph.

    """
    ud_range,lr_range = np.shape(graph)
    if ud_range < (boulders[0]+boulders[1]) or lr_range < (boulders[2]+boulders[3]):
        raise IOError('Cut bouder too big, misison impossible.')
    cutted_graph = graph[boulders[0]:(ud_range-boulders[1]),boulders[2]:(lr_range-boulders[3])]
    
    return cutted_graph
#%% Function 5 Boulder Fill
def Boulder_Fill(graph,boulders,fill_value):
    """
    Fill Graph Boulder with specific value. Graph shape will not change.

    Parameters
    ----------
    graph : (2D Array)
        Input graph.
    boulders : (4 element list)
        Telling boulder width in all 4 directions.
        [0]:Up; [1]:Down; [2]:Left; [3]:Right
        fill_value : (number)
        Value you want to fill in boulders.

    Returns
    -------
    graph : (2D Array)
        Boulder filled graph.

    """
    length,width = np.shape(graph)
    graph[0:boulders[0],:] = fill_value
    graph[(length-boulders[1]):length,:] = fill_value
    graph[:,0:boulders[2]] = fill_value
    graph[:,(width-boulders[3]):width] = fill_value
    
    return graph
#%% Function 6 Grap_Combine
def Graph_Combine(graph_A,graph_B,bit = 'u1'):
    """
    Combine 2 input graphs, just add together.

    Parameters
    ----------
    graph_A : (Input Graph, 2D or 3D Array)
        Graph A. Gray map 2D, color map 3D.
    graph_B : (Input Graph, 2D or 3D Array)
        Graph B. same type as A.
    bit : ('u1' or 'u2'), optional
        DESCRIPTION. The default is 'u1'.

    Returns
    -------
    combined_graph : TYPE
        Graph same shape as input.

    """
    graph_A = graph_A.astype('f8')
    graph_B = graph_B.astype('f8')
    # Check graph shape
    if np.shape(graph_A) != np.shape(graph_B):
        raise IOError('Graph Shape not match, CHECK please.')
    # Determine max pix value.
    if bit == 'u1':
        max_value = 255
    elif bit == 'u2':
        max_value = 65535
    else:
        raise IOError('Incorrect bit depth.')
    # Then Add Up 2 graphs, then clip them.
    combined_graph = np.clip(graph_A + graph_B,0,max_value).astype(bit)
    
    return combined_graph
#%% Function7 Graph Depth Change
def Graph_Depth_Change(graph,output_bit = 'u2'):
    """
    Change Graph Depth between uint8 and uint16. Change from 1 to another.

    Parameters
    ----------
    graph : (Input Graph, 2D or 3D Array)
        Input Graph of .
    current_bit : ('u1' or 'u2'), optional
        Dtype of output graph. The default is 'u2'.

    Returns
    -------
    output_graph : (2D or 3D Array)
        Output graph.

    """
    graph = graph.astype('f8')
    normalized_graph = (graph-np.min(graph))/(np.max(graph)-np.min(graph))
    if output_bit == 'u1':
        max_value = 255
    elif output_bit == 'u2':
        max_value = 65535
    else:
        raise IOError('Incorrect bit detph')
    output_graph = (normalized_graph*max_value).astype(output_bit)
    
    return output_graph
#%% Function8 Sub Graph Generator
def Graph_Subtractor(tif_names,A_Sets,B_Sets,clip_std = 2.5,output_type = 'u2'):
    """
    Get A-B graph.

    Parameters
    ----------
    tif_names : (list)
        List of all aligned tif names.This can be found in Align_Property(Cross_Run_Align.Do_Align())
    A_Sets : (list)
        Frame id of set A.Use this to get specific frame name.
    B_Sets : (list)
        Frame id of set B.
    clip_std : (number), optional
        How many std will be used to clip output graph. The default is 2.5.
    output_type : ('f8','u1','u2'), optional
        Data type of output grpah. The default is 'u2'.

    Returns
    -------
    subtracted_graph : (2D ndarray)
        Subtracted graph.
    dF_F:(float)
        Rate of changes, (A-B)/B

    """
    A_Set_tif_names = []
    for i in range(len(A_Sets)):
        A_Set_tif_names.append(tif_names[A_Sets[i]])
    B_Set_tif_names = []
    for i in range(len(B_Sets)):
        B_Set_tif_names.append(tif_names[B_Sets[i]])
    A_Set_Average = Average_From_File(A_Set_tif_names)
    B_Set_Average = Average_From_File(B_Set_tif_names)
    simple_sub = A_Set_Average - B_Set_Average
    dF_F = simple_sub.mean()/B_Set_Average.mean()
    subtracted_graph = Clip_And_Normalize(simple_sub,clip_std,bit = output_type)
    return subtracted_graph,dF_F
    
#%% Function 9 Graph Overlapping/Union
def Graph_Overlapping(graph_A,graph_B,thres = 0.5):
    """
    Simple overlapping calculation, used to compare cell locations

    Parameters
    ----------
    graph_A : (2D Array/2D Array*3)
        Graph A, regarded as gray graph.
    graph_B : (2D Array/2D Array*3)
        Graph B, regarded as gray graph.
    thres : (0~1 float)
        Threshold used for binary data.

    Returns
    -------
    intersection_graph : (2D Array, dtype = 'u1')
        Overlapping graph. Both active point will be shown on this graph.
    union_graph : (2D Array, dtype = 'u1')
        Union graph. All active point in single graph will be shown.
    active_areas:(list,3-element)
        [A_areas,B_areas,intersection_areas]
    """
    # Process graph first.
    A_shape = np.shape(graph_A)
    if len(A_shape) == 3:# Meaning color graph.
        used_A_graph = cv2.cvtColor(graph_A,cv2.COLOR_BGR2GRAY).astype('f8')
    else:
        used_A_graph = graph_A.astype('f8')
    norm_A_graph = (used_A_graph-used_A_graph.min())/(used_A_graph.max()-used_A_graph.min())
    bool_A = norm_A_graph > thres
    B_shape = np.shape(graph_B)
    if len(B_shape) == 3:# Meaning color graph.
        used_B_graph = cv2.cvtColor(graph_B,cv2.COLOR_BGR2GRAY).astype('f8')
    else:
        used_B_graph = graph_B.astype('f8')
    norm_B_graph = (used_B_graph-used_B_graph.min())/(used_B_graph.max()-used_B_graph.min())
    bool_B = norm_B_graph > thres    
    # Then calculate intersection and union.
    bool_intersection = bool_A*bool_B
    bool_union = bool_A+bool_B
    A_areas = bool_A.sum()
    B_areas = bool_B.sum()
    intersection_areas = bool_intersection.sum()
    active_areas = [A_areas,B_areas,intersection_areas]
    #return bool_intersection,bool_union
    # Output as u1 type at last.
    intersection_graph = (bool_intersection.astype('u1'))*255
    union_graph = (bool_union.astype('u1'))*255
    return intersection_graph,union_graph,active_areas
    
#%% Functino 10 : Plot several input graph on same map, using different colors.
from My_Wheels.Calculation_Functions import Color_Dictionary
def Combine_Graphs(
        graph_turples,
        all_colors = ['r','g','b','y','c','p'],
        graph_size = (512,512)
        ):
    """
    Combine several map together, using different colors. This function better be used on binary graphs.

    Parameters
    ----------
    graph_turples : (turple)
        Turple list of input graph, every element shall be a 2D array, 6 map supported for now.
    all_colors : (list), optional
        Sequence of input graph colors. The default is ['r','g','b','y','c','p'].
    graph_size : (2-element turple),optional
        Graph size. Pre defined for convenience

    Returns
    -------
    Combined_Map : (2D array, 3 channel,dtype = 'u1')
        Combined graph. Use u1 graph.
    """
    Combined_Map = np.zeros(shape = (graph_size[0],graph_size[1],3),dtype = 'f8')
    Graph_Num= len(graph_turples)
    if Graph_Num > len(all_colors):
        raise ValueError('Unable to combine so many graphs for now..\n')
    for i in range(Graph_Num):
        current_graph = graph_turples[i]
        if len(np.shape(current_graph)) == 3:# for color map,change into gray.
            current_graph = cv2.cvtColor(current_graph,cv2.COLOR_BGR2GRAY).astype('f8')
        current_graph = Clip_And_Normalize(current_graph,clip_std = 0, bit = 'f8')# Normalize and to 0-1
        # After processing, draw current graph onto combined map.
        current_color = Color_Dictionary[all_colors[i]]
        Combined_Map[:,:,0] = Combined_Map[:,:,0]+current_graph*current_color[0]
        Combined_Map[:,:,1] = Combined_Map[:,:,1]+current_graph*current_color[1]
        Combined_Map[:,:,2] = Combined_Map[:,:,2]+current_graph*current_color[2]
    # After that, clip output graph.
    Combined_Map = np.clip(Combined_Map,0,255).astype('u1')    
    return Combined_Map
#%% Function 11 : Easy Plot.
def EZPlot(input_graph,show_time = 7000):
    """
    Easy plot, do nothing and just show graph.

    Parameters
    ----------
    input_graph : (2D Array, u1 or u2 dtype)
        Input graph.
    show_time : (int),optional
        Show time. The default is 7s.
    Returns
    -------
    int
        Fill in blank.

    """
    graph_name = 'current_graph'
    Show_Graph(input_graph,graph_name,save_path = '',show_time = show_time,write = False)
    return 0
