import numpy as np
import cv2
import GetTransformation

def RANSAC_myMethod(point_set_src, point_set_dst, iteration, tolerance):
    point_count = point_set_src.shape[0]
    best_inlier = 0
    best_M = None
    best_model = None
    for index in range(0, iteration):
        sample_index = np.random.choice(range(0, point_count), 3, replace=False)
        src = point_set_src[sample_index, :]
        dst = point_set_dst[sample_index, :]
        M = GetTransformation.GetTransformation(src, dst)
        new_point_set = np.asarray([np.dot(M, np.array([x[0], x[1], x[2], 1], dtype=np.float32).T) for x in point_set_src])
        distance_matrix = np.linalg.norm(new_point_set - point_set_dst, axis=1)
        inlier = np.sum(distance_matrix <= tolerance)
        #print inlier
        if inlier > best_inlier:
            best_model = new_point_set
            best_M = M
            best_inlier = inlier
    print 'best inlier: %d'%best_inlier
    print 'best ratio: %f'%(float(best_inlier)/point_count)
    return best_M, best_model

if __name__ == '__main__':
    a = [[0,0,0],[1,1,1],[2,2,2],[3,3,3]]
    b = [[5,5,5],[6,6,6],[9,9,9],[2,2,2]]
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype = np.float32)
    M,data = RANSAC_3D(a,b,10,100,1)
    print M
    print data
