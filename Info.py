import sys
import os
import subprocess
import Config
import json

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
    state = dict({'reconstruction':reconstruct, 'downloadpano':downloadpano, 'extractsift':extractsift, 'fisher':fisher, 'matchFunM':matchFunM,
        'matchLst':matchLst, 'ransac_2D':ransac_2D
                 })

    output = dict({'video_path':video_path, 'frame_path':frame_path, 'pano_path':pano_path, 'location':location,
                   'pano_download_path':pano_download_path, 'frame_sift_path':frame_sift_path, 'pano_sift_path':pano_sift_path,
                   'state':state
                  })
    for i,key in enumerate(output):
        if key != 'location' and key != 'state':
            if not os.path.isdir(output[key]):
                subprocess.call('mkdir -p %s'%output[key], shell=True)
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
def ReadReconstructionData(info):
    f = open(info['video_path'] + '/reconstruction.json', 'r')
    data = json.load(f)[0]
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
