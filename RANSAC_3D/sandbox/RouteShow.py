#! /usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import cv2

def optical_center(shot):
    R = cv2.Rodrigues(np.array(shot['rotation'], dtype=float))[0]
    t = shot['translation']
    return -R.T.dot(t)

def RouteShow(name):
    f = open(name, "r")
    obj = json.load(f)
    f.close()
    name_lst = []
    index = 1
    obj = obj[0]
    x_lst = []
    y_lst = []
    z_lst = []
    max_val = 0
    min_val = 0
    x_total = 0
    y_total = 0
    z_total = 0
    h_lst = []
    for index,key in enumerate(obj['shots']):
        #name = 'image-%.5d.jpg'%index
        name = key
        try:
            output = optical_center(obj['shots'][name])
            x_lst.append(output[0])
            y_lst.append(output[1])
            z_lst.append(output[2])
            h_lst.append(1)
            x_total+=output[0]
            y_total+=output[1]
            z_total+=output[2]
            if max(output) > max_val:
                max_val = max(output)
            if min(output) < min_val:
                min_val = min(output)        
        except KeyError:
            print index
            pass
        index+=1
    return np.array([x_lst, y_lst, z_lst, h_lst], dtype=np.float32)
    '''
    x_p_lst = []
    y_p_lst = []
    z_p_lst = []
    color_lst = []
    for index,key in enumerate(obj['points']):
        try:
            point = obj['points'][key]['coordinates']
            if point[0] > 5000 or point[1] > 5000 or point[2] > 5000:
                continue
            x_p_lst.append(round(float(point[0])))
            y_p_lst.append(round(float(point[1])))
            z_p_lst.append(round(float(point[2])))
            color_lst.append('red')
            if max(output) > max_val:
                max_val = max(output)
            if min(output) < min_val:
                min_val = min(output) 
        except:
            print key
            pass
    '''
    fig = plt.figure() # creat a new figure
    ax = fig.gca(projection='3d',label='...') # get current figure instance
    ax.scatter(x_lst, y_lst, z_lst, label='...')
    #ax.scatter(x_p_lst,y_p_lst,z_p_lst,s=1,color=color_lst,)
    
    x_ava = x_total/len(obj['shots'])
    y_ava = y_total/len(obj['shots'])
    z_ava = z_total/len(obj['shots'])

    print np.shape(x_lst)
    x_lst = np.linspace(min_val, max_val, 100)
    y_lst = []
    z_lst = []
    for i in range(0,100):
        y_lst.append(y_ava)
        z_lst.append(z_ava)
    ax.scatter(x_lst, y_lst, z_lst, s=1,c='r',label='...')
    x_lst = []
    y_lst = np.linspace(min_val, max_val, 100)
    z_lst = []
    for i in range(0,100):
        x_lst.append(x_ava)
        z_lst.append(z_ava)
    ax.scatter(x_lst, y_lst, z_lst, s=1,c='r', label='...')
    x_lst = []
    y_lst = []
    z_lst = np.linspace(min_val, max_val, 100)
    for i in range(0,100):
        x_lst.append(x_ava)
        y_lst.append(y_ava)
    ax.scatter(x_lst, y_lst, z_lst, s=1,c='r', label='...')
    ax.legend()
    plt.show()

if __name__ == '__main__':
    RouteShow(sys.argv[1])
