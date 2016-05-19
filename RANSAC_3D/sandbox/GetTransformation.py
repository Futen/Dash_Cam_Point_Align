import numpy as np
import cv2
import time

# B = A X
# X = A\B
test_src_set = np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=np.float32)
test_dst_set = np.array([[14,23,32],[41,55,60],[70,89,93]], dtype=np.float32)
#test_dst_set = test_src_set + 5
def GetScalarMatrix(X):
    matrix = np.zeros([3,4], dtype = np.float32)
    matrix[[0,0,1,1,2,0,1,2],[0,1,0,1,2,3,3,3]] = X
    return matrix
def GetAMatrix(point_set):
    '''
    [1,2,3]
    [4,5,6]
    [7,8,9]
    '''
    matrix = np.zeros([9, 8], dtype=np.float32)
    matrix[0,0] = point_set[0,0]
    matrix[0,1] = point_set[0,1]
    matrix[1,2] = point_set[0,0]
    matrix[1,3] = point_set[0,1]
    matrix[2,4] = point_set[0,2]
    matrix[0,5] = 1
    matrix[1,6] = 1
    matrix[2,7] = 1
    
    matrix[3,0] = point_set[1,0]
    matrix[3,1] = point_set[1,1]
    matrix[4,2] = point_set[1,0]
    matrix[4,3] = point_set[1,1]
    matrix[5,4] = point_set[1,2]
    matrix[3,5] = 1
    matrix[4,6] = 1
    matrix[5,7] = 1

    matrix[6,0] = point_set[2,0]
    matrix[6,1] = point_set[2,1]
    matrix[7,2] = point_set[2,0]
    matrix[7,3] = point_set[2,1]
    matrix[8,4] = point_set[2,2]
    matrix[6,5] = 1
    matrix[7,6] = 1
    matrix[8,7] = 1
    return matrix
def GetBMatrix(point_set):
    return np.hstack(point_set)
def GetTransformation(point_set_src, point_set_dst):
    A = GetAMatrix(point_set_src)
    B = GetBMatrix(point_set_dst)
    A_inv = np.linalg.pinv(A)
    X = np.dot(A_inv, B)
    #print X
    return GetScalarMatrix(X)

if __name__ == '__main__':
    s = time.time()
    X = GetTransformation(test_src_set, test_dst_set)
    print 'Test_dst'
    print test_dst_set
    for point in test_src_set:
        print np.dot(X, np.array([point[0], point[1], point[2], 1], dtype = np.float32).T)
    #print (time.time() - s)*10000
