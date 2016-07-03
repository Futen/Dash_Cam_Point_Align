import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
from matplotlib import pyplot as plt
import json
import numpy as np
import os


# This code is plot the three different transformation in deep match
def LoadFile(path):
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def CheckState(ID):
    info = Info.GetVideoInfo(ID)
    deep_f = info['deep_match_path'] + '/distance_result.json'
    hog_f = info['hog_match_path'] + '/distance_result.json'
    dsift_f = info['dsift_match_path'] + '/distance_result.json'
    func = os.path.isfile
    if func(deep_f) and func(hog_f) and func(dsift_f):
        return True
    return False
def GetDeepPath(info):
    return info['deep_match_path'] + '/distance_result.json'
def GetHogPath(info):
    return info['hog_match_path'] + '/distance_result.json'
def GetDsiftPath(info):
    return info['dsift_match_path'] + '/distance_result.json'
def Plot():
    lst = Info.GetStateList(['match_result'], ['yes'])
    do_lst = []
    for one in lst:
        if CheckState(one):
            do_lst.append(one)
# Deep
    dis_data = []
    for one in do_lst:
        info = Info.GetVideoInfo(one)
        f = GetDeepPath(info)
        data = LoadFile(f)
        for key in data:
            dis_data.append(data[key])
    deep_dis_data = np.array(dis_data, dtype=np.float32)
    print 'Deep Max val : %f'%np.max(deep_dis_data)
    print 'Deep Min val : %f'%np.min(deep_dis_data)
    print 'Deep Mean val : %f'%np.mean(deep_dis_data)
    print 'Deep Standard Deviation : %f'%np.std(deep_dis_data)
    deep_max = int(np.max(dis_data))
    nop = len(deep_dis_data) 
#####
# Hog
    dis_data = []
    for one in do_lst:
        info = Info.GetVideoInfo(one)
        f = GetHogPath(info)
        data = LoadFile(f)
        for key in data:
            dis_data.append(data[key])
    hog_dis_data = np.array(dis_data, dtype=np.float32)
    print 'Hog Max val : %f'%np.max(hog_dis_data)
    print 'Hog Min val : %f'%np.min(hog_dis_data)
    print 'Hog Mean val : %f'%np.mean(hog_dis_data)
    print 'Hog Standard Deviation : %f'%np.std(hog_dis_data)
    hog_max = int(np.max(dis_data))
#####
# Dsift
    dis_data = []
    for one in do_lst:
        info = Info.GetVideoInfo(one)
        f = GetDsiftPath(info)
        data = LoadFile(f)
        for key in data:
            dis_data.append(data[key])
    dsift_dis_data = np.array(dis_data, dtype=np.float32)
    print 'Dsift Max val : %f'%np.max(dsift_dis_data)
    print 'Dsift Min val : %f'%np.min(dsift_dis_data)
    print 'Dsift Mean val : %f'%np.mean(dsift_dis_data)
    print 'Dsift Standard Deviation : %f'%np.std(dsift_dis_data)
    dsift_max = int(np.max(dis_data))
#####
    all_max = np.max([deep_max, hog_max, dsift_max])
    top_bound = int(np.ceil(all_max))
    x_axis = np.arange(0, top_bound+1)
    deep_hist = np.zeros([top_bound+1], dtype=np.float32)
    hog_hist = np.zeros([top_bound+1], dtype=np.float32)
    dsift_hist = np.zeros([top_bound+1], dtype=np.float32)
    for i in range(0, top_bound+1):
        deep_hist[i] = np.sum(deep_dis_data <= i)
        hog_hist[i] = np.sum(hog_dis_data <= i)
        dsift_hist[i] = np.sum(dsift_dis_data <= i)
    
    x_axis = x_axis[1:]
    deep_hist = deep_hist[1:]
    hog_hist = hog_hist[1:]
    dsift_hist = dsift_hist[1:]
    plt.subplot('111')
    plt.plot(x_axis, deep_hist/nop*100, 'r', color='r', linewidth='4', label = 'deep match')
    plt.plot(x_axis, hog_hist/nop*100, 'r', color='g', linewidth='4', label = 'hog match')
    plt.plot(x_axis, dsift_hist/nop*100, 'r', color='b', linewidth='4', label = 'dense sift match')
    plt.xscale('log')
    #plt.xscale('log')
    #plt.xlim([1])
    plt.xlabel('within distance(m)')
    plt.ylabel('persent(%)')
    plt.legend(loc = 'right')
    plt.savefig('match.jpg')
    plt.show()
if __name__ == '__main__':
    Plot()
