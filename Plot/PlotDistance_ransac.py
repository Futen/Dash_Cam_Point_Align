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
    number_of_point = len(our_dis)
    our_dis = np.array(our_dis, dtype = np.float32)
    print 'Ourmethod Max val : %f'%np.max(our_dis)
    print 'Ourmethod Min val : %f'%np.min(our_dis)
    print 'Ourmethod Mean val : %f'%np.mean(our_dis)
    print 'Ourmethod Standard Deviation : %f'%np.std(our_dis)
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
    print 'Affine Mean val : %f'%np.mean(affine_dis)
    print 'Affine Standard Deviation : %f'%np.std(affine_dis)
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
    print 'Rigid Mean val : %f'%np.mean(rigid_dis)
    print 'Rigid Standard Deviation : %f'%np.std(rigid_dis)
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
    
    our_max = np.max(our_Y)
    affine_max = np.max(affine_Y)
    rigid_max = np.max(rigid_Y)
    all_max = np.max([our_max, affine_max, rigid_max])
    top_bound = int(np.ceil(all_max))
    X_axis = np.arange(0, top_bound + 1)

    tmp = np.zeros([top_bound+1], dtype = np.float32)
    tmp[:] = our_max
    tmp[0:our_Y.size] = our_Y
    our_Y = tmp / number_of_point * 100
    tmp = np.zeros([top_bound+1], dtype = np.float32)
    tmp[:] = affine_max
    tmp[0:affine_Y.size] = affine_Y
    affine_Y = tmp / number_of_point * 100
    tmp = np.zeros([top_bound+1], dtype = np.float32)
    tmp[:] = rigid_max
    tmp[0:rigid_Y.size] = rigid_Y
    rigid_Y = tmp / number_of_point * 100
    
    X_axis = X_axis[1:]
    our_Y = our_Y[1:]
    affine_Y = affine_Y[1:]
    rigid_Y = rigid_Y[1:]
    fig = plt.subplot('111')
    plt.plot(X_axis, our_Y, 'r', color = 'r', linewidth = 4, label = 'ourmethod')
    plt.plot(X_axis, affine_Y, 'r', color = 'g', linewidth = 4, label = 'affine')
    plt.plot(X_axis, rigid_Y, 'r', color = 'b', linewidth = 4, label = 'rigid')
    plt.xscale('log')
    #plt.xlim([1, 300])
    plt.xlabel('within distance(m)')
    plt.ylabel('persent(%)')
    plt.legend(loc = 'right')
    plt.savefig('ransac_transform.jpg')
    plt.show()


if __name__ == '__main__':
    #print info['deep_match_path']
    #print info['hog_match_path']
    #print info['dsift_match_path']
    Plot()
