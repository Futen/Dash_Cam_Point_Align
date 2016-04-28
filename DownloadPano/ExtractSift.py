#! /usr/bin/env python

import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import subprocess
import os
import time
import shutil
import SendEmail
from multiprocessing import Pool

def WriteImageList(DIR, OUTPUT_NAME):
    lst = [x for x in sorted(os.listdir(DIR)) if x.endswith('.jpg')]
    f = open('%s'%OUTPUT_NAME,'w')
    for one in lst:
        f.write(one + '\n')
    f.close()
def GetSiftList(DIR, OUTPUT_NAME): #output_name is output_dir + name
    lst = [x for x in sorted(os.listdir(DIR)) if x.endswith('.sift')]
    f = open('%s'%OUTPUT_NAME, 'w')
    for one in lst:
        f.write(one + '\n')
    f.close()
def ExtractSift(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    frame_path = info['frame_path']
    pano_download_path = info['pano_download_path']
    pano_path = info['pano_path']
    frame_sift_path = info['frame_sift_path']
    pano_sift_path = info['pano_sift_path']

    frame_lst_name = frame_path + '/list.txt'
    pano_lst_name = pano_download_path + '/list.txt'
    frame_sift_lst_name = pano_path + '/frame_sift_lst.txt'
    pano_sift_lst_name = pano_path + '/pano_sift_lst.txt'

    WriteImageList(frame_path, frame_lst_name)
    WriteImageList(pano_download_path, pano_lst_name)
    
    command_1 = 'VisualSFM siftgpu %s'%frame_lst_name
    command_2 = 'VisualSFM siftgpu %s'%pano_lst_name
    subprocess.call(command_1, shell=True)
    subprocess.call(command_2, shell=True)

    command_1 = 'mv %s/*.sift %s'%(frame_path, frame_sift_path)
    command_2 = 'mv %s/*.sift %s'%(pano_download_path, pano_sift_path)
    subprocess.call(command_1, shell=True)
    subprocess.call(command_2, shell=True)

    GetSiftList(frame_sift_path, frame_sift_lst_name)
    GetSiftList(pano_sift_path, pano_sift_lst_name)
    os.remove(frame_lst_name)
    os.remove(pano_lst_name)
if __name__ == '__main__':
    do_lst = Info.GetStateList(['reconstruction', 'downloadpano', 'extractsift'], ['yes', 'yes', 'no'])
    print 'Total %d videos to extract sift'%len(do_lst)
    #pool = Pool(processes = 1)
    #pool.map(ExtractSift, do_lst)
    for ID in do_lst:
        ExtractSift(ID)
        #exit()
    SendEmail.SendEmail(Text = 'ExtractSift finish!!')





