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
    rigid_f = info['deep_match_path'] + '/rigid_distance_result.json'
    affine_f = info['deep_match_path'] + '/affine_distance_result.json'
    ourmethod_f = info['deep_match_path'] + '/distance_result.json'
    func = os.path.isfile
    if func(rigid_f) and func(affine_f) and func(ourmethod_f):
        return True
    return False
def GetOurPath(info):
    return info['deep_match_path'] + '/distance_result.json'
def GetAffinePath(info):
    return info['deep_match_path'] + '/affine_distance_result.json'
def GetRigidPath(info):
    return info['deep_match_path'] + '/rigid_distance_result.json'
def Plot():
    lst = Info.GetStateList(['match_result'], ['yes'])
    do_lst = [x for x in lst if CheckState(x)]
    #print len(do_lst)
# our
    our_dis = []
    for one in do_lst:
        info = Info.GetVideoInfo(one)
        f = GetOurPath(info)
        data = LoadFile(f)
        for key in data:
            our_dis.append(data[key])
    our_dis = np.array(our_dis, dtype = np.float32)
    print 'Ourmethod Max val : %f'%np.max(our_dis)
    print 'Ourmethod Min val : %f'%np.min(our_dis)
    top_bound = np.ceil(np.max(our_dis))
    #print top_bound
    histogram = np.zeros([int(top_bound)+1], dtype=np.float32)
    ceil_data = np.ceil(our_dis)
    for i in range(0, int(top_bound) + 1):
        count = np.sum(ceil_data <= i)
        histogram[i] = count
    #print histogram
    our_Y = histogram
    our_X = np.arange(0, top_bound+1)
# affine
    affine_dis = []
    for one in do_lst:
        info = Info.GetVideoInfo(one)
        f = GetAffinePath(info)
        data = LoadFile(f)
        for key in data:
            affine_dis.append(data[key])
    affine_dis = np.array(affine_dis, dtype = np.float32)
    print 'Affine Max val : %f'%np.max(affine_dis)
    print 'Affine Min val : %f'%np.min(affine_dis)
    top_bound = np.ceil(np.max(affine_dis))
    #print top_bound
    histogram = np.zeros([int(top_bound)+1], dtype=np.float32)
    ceil_data = np.ceil(affine_dis)
    for i in range(0, int(top_bound) + 1):
        count = np.sum(ceil_data <= i)
        histogram[i] = count
    #print histogram
    affine_Y = histogram
    affine_X = np.arange(0, top_bound+1)
# rigid
    rigid_dis = []
    for one in do_lst:
        info = Info.GetVideoInfo(one)
        f = GetRigidPath(info)
        data = LoadFile(f)
        for key in data:
            rigid_dis.append(data[key])
    rigid_dis = np.array(rigid_dis, dtype = np.float32)
    print 'Rigid Max val : %f'%np.max(rigid_dis)
    print 'Rigid Min val : %f'%np.min(rigid_dis)
    top_bound = np.ceil(np.max(rigid_dis))
    #print top_bound
    histogram = np.zeros([int(top_bound)+1], dtype=np.float32)
    ceil_data = np.ceil(rigid_dis)
    for i in range(0, int(top_bound) + 1):
        count = np.sum(ceil_data <= i)
        histogram[i] = count
    #print histogram
    rigid_Y = histogram
    rigid_X = np.arange(0, top_bound+1)

    plt.subplot('111')
    plt.plot(our_X, our_Y, 'r', color = 'r', label = 'ourmethod')
    plt.plot(affine_X, affine_Y, 'r', color = 'g', label = 'affine')
    plt.plot(rigid_X, rigid_Y, 'r', color = 'b', label = 'rigid')
    plt.xlabel('within distance(m)')
    plt.ylabel('number of point')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    #print info['deep_match_path']
    #print info['hog_match_path']
    #print info['dsift_match_path']
    Plot()
