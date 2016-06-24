import sys
import os
import subprocess
import Config
import json
import numpy as np

ID_lst = [] # 000001.....
CutFrame_lst = [] #1478...
Loc_lst = [] # [(lat, lon),.....]
Name_lst = [] #07MD6520....
data = {}

file_name = Config.DATA_PATH + '/list_long_enough.txt'
f = open(file_name, 'r')
for line in f:
    line = line[0:-1].split('\t')
    ID_lst.append(line[0])
    CutFrame_lst.append(float(line[1]))
    loc = (float(line[2]), float(line[3])) # loc is string type, must change to float if We need use it
    Loc_lst.append(loc)
    Name_lst.append(line[4])
    data[line[0]] = loc
f.close()

def GetVideoInfo(ID):
    video_path = Config.VIDEO_ROOT_PATH + '/' + ID
    ###################################
    # Just  change this line will chage mage type
    match_path = Config.ROOT_PATH + '/' + 'Match_result/' + ID + '/deep_match_result'
    ##############################
    frame_path = video_path + '/' + 'images'
    pano_path = video_path + '/' + 'pano'
    pano_download_path = pano_path + '/' + 'download'
    frame_sift_path = pano_path + '/' + 'frame_sift'
    pano_sift_path = pano_path + '/' + 'pano_sift'
    location = data[ID]
    
    reconstruct = 'no'
    downloadpano = 'no'
    extractsift = 'no'
    fisher = 'no'
    matchFunM = 'no'
    matchLst = 'no'
    ransac_2D = 'no'
    match_result = 'no'
    match_result_extract = 'no'
    ransac_3D = 'no'
    if os.path.isfile(video_path + '/reconstruction.json'):
        reconstruct = 'yes'
    if os.path.isfile(pano_path + '/pano_lst.txt'):
        downloadpano = 'yes'
    if os.path.isfile(pano_path + '/pano_sift_lst.txt') and os.path.isfile(pano_path + '/frame_sift_lst.txt'):
        extractsift = 'yes'
    if os.path.isfile(pano_path + '/fisher_results.npy'):
        fisher = 'yes'
    if os.path.isfile(pano_path + '/results_fundM.npy'):
        matchFunM = 'yes'
    if os.path.isfile(pano_path + '/match_lst.txt'):
        matchLst = 'yes'
    if os.path.isfile(pano_path + '/latlon.gcp'):
        ransac_2D = 'yes'
    if os.path.isfile(match_path + '/match_result.npy') and os.path.isfile(match_path + '/pano_result.json'):
        match_result = 'yes'
    if os.path.isfile(match_path + '/point_set.npy'):
        match_result_extract = 'yes'
    if os.path.isfile(match_path + '/ransac_3D_result.json'):
        ransac_3D = 'yes'
    state = dict({'reconstruction':reconstruct, 'downloadpano':downloadpano, 'extractsift':extractsift, 
        'fisher':fisher, 'matchFunM':matchFunM, 'matchLst':matchLst, 'ransac_2D':ransac_2D, 
        'match_result':match_result, 'match_result_extract':match_result_extract, 'ransac_3D':ransac_3D
                 })

    output = dict({'video_path':video_path, 'frame_path':frame_path, 'pano_path':pano_path, 'location':location,
                   'pano_download_path':pano_download_path, 'frame_sift_path':frame_sift_path, 
                   'pano_sift_path':pano_sift_path, 'match_path':match_path, 'ID':ID,
                   'state':state
                  })
    '''
    for i,key in enumerate(output):
        if key != 'location' and key != 'state' and key != ID:
            if not os.path.isdir(output[key]):
                subprocess.call('mkdir -p %s'%output[key], shell=True)
    '''
    return output
def GetStateList(key_lst, state_lst): # e.g. 'reconstruction', 'yes' or 'no'
    output_lst = ID_lst
    for index in range(len(key_lst)):
        key = key_lst[index]
        state = state_lst[index]
        lst = []
        for ID in output_lst:
            info = GetVideoInfo(ID)
            if info['state'][key] == state:
                lst.append(ID)
        output_lst = lst
    return output_lst
def GetAllVideoID():
    return ID_lst
def GetAllVideoCutFrame():
    return CutFrame_lst
def GetAllVideoLoc():
    return Loc_lst
def GetAllVideoName():
    return Name_lst
def GetMatchFunMFileName(info):
    return info['pano_path'] + '/results_fundM.npy'
def GetFisherResultFileName(info):
    return info['pano_path'] + '/fisher_results.npy'
def GetMatchLstFileName(info):
    return info['pano_path'] + '/match_lst.txt'
def GetGCPFileName(info):
    return info['pano_path'] + '/latlon.gcp'
def GetTrackFileName(info):
    return info['video_path'] + '/tracks.csv'
def GetMatchResultFileName(info): # get the match point(2D) in opensfm datasset
    return info['match_path'] + '/match_result.npy'
def GetMatchResultPointFileName(info): # get the match point(3D) in google streetview data
    return info['match_path'] + '/pano_result.json'
def GetMatchResultExtractPointFileName(info): # the point to do 3D ransac
    return info['match_path'] + '/point_set.npy'
def Get3DRansacFileName(info):
    return info['match_path'] + '/ransac_3D_result.json'
def GetReconstructionFileName(info):
    return info['video_path'] + '/reconstruction.json'
def ReadReconstructionData(info):
    f = open(info['video_path'] + '/reconstruction.json', 'r')
    data = json.load(f)[0]
    f.close()
    return data
def ReadGCPData(info):
    f_name = GetGCPFileName(info)
    data = {}
    f = open(f_name, 'r')
    for line in f:
        line = line[0:-1].split('\t')
        name = line[0]
        lat = float(line[1])
        lon = float(line[2])
        data[line[0]] = [lat, lon]
    f.close()
    return data
def ArgumentComprass(data1, data2):
    if len(data1) != len(data2):
        print 'ArgCom in Info.py error'
        exit()
    lst = []
    for i in range(0, len(data1)):
        tmp = (data1[i], data2[i])
        lst.append(tmp)
    return lst
