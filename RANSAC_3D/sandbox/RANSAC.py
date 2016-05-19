import numpy as np
import cv2
import Transformation as TM
import GetTransformation

# set: [[1,2,3],[4,5,6].....] should be np array
def RANSAC_3D(point_set_src, point_set_dst, tolerance, iteration, threshold):
    if len(point_set_src) != len(point_set_dst):
        print 'ransac input size error'
        exit()
    print point_set_src.shape
    #return
    length = float(point_set_src.shape[0])

    point_set_src = np.array([point_set_src[:,0], point_set_src[:,1], point_set_src[:,2]]) ####
    point_set_dst = np.array([point_set_dst[:,0], point_set_dst[:,1], point_set_dst[:,2]]) ####

    #print type(length)
    #return
    best_threshold = 0
    best_M = None
    for time in range(iteration):
        indices = sorted(np.random.choice(range(len(point_set_src)), 3, replace=False))
        #print indices
        src = point_set_src[indices]
        dst = point_set_dst[indices]
        #retval, M, inliner = cv2.estimateAffine3D(src, dst)
        #if retval == 0:
        #    continue
        M = TM.affine_matrix_from_points(src, dst)
        #print M.shape
        inlier = 0
        align_data = []
        for index,point in enumerate(point_set_src):
            '''
            homo_point = cv2.convertPointsToHomogeneous(np.reshape(point,(-1,1,3)))[0][0]
            '''
            transform = np.dot(M, point)
            #print transform.shape
            distance = np.linalg.norm(point_set_dst[index]-transform)
            align_data.append(transform)
            if distance <= tolerance:
                #print '%d    gggg'%time
                inlier += 1
        #print inlier
        ratio = inlier/length
        print ratio
        '''
        if ratio >= threshold:
            return M,align_data,ratio
        '''
        if ratio >= best_threshold:
            best_threshold = ratio
            best_M = M
    return best_threshold
def Super(point_set_src, point_set_dst, tolerance):
    length = float(point_set_src.shape[1])
    M = TM.superimposition_matrix(point_set_src, point_set_dst, scale = False)

    align_data = np.dot(M, point_set_src)[0:3,:]
    '''
    #print align_data.shape
    distance = np.sqrt(np.sum((align_data - point_set_dst[0:3])**2, axis=0))
    inliner = float(distance[distance <= tolerance].size)
    ava_dis = np.sum(distance) / length
    '''
    return 0,align_data,M
    #print M
def RANSAC_test(point_set_src, point_set_dst, iteration, tolerance):
    #point_set_src = point_set_src[0:3, :]
    #point_set_dst = point_set_dst[0:3, :]
    length = (point_set_src.shape[1])
    print length

    best_ratio = 0
    dis = 100000000000
    std = 100000000000
    for time in range(0, iteration):
        indices = sorted(np.random.choice(range(0,length), 4, replace=False))
        src = point_set_src[:, indices]
        dst = point_set_dst[:, indices]
        M = TM.affine_matrix_from_points(src[0:3,:], dst[0:3,:], shear=True, scale=True)
        #print src
        #print dst
        if np.allclose(dst, np.dot(M, src)):
            align_data = np.dot(M, point_set_src)[0:3,:]
            #print align_data.shape
            distance = np.sqrt(np.sum((align_data - point_set_dst[0:3])**2, axis=0))
            #distance = distance[distance <= 10000000]
            inliner = float(distance[distance <= tolerance].size)
            ava_dis = np.mean(distance)
            now_std = np.std(distance)
            #print inliner
            #print distance.shape
            ratio = inliner / length
            print ratio
            if ratio > best_ratio:
                std = now_std
                dis = ava_dis
                best_ratio = ratio
                best_align = align_data
                best_M = M
        
            '''        
            if ratio > best_ratio:
                best_ratio = ratio
                best_align = align_data
                best_M = M
            '''
    return best_ratio, best_align, best_M
def RANSAC_myMethod(point_set_src, point_set_dst, iteration, tolerance):
    point_count = point_set_src.shape[0]
    best_inlier = 0
    best_M = None
    best_model = None
    for index in range(0, iteration):
        sample_index = np.random.choice(range(0, point_count), 3)
        src = point_set_src[sample_index, :]
        dst = point_set_dst[sample_index, :]
        M = GetTransformation.GetTransformation(src, dst)
        new_point_set = np.asarray([np.dot(M, np.array([x[0], x[1], x[2], 1], dtype=np.float32).T) for x in point_set_src])
        distance_matrix = np.linalg.norm(new_point_set - point_set_dst, axis=1)
        inlier = np.sum(distance_matrix <= tolerance)
        print inlier
        if inlier > best_inlier:
            best_model = new_point_set
            best_M = M
            best_inlier = inlier
    return best_M, best_model

if __name__ == '__main__':
    a = [[0,0,0],[1,1,1],[2,2,2],[3,3,3]]
    b = [[5,5,5],[6,6,6],[9,9,9],[2,2,2]]
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype = np.float32)
    M,data = RANSAC_3D(a,b,10,100,1)
    print M
    print data
