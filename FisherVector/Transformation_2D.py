import numpy as np
import cv2
# B = A X
# X = A\B
test_src = np.array([[1,2],[3,4],[5,6]], dtype=np.float32)
test_dst = np.array([[7,5],[17,11],[27,17]], dtype=np.float32)

def GetScalarMatrix(X):
    matrix = np.zeros([2,3], dtype = np.float32)
    matrix[[0,0,0,1,1,1],[0,1,2,0,1,2]] = X
    return matrix
def GetAMatrix(point_set):
    matrix = np.zeros([6,6], dtype=np.float32)
    matrix[0,0] = point_set[0,0]
    matrix[0,1] = point_set[0,1]
    matrix[0,2] = 0
    matrix[1,3] = point_set[0,0]
    matrix[1,4] = point_set[0,1]
    matrix[1,5] = 0

    matrix[2,0] = point_set[1,0]
    matrix[2,1] = point_set[1,1]
    matrix[2,2] = 0
    matrix[3,3] = point_set[1,0]
    matrix[3,4] = point_set[1,1]
    matrix[3,5] = 0

    matrix[4,0] = point_set[2,0]
    matrix[4,1] = point_set[2,1]
    matrix[4,2] = 0
    matrix[5,3] = point_set[2,0]
    matrix[5,4] = point_set[2,1]
    matrix[5,5] = 0
    return matrix
def GetBMatrix(point_set):
    return np.hstack(point_set)
def GetTransformation(point_set_src, point_set_dst):
    A = GetAMatrix(point_set_src)
    B = GetBMatrix(point_set_dst)
    A_inv = np.linalg.pinv(A)
    X = np.dot(A_inv, B)
    return GetScalarMatrix(X)
if __name__ == '__main__':
    M = GetTransformation(test_src, test_dst)
    print M
    t = np.ones([3,3], dtype=np.float32)
    t[:,0:2] = test_src
    print test_dst
    print np.dot(M, t.T)
    a = np.array([test_src], dtype=np.float32)
    b = np.array([test_dst], dtype=np.float32)
    m = cv2.estimateRigidTransform(a, b, fullAffine=False)
    print m

