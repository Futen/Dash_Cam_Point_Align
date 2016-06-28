import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import numpy as np
import cv2
import subprocess
import SendEmail
from multiprocessing import Pool
import Transformation_2D  as T2D

def optical_center(shot):
    R = cv2.Rodrigues(np.array(shot['rotation'], dtype=float))[0]
    t = shot['translation']
    a = -R.T.dot(t)
    #a[1] *= -1
    return a

def GetPointData(info):
    reconstruction = Info.ReadReconstructionData(info)['shots']
    reconstruction_data = []
    latlon_data = []
    frame_lst = []
    f = open(Info.GetMatchLstFileName(info), 'r')
    for line in f:
        line = line[0:-1].split('\t')
        frame_name = line[0]
        pano_name = line[1]
        try:
            [x, y, z] = optical_center(reconstruction[frame_name])
        except:
            continue
        lat = float(line[2])
        lon = float(line[3])
        frame_lst.append(line[0])
        reconstruction_data.append([y, x])
        latlon_data.append([lat,lon])
    f.close()
    reconstruction_data = np.array(reconstruction_data, dtype=np.float32)
    latlon_data =  np.array(latlon_data, dtype=np.float32)
    return [frame_lst, reconstruction_data, latlon_data]

def RANSAC_2D(point_set1, point_set2, iteration, tolerance):
    x_mean = np.mean(point_set2[:,0])
    y_mean = np.mean(point_set2[:,1])
    print x_mean
    print y_mean
    point_count = point_set1.shape[0]
    best_M = None
    best_inlier = 0
    best_model = None
    for i in range(0, iteration):
        sample_index = np.random.choice(range(0, point_count), 3, replace = False)
        first_set = np.array([point_set1[sample_index]], dtype = np.float32)
        second_set = np.array([point_set2[sample_index]], dtype = np.float32)
        #print first_set.shape
        transformation = cv2.estimateRigidTransform(first_set, second_set, fullAffine = False)
        if transformation is None:
            continue
        #print '******'
        #print first_set
        #print second_set
        #print '******'
        #transformation[1,2] *= -1
        new_point_set1 = np.asarray([T2D.Mirror(transformation, x, x_mean, y_mean) for x in point_set1], dtype=np.float32)
        distance_matrix = np.linalg.norm(new_point_set1 - point_set2, axis = 1)
        #print distance_matrix
        inlier = np.sum(distance_matrix <= tolerance)
        #print inlier
        if inlier > best_inlier:
            best_inlier = inlier
            best_M = transformation
            best_model = new_point_set1
    print best_inlier
    print np.linalg.pinv(best_M[:, 0:2])
    return best_M, best_model

def RunRANSAC(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    subprocess.call('rm %s'%(Info.GetGCPFileName(info)), shell=True)
    [frame_lst, reconstruct_set, latlon_set] = GetPointData(info)
    if len(reconstruct_set) == 0 or len(latlon_set) == 0:
        return
    #try:
    [M, model] = RANSAC_2D(reconstruct_set, latlon_set, iteration = 1000, tolerance = Info.Config.STEP_TEN_METER)
    print M
    #except:
    #    return
    if not M is None and not model is None:
        reconstruct = Info.ReadReconstructionData(info)['shots']
        f = open(Info.GetGCPFileName(info), 'w')
        frame_lst = sorted(reconstruct.keys())
        for index, frame in enumerate(frame_lst):
            [x, y, z] = optical_center(reconstruct[frame])
            point = np.dot(M, np.transpose(np.array([x, y, 1], dtype=np.float32)))
            s = '%s\t%f\t%f\n'%(frame, point[0], point[1])
            f.write(s)
        f.close()

if __name__ == '__main__':
    do_lst = Info.GetStateList(['matchLst'], ['yes'])
    #pool = Pool(processes = 8)
    RunRANSAC('001234')
    #pool.map(RunRANSAC, do_lst)
    #SendEmail.SendEmail(Text = 'RANSAC finish!!!')
    #print do_lst
