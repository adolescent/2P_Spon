# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:18:31 2020

@author: ZR
"""
import numpy as np

def Sub_Dic_Generator(mode,para = None):
    '''
    Generate subtraction dics.

    Parameters
    ----------
    mode : ('G8','G8+90','RGLum4','OD_OI','OD_2P')
        Mode of data. This is important for 
    para : (turple)
        API added. For parameters may need for some run...
    


    Returns
    -------
    sub_dics : TYPE
        DESCRIPTION.

    '''
    sub_dics = {}
    if mode == 'OD_OI':
        sub_dics['All-0'] = [[1,2,3,4,5,6,7,8],[0]]
        sub_dics['OD'] = [[1,2,3,4],[5,6,7,8]]
        sub_dics['L-0'] = [[1,2,3,4],[0]]
        sub_dics['R-0'] = [[5,6,7,8],[0]]
        sub_dics['A-O'] = [[4,8],[2,6]]
        sub_dics['H-V'] = [[3,7],[1,5]]
        sub_dics['HV-AO'] = [[1,3,5,7],[2,4,6,8]]
        
    elif mode == 'OD_2P':
        sub_dics['All-0'] = [[1,2,3,4,5,6,7,8],[0]]
        sub_dics['OD'] = [[1,3,5,7],[2,4,6,8]]
        sub_dics['L-0'] = [[1,3,5,7],[0]]
        sub_dics['R-0'] = [[2,4,6,8],[0]]
        sub_dics['H-V'] = [[1,2],[5,6]]
        sub_dics['A-O'] = [[3,4],[7,8]]
        sub_dics['HV-AO'] = [[1,2,5,6],[3,4,7,8]]
        
    elif mode == 'G8_Norm':# Normal G8, ID1 is right moving bars.
        sub_dics['All-0'] = [[1,2,3,4,5,6,7,8],[0]]
        sub_dics['H-V'] = [[3,7],[1,5]]
        sub_dics['A-O'] = [[4,8],[2,6]]
        sub_dics['HV-AO'] = [[1,3,5,7],[2,4,6,8]]
        sub_dics['Orien0-0'] = [[3,7],[0]]
        sub_dics['Orien45-0'] = [[4,8],[0]]
        sub_dics['Orien90-0'] = [[1,5],[0]]
        sub_dics['Orien135-0'] = [[2,6],[0]]
        sub_dics['DirU-D'] = [[2,3,4],[6,7,8]]
        sub_dics['DirL-R'] = [[4,5,6],[8,1,2]]
        
    elif mode == 'G8+90': # In early 2p stims, use up moving bars as ID1.
        sub_dics['All-0'] = [[1,2,3,4,5,6,7,8],[0]]
        sub_dics['H-V'] = [[1,5],[3,7]]
        sub_dics['A-O'] = [[2,6],[4,8]]
        sub_dics['HV-AO'] = [[1,3,5,7],[2,4,6,8]]
        sub_dics['HA-VO'] = [[1,2,5,6],[3,4,7,8]]
        sub_dics['Orien0-0'] = [[1,5],[0]]
        sub_dics['Orien45-0'] = [[2,6],[0]]
        sub_dics['Orien90-0'] = [[3,7],[0]]
        sub_dics['Orien135-0'] = [[4,8],[0]]
        sub_dics['DirU-D'] = [[2,1,8],[4,5,6]]
        sub_dics['DirL-R'] = [[2,3,4],[6,7,8]]
        sub_dics['Dir0-0'] = [[1],[0]]
        sub_dics['Dir45-0'] = [[2],[0]]
        sub_dics['Dir90-0'] = [[3],[0]]
        sub_dics['Dir135-0'] = [[4],[0]]
        sub_dics['Dir180-0'] = [[5],[0]]
        sub_dics['Dir225-0'] = [[6],[0]]
        sub_dics['Dir270-0'] = [[7],[0]]
        sub_dics['Dir315-0'] = [[8],[0]]
        
    elif mode == 'RGLum4':
        sub_dics['All-0'] = [[1,2,3,4],[0]]
        sub_dics['RG-Lum'] = [[1,2],[3,4]]
        sub_dics['A-O'] = [[1,3],[2,4]]
        sub_dics['RG-0'] = [[1,2],[0]]
        sub_dics['Lum-0'] = [[3,4],[0]]
        
        
    elif mode == 'Color7Dir8':
        print('ID1 as up moving bars.')
        print('Use ISI as 0 in this dic.')
        sub_dics['H-V'] = [[1,9,17,25,33,41,49,5,13,21,29,37,45,53],[3,11,19,27,35,43,51,7,15,23,31,39,47,55]]
        sub_dics['A-O'] = [[2,10,18,26,34,42,50,6,14,22,30,38,46,54],[4,12,20,28,36,44,52,8,16,24,32,40,48,56]]
        sub_dics['DirL-R'] = [[2,10,18,26,34,42,50,3,11,19,27,35,43,51,4,12,20,28,36,44,52],[6,7,8,14,15,16,22,23,24,30,31,32,38,39,40,46,47,48,54,55,56]]
        sub_dics['DirU-D'] = [[2,1,8,10,9,16,18,17,24,26,27,32,34,35,40,42,43,48,50,51,56],[4,5,6,12,13,14,20,21,22,28,29,30,36,37,38,44,45,46,52,53,54]]
        sub_dics['Orien90-0'] = [[3,11,19,27,35,43,51,7,15,23,31,39,47,55],[-1]]
        sub_dics['Orien135-0'] = [[4,12,20,28,36,44,52,8,16,24,32,40,48,56],[-1]]
        sub_dics['Orien0-0'] = [[1,9,17,25,33,41,49,5,13,21,29,37,45,53],[-1]]
        sub_dics['Orien45-0'] = [[2,10,18,26,34,42,50,6,14,22,30,38,46,54],[-1]]
        sub_dics['Red-White'] = [[1,2,3,4,5,6,7,8],[49,50,51,52,53,54,55,56]]
        sub_dics['Yellow-White'] = [[9,10,11,12,13,14,15,16],[49,50,51,52,53,54,55,56]]
        sub_dics['Green-White'] = [[17,18,19,20,21,22,23,24],[49,50,51,52,53,54,55,56]]
        sub_dics['Cyan-White'] = [[25,26,27,28,29,30,31,32],[49,50,51,52,53,54,55,56]]
        sub_dics['Blue-White'] = [[33,34,35,36,37,38,39,40],[49,50,51,52,53,54,55,56]]
        sub_dics['Purple-White'] = [[41,42,43,44,45,46,47,48],[49,50,51,52,53,54,55,56]]
        sub_dics['Red-Cyan'] = [[1,2,3,4,5,6,7,8],[25,26,27,28,29,30,31,32]]
        sub_dics['Yellow-Blue'] = [[9,10,11,12,13,14,15,16],[33,34,35,36,37,38,39,40]]
        sub_dics['Green-Purple'] = [[17,18,19,20,21,22,23,24],[41,42,43,44,45,46,47,48]]
        sub_dics['All-0'] = [list(np.arange(1,57)),[-1]]
        
    elif mode == 'Color7Dir8+90':
        print('ID1 as right moving bars.')
        print('Use ISI as 0 in this dic.')
        sub_dics['H-V'] = [[3,11,19,27,35,43,51,7,15,23,31,39,47,55],[1,9,17,25,33,41,49,5,13,21,29,37,45,53]]
        sub_dics['A-O'] = [[4,12,20,28,36,44,52,8,16,24,32,40,48,56],[2,10,18,26,34,42,50,6,14,22,30,38,46,54]]
        sub_dics['DirU-D'] = [[2,10,18,26,34,42,50,3,11,19,27,35,43,51,4,12,20,28,36,44,52],[6,7,8,14,15,16,22,23,24,30,31,32,38,39,40,46,47,48,54,55,56]]
        sub_dics['DirL-R'] = [[4,5,6,12,13,14,20,21,22,28,29,30,36,37,38,44,45,46,52,53,54],[2,1,8,10,9,16,18,17,24,26,27,32,34,35,40,42,43,48,50,51,56]]
        sub_dics['Orien0-0'] = [[3,11,19,27,35,43,51,7,15,23,31,39,47,55],[-1]]
        sub_dics['Orien45-0'] = [[4,12,20,28,36,44,52,8,16,24,32,40,48,56],[-1]]
        sub_dics['Orien90-0'] = [[1,9,17,25,33,41,49,5,13,21,29,37,45,53],[-1]]
        sub_dics['Orien135-0'] = [[2,10,18,26,34,42,50,6,14,22,30,38,46,54],[-1]]
        sub_dics['Red-White'] = [[1,2,3,4,5,6,7,8],[49,50,51,52,53,54,55,56]]
        sub_dics['Yellow-White'] = [[9,10,11,12,13,14,15,16],[49,50,51,52,53,54,55,56]]
        sub_dics['Green-White'] = [[17,18,19,20,21,22,23,24],[49,50,51,52,53,54,55,56]]
        sub_dics['Cyan-White'] = [[25,26,27,28,29,30,31,32],[49,50,51,52,53,54,55,56]]
        sub_dics['Blue-White'] = [[33,34,35,36,37,38,39,40],[49,50,51,52,53,54,55,56]]
        sub_dics['Purple-White'] = [[41,42,43,44,45,46,47,48],[49,50,51,52,53,54,55,56]]
        sub_dics['Red-Cyan'] = [[1,2,3,4,5,6,7,8],[25,26,27,28,29,30,31,32]]
        sub_dics['Yellow-Blue'] = [[9,10,11,12,13,14,15,16],[33,34,35,36,37,38,39,40]]
        sub_dics['Green-Purple'] = [[17,18,19,20,21,22,23,24],[41,42,43,44,45,46,47,48]]
        sub_dics['All-0'] = [list(np.arange(1,57)),[-1]]
    
    elif mode == 'Shape3Dir8':
        sub_dics['H-V'] = [[3,7],[1,5]]
        sub_dics['A-O'] = [[4,8],[2,6]]
        sub_dics['Triangle-Bar'] = [[9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8]]
        sub_dics['Circle-Bar'] = [[17,18,19,20,21,22,23,24],[1,2,3,4,5,6,7,8]]
        sub_dics['Circle-Triangle'] = [[17,18,19,20,21,22,23,24],[9,10,11,12,13,14,15,16]]
        sub_dics['DirU-D_All'] = [[2,3,4,10,11,12,18,19,20],[6,7,8,14,15,16,22,23,24]]
        sub_dics['DirL-R_All'] = [[4,5,6,12,13,14,20,21,22],[2,1,8,10,9,16,18,17,24]]
        sub_dics['DirU-D_Bar'] = [[2,3,4],[6,7,8]]
        sub_dics['DirU-D_Circle'] = [[18,19,20],[22,23,24]]
        sub_dics['DirU-D_Triangle'] = [[10,11,12],[14,15,16]]
        sub_dics['DirL-R_Bar'] = [[4,5,6],[2,1,8]]
        sub_dics['DirL-R_Circle'] = [[20,21,22],[24,17,18]]
        sub_dics['DirL-R_Triangle'] = [[12,13,14],[9,10,16]]
        sub_dics['Circle-0'] = [[17,18,19,20,21,22,23,24],[-1]]
        sub_dics['Bars-0'] = [[1,2,3,4,5,6,7,8],[-1]]
        sub_dics['Triangle-0'] = [[9,10,11,12,13,14,15,16],[-1]]
        sub_dics['All-0'] = [list(np.arange(1,25)),[-1]]
        
    elif mode == 'G16_2P':# id 1,Up moving. Counter clockwise.
        sub_dics['All-0'] = [list(np.arange(1,17)),[0]]
        sub_dics['H-V'] = [[1,9],[5,13]]
        sub_dics['A-O'] = [[3,11],[7,15]]
        sub_dics['DirU-D'] = [[1,2,3,4,14,15,16],[6,7,8,9,10,11,12]]
        sub_dics['DirL-R'] = [[2,3,4,5,6,7,8],[10,11,12,13,14,15,16]]
        sub_dics['HV-AO'] = [[1,5,9,13],[3,7,11,15]]
        sub_dics['Orien0-0'] = [[1,9],[0]]
        sub_dics['Orien22.5-0'] = [[2,10],[0]]
        sub_dics['Orien45-0'] = [[3,11],[0]]
        sub_dics['Orien67.5-0'] = [[4,12],[0]]
        sub_dics['Orien90-0'] = [[5,13],[0]]
        sub_dics['Orien112.5-0'] = [[6,14],[0]]
        sub_dics['Orien135-0'] = [[7,15],[0]]
        sub_dics['Orien157.5-0'] = [[8,16],[0]]
        sub_dics['Dir0-180'] = [[1],[9]]
        sub_dics['Dir22.5-202.5'] = [[2],[10]]
        sub_dics['Dir45-225'] = [[3],[11]]
        sub_dics['Dir67.5-247.5'] = [[4],[12]]
        sub_dics['Dir90-270'] = [[5],[13]]
        sub_dics['Dir112.5-292.5'] = [[6],[14]]
        sub_dics['Dir135-315'] = [[7],[15]]
        sub_dics['Dir157.5-337.5'] = [[8],[16]]

        
    elif mode =='RFSize':
        if para == None:
            raise IOError('Please give RF paras.')
        sizes = para['Size']
        dirs = para['Dir']
        size_num = len(sizes)
        dir_num = len(dirs)
        # Get all shapes id.
        all_size_dic = {}
        for i in range(size_num):
            all_size_dic[sizes[i]] = list(range(i*dir_num+1,(i+1)*dir_num+1))
        # Then get all dir ids.
        all_dir_dic = {}
        for i in range(dir_num):
            current_dir_id = []
            for j in range(size_num):
                current_dir_id.append(i+1+j*dir_num)
            all_dir_dic[dirs[i]] = current_dir_id
        # At last, return subtraction pairs.
        sizes.sort()# sort from small to big, then sub by sequence.
        # Calculate size tuning graph here.
        for i in range(size_num-1):
            current_sub_name = 'Size'+str(sizes[i])+'-Size'+str(sizes[i+1])
            sub_dics[current_sub_name] = [all_size_dic[sizes[i]],all_size_dic[sizes[i+1]]]
        # And direction - 0 graphs.
        for i in range(dir_num):
            current_sub_name = 'Dir'+str(dirs[i])+'-0'
            sub_dics[current_sub_name] = [all_dir_dic[dirs[i]],[-1]]
            
    elif mode == 'SFTF':
        if para == None:
            raise IOError('Please give SF paras.')
        SFs = para['SF']
        TFs = para['TF']
        Dirs = para['Dir']
        SF_num = len(SFs)
        TF_num = len(TFs)
        Dir_num = len(Dirs)
        # Get Dir ids
        all_Dir_dic = {}
        for i in range(Dir_num):
            all_Dir_dic[Dirs[i]] = list(range(i*SF_num*TF_num+1,(i+1)*SF_num*TF_num+1))
        # Get SF ids
        all_SF_dic = {}
        for i in range(SF_num):
            current_SF_id = []
            for j in range(TF_num*Dir_num):
                current_SF_id.append(i+1+j*SF_num)
            all_SF_dic[SFs[i]]=current_SF_id
        # Get TF ids
        all_TF_dic = {}
        for i in range(TF_num):
            current_TF_id = []
            for j in range(Dir_num):
                for k in range(SF_num):
                    current_TF_id.append(1+k+i*SF_num+j*SF_num*TF_num)
            all_TF_dic[TFs[i]] = current_TF_id
        # At last, we can calculate SF-TF graphs here.
        if SF_num>1:
            SFs.sort()
            for i in range(SF_num-1):
                current_file_name = 'SF'+str(SFs[i])+'-SF'+str(SFs[i+1])
                sub_dics[current_file_name] = [all_SF_dic[SFs[i]],all_SF_dic[SFs[i+1]]]
        else:
            print('Only 1 SF given, no SF sub maps.')
        # Then for TF maps.
        if TF_num>1:
            TFs.sort()
            for i in range(TF_num-1):
                current_file_name = 'TF'+str(TFs[i])+'-SF'+str(TFs[i+1])
                sub_dics[current_file_name] = [all_TF_dic[TFs[i]],all_TF_dic[TFs[i+1]]]
        else:
            print('Only 1 TF given, no TF sub maps.')
        # Then dir-0
        for i in range(Dir_num):
            current_file_name = 'Dir'+str(Dirs[i])+'-0'
            sub_dics[current_file_name] = [all_Dir_dic[Dirs[i]],[-1]]
            
        
    else:
        raise IOError('Method not understand, please check.')
            
    return sub_dics