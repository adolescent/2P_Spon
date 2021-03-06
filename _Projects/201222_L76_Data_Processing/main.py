# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 13:54:11 2020

@author: ZR
This script is used for 12/22 data processing
"""
import My_Wheels.List_Operation_Kit as List_Tools
import My_Wheels.Graph_Operation_Kit as Graph_Tools
import My_Wheels.OS_Tools_Kit as OS_Tools
import cv2
data_folder = [r'E:\Test_Data\2P\201222_L76_2P']
run_list = [
    '1-001',# Spon
    '1-008',# OD
    '1-010',# G8
    '1-011',# RGLum4
    '1-014'# Spon After
    ]
all_runs = List_Tools.List_Annex(data_folder, run_list)
#%% Add 3 list for run01 to fit ROI change.
run_1 = all_runs[0]
run1_all_tif = OS_Tools.Get_File_Name(run_1)
save_path = run_1+r'\shape_extended'
OS_Tools.mkdir(save_path)
for i in range(len(run1_all_tif)):
    current_graph = cv2.imread(run1_all_tif[i],-1)
    extended_graph = Graph_Tools.Boulder_Extend(current_graph, [0,0,0,3])# 3 pix on the right.
    current_graph_name = run1_all_tif[i].split('\\')[-1]
    Graph_Tools.Show_Graph(extended_graph, current_graph_name, save_path,show_time = 0)  
#%% Then align Run01_Spon.
from My_Wheels.Translation_Align_Function import Translation_Alignment
Translation_Alignment([all_runs[0]+r'\shape_extended'],graph_shape=(325,324))
#%% Then Use this base to align other runs.
base = cv2.imread(r'I:\Test_Data\2P\201222_L76_2P\1-001\Results\Run_Average_After_Align.tif',-1)
Translation_Alignment(all_runs[1:5],base_mode = 'input',input_base = base,graph_shape = (325,324))
#%% Then calculate stim frame align data.
from My_Wheels.Stim_Frame_Align import Stim_Frame_Align
all_stim_folder = [
    r'I:\Test_Data\2P\201222_L76_2P\201222_L76_2P_stimuli\Run08_2P_OD8_auto',
    r'I:\Test_Data\2P\201222_L76_2P\201222_L76_2P_stimuli\Run10_2P_G8',
    r'I:\Test_Data\2P\201222_L76_2P\201222_L76_2P_stimuli\Run11_2P_RGLum4'
    ]
for i in range(3):
    current_stim_folder = all_stim_folder[i]
    _,stimdic = Stim_Frame_Align(current_stim_folder,jmp_step = 1500,head_extend = -1)# for T pre
    OS_Tools.Save_Variable(current_stim_folder, 'Stim_Frame_Align', stimdic)
#%% Use global morpho as base to find cell.
from My_Wheels.Cell_Find_From_Graph import Cell_Find_And_Plot
global_cell = Cell_Find_And_Plot(r'E:\Test_Data\2P\201222_L76_2P\1-008\Results', 'Global_Average_After_Align.tif', 'Global_Morpho',1)
cell_folder = r'E:\Test_Data\2P\201222_L76_2P\1-008\Results\Global_Morpho'
#%% For Run08
from My_Wheels.Standard_Stim_Processor import One_Key_Stim_Maps
from My_Wheels.Standard_Parameters.Sub_Graph_Dics import Sub_Dic_Generator
# Calculate Run08 Cells.
OD_Folder = r'E:\Test_Data\2P\201222_L76_2P\1-008'
OD_sub_dic = Sub_Dic_Generator('OD_2P')
One_Key_Stim_Maps(OD_Folder, cell_folder, OD_sub_dic)
#%% Then Run 10 G8
G8_Folder = r'E:\Test_Data\2P\201222_L76_2P\1-010'
G8_sub_dic = Sub_Dic_Generator('G8+90')
One_Key_Stim_Maps(G8_Folder, cell_folder, G8_sub_dic)
#%% Then RGLum4
RG_Folder = r'E:\Test_Data\2P\201222_L76_2P\1-011'
RG_sub_dic = Sub_Dic_Generator('RGLum4')
One_Key_Stim_Maps(RG_Folder, cell_folder, RG_sub_dic)