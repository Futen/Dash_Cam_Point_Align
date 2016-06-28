import numpy as np
import cv2
from geopy.distance import VincentyDistance as VD
# B = A X
# X = A\B
test_src = np.array([[-9.6522398,-137.97637939],[7.1731391,-43.4574585],[-6.85418129,-110.25995636]], dtype=np.float32)
test_dst = np.array([[25.00469589,121.49633026],[25.00494576,121.49611664],[25.00469589,121.49623108]], dtype=np.float32)

def GetScalarMatrix(X):
    matrix = np.zeros([2,3], dtype = np.float32)
    matrix[[0,0,0,1,1,1],[0,1,2,0,1,2]] = X
    return matrix
def GetAMatrix(point_set):
    matrix = np.zeros([6,6], dtype=np.float32)
    matrix[0,0] = point_set[0,0]
    matrix[0,1] = point_set[0,1]
    matrix[0,2] = 1
    matrix[1,3] = point_set[0,0]
    matrix[1,4] = point_set[0,1]
    matrix[1,5] = 1

    matrix[2,0] = point_set[1,0]
    matrix[2,1] = point_set[1,1]
    matrix[2,2] = 1
    matrix[3,3] = point_set[1,0]
    matrix[3,4] = point_set[1,1]
    matrix[3,5] = 1

    matrix[4,0] = point_set[2,0]
    matrix[4,1] = point_set[2,1]
    matrix[4,2] = 1
    matrix[5,3] = point_set[2,0]
    matrix[5,4] = point_set[2,1]
    matrix[5,5] = 1
    return matrix
def GetBMatrix(point_set):
    return np.hstack(point_set)
def GetTransformation(point_set_src, point_set_dst):
    A = GetAMatrix(point_set_src)
    B = GetBMatrix(point_set_dst)
    A_inv = np.linalg.pinv(A)
    X = np.dot(A_inv, B)
    return GetScalarMatrix(X)
def Mirror(M, X, mid_num, mid_num2): # [R|T] x X
    # [R|T] x X
    # RX + T
    # R(X + R'T)
    R = M[:, 0:2]
    T = M[:, 2]
    R_inv = np.linalg.pinv(R)
    ori_point = X + np.dot(R_inv, T)
    print ori_point
    #if ori_point[0] > mid_num:
    #    ori_point[0] -= 2 * np.abs(ori_point[0] - mid_num)
    #else:
    #    ori_point[0] += 2 * np.abs(ori_point[0] - mid_num)
    #if ori_point[1] > mid_num2:
    #    ori_point[1] -= 2 * np.abs(ori_point[1] - mid_num2)
    #else:
    #    ori_point[1] += 2 * np.abs(ori_point[1] - mid_num2)

    return np.dot(R, ori_point)
    
if __name__ == '__main__':
    M = GetTransformation(test_src, test_dst)
    #print M
    t = np.ones([3,3], dtype=np.float32)
    t[:,0:2] = test_src
    #print test_dst
    #print M
    #print t
    g = np.dot(M, t.T).T
    a = np.reshape(test_src,[1,3,2])
    b = np.reshape(test_dst,[1,3,2])
    #print a
    m = cv2.estimateRigidTransform(a, b, fullAffine=False)
    #print m
    t = np.ones([3,3], dtype=np.float32)
    t[:,0:2] = test_src
    gg = np.dot(m, t.T).T

    print VD(g[0], gg[0]).km*1000
    print VD(g[1], gg[1]).km*1000
    print VD(g[2], gg[2]).km*1000

