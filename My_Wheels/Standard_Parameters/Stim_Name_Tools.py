# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:28:17 2021

@author: ZR
"""

#%% Function1, return 
def Stim_ID_Combiner(mode,para_dic = None):
    
    Stim_IDs = {}
    if mode == 'G16_Oriens':
        print('Orientation 0 is horizontal, counterclockwise.')
        Stim_IDs['Orien0'] = [1,9]
        Stim_IDs['Orien22.5'] = [2,10]
        Stim_IDs['Orien45'] = [3,11]
        Stim_IDs['Orien67.5'] = [4,12]
        Stim_IDs['Orien90'] = [5,13]
        Stim_IDs['Orien112.5'] = [6,14]
        Stim_IDs['Orien135'] = [7,15]
        Stim_IDs['Orien157.5'] = [8,16]
        Stim_IDs['Blank'] = [0]
        
    elif mode == 'G16_Dirs':
        print('Dir 0 is horizontal, moving up. Counterclockwise.')
        for i in range(16):
            current_name = 'Dir'+str(i*22.5)
            Stim_IDs[current_name] = [i+1]
        Stim_IDs['Blank'] = [0]
        Stim_IDs['All'] = list(range(1,17))
        
    elif mode == 'G16_Radar':
        print('Dir 0 is horizontal, moving up. Counterclockwise.')
        for i in range(16):
            current_name = 'Dir'+str(i*22.5)
            Stim_IDs[current_name] = [i+1]
        
    elif mode == 'Color7Dir8_Colors':
        Stim_IDs['Red'] = list(range(1,9))
        Stim_IDs['Yellow'] = list(range(9,17))
        Stim_IDs['Green'] = list(range(17,25))
        Stim_IDs['Cyan'] = list(range(25,33))
        Stim_IDs['Blue'] = list(range(33,41))
        Stim_IDs['Purple'] = list(range(41,49))
        Stim_IDs['While'] = list(range(49,57))
        Stim_IDs['All'] = list(range(1,57))
        
    elif mode == 'OD_2P':
        print('1357L,2468R,12 up moving.')
        Stim_IDs['L_All'] = [1,3,5,7]
        Stim_IDs['L_Orien0'] = [1]
        Stim_IDs['L_Orien45'] = [3]
        Stim_IDs['L_Orien90'] = [5]
        Stim_IDs['L_Orien135'] = [7]
        Stim_IDs['R_All'] = [2,4,6,8]
        Stim_IDs['R_Orien0'] = [2]
        Stim_IDs['R_Orien45'] = [4]
        Stim_IDs['R_Orien90'] = [6]
        Stim_IDs['R_Orien135'] = [8]
        Stim_IDs['All'] = list(range(1,9))
        Stim_IDs['Blank'] = [0]
        
    elif mode == 'OD_2P_Radar':
        print('Symetric radar id provided, angle baise = 22.5 advised.')
        Stim_IDs['L_deg0'] = [1]
        Stim_IDs['L_deg45'] = [3]
        Stim_IDs['L_deg90'] = [5]
        Stim_IDs['L_deg135'] = [7]
        Stim_IDs['R_deg135'] = [8]
        Stim_IDs['R_deg90'] = [6]
        Stim_IDs['R_deg45'] = [4]
        Stim_IDs['R_deg0'] = [2]
        
    elif mode == 'Shape3Dir8_General':
        print('General properties of S3D8.ID 1 moving right. Draw in 3*4')
        Stim_IDs['Bars'] =list(range(1,9))
        Stim_IDs['Triangles'] = list(range(9,17))
        Stim_IDs['Circles'] = list(range(17,25))
        Stim_IDs['All'] = list(range(1,25))
        Stim_IDs['Dir0'] = [3,11,19]
        Stim_IDs['Dir45'] = [4,12,20]
        Stim_IDs['Dir90'] = [5,13,21]
        Stim_IDs['Dir135'] = [6,14,22]
        Stim_IDs['Dir180'] = [7,15,23]
        Stim_IDs['Dir225'] = [8,16,24]
        Stim_IDs['Dir270'] = [1,9,17]
        Stim_IDs['Dir315'] = [2,10,18]
        
        
        
        
    elif mode == 'Shape3Dir8_Single':
        print('Generate single condition S3D8 subplots.ID 1 moving right. Draw in 4*8')
        for i in range(8):
            c_name = 'All_Dir'+str(i*45)
            if i >5:
                Stim_IDs[c_name] = [i-5,i+3,i+11]
            else:
                Stim_IDs[c_name] = [i+3,i+11,i+19]
                
        for i in range(8):
            c_name = 'Bar_Dir'+str(i*45)
            if i >5:
                Stim_IDs[c_name] = [i-5]
            else:
                Stim_IDs[c_name] = [i+3]
        for i in range(8):
            c_name = 'Triangle_Dir'+str(i*45)
            if i >5:
                Stim_IDs[c_name] = [i+3]
            else:
                Stim_IDs[c_name] = [i+11]
        for i in range(8):
            c_name = 'Circle_Dir'+str(i*45)
            if i >5:
                Stim_IDs[c_name] = [i+11]
            else:
                Stim_IDs[c_name] = [i+19]
                
    elif mode == 'RFSize':
        if para_dic == None:
            raise IOError('Please give RF Size dics.')
        sizes = para_dic['Size']
        dirs = para_dic['Dir']
        cond_num = len(sizes)*len(dirs)
        size_num = len(sizes)
        dir_num = len(dirs)
        Stim_IDs['All'] = list(range(1,cond_num+1))
        # Then all sizes
        for i in range(size_num):
            c_size = sizes[i]
            
        


    return Stim_IDs
#%% Function 2, 
def Ortho_Stim_Name(input_stim_name):
    pass
