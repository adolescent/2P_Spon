# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:53:39 2020

@author: ZR
"""
import My_Wheels.OS_Tools_Kit as OS_Tools
import My_Wheels.Graph_Operation_Kit as Graph_Tools
import cv2
import scipy

def Video_From_File(
        data_folder,
        graph_size = (512,512),
        file_type = '.tif',
        fps = 15,
        clip = 5,
        gaussian = 1,
        frame_annotate = True,
        ):
    """
    The function to fold all graphs in folder into a video file. All paremeters of video can be adjusted.
    Video can only be shown as 8 bit, if input graph is 16bit, we need to change it into 8.
    
    Parameters
    ----------
    data_folder : (str)
        Folder of all image files.
    graph_size : (turple)
        Size of graphs. Need to be pre-given for convenience. The default is (512，512)
    file_type : (str), optional
        Extend name of image files. The default is '.tif'.
    fps : (int), optional
        Frame per second. The default is 15.
    clip : (float), optional
        Std of clip for graph to average. The default is 5.
    gaussian : (int), optional
        Gaussian Blurry std. The bigger this vale, the more blurry will be. The default is 1.
    frame_annotate : (bool),optional
        Whether we show frame number on video. The default is true.
 

    Returns
    True.

    """

    all_tif_name = OS_Tools.Get_File_Name(path = data_folder,file_type = file_type)
    graph_num = len(all_tif_name)
    video_writer = cv2.VideoWriter(data_folder+r'\\Video.mp4',cv2.VideoWriter_fourcc('H','E','V','C'),fps,graph_size,0)
    #video_writer = cv2.VideoWriter(data_folder+r'\\Video.avi',-1,fps,graph_size,0)
    for i in range(graph_num):
        raw_graph = cv2.imread(all_tif_name[i],-1).astype('f8')
        # Do clip first.
        u1_writable_graph = Graph_Tools.Clip_And_Normalize(raw_graph,clip_std = clip,bit = 'u1')
        u1_writable_graph = scipy.ndimage.gaussian_filter(u1_writable_graph,sigma = gaussian)
        if frame_annotate == True:
            cv2.putText(u1_writable_graph,'Stim ID = '+str(i),(300,30),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255),1)
        video_writer.write(u1_writable_graph)
    del video_writer 
    return True