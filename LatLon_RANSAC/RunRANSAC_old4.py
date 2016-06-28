import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import numpy as np
import cv2
import subprocess
import SendEmail
import Transformation_2D as T2D
from multiprocessing import Pool
def optical_center(shot):
    R = cv2.Rodrigues(np.array(shot['rotation'], dtype=float))[0]
    t = shot['translation']
    return -R.T.dot(t)

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
        reconstruction_data.append([x, y])
        latlon_data.append([lat,lon])
    f.close()
    reconstruction_data = np.array(reconstruction_data, dtype=np.float32)
    latlon_data =  np.array(latlon_data, dtype=np.float32)
    return [frame_lst, reconstruction_data, latlon_data]

def RANSAC_2D(point_set1, point_set2, iteration, tolerance):
    #print point_set1.shape
    #print point_set2.shape
    point_count = point_set1.shape[0]
    best_M = None
    best_inlier = 0
    best_model = None
    for i in range(0, iteration):
        sample_index = np.random.choice(range(0, point_count), 3, replace = False)
        first_set = point_set1[sample_index]
        second_set = point_set2[sample_index]
        #print first_set
        #print second_set
        transformation = T2D.GetTransformation(first_set, second_set)
        #print transformation
        if transformation is None:
            continue
        #transformation[1,2] *= -1
        new_point_set1 = [np.dot(transformation, np.array([x[0], x[1], 1]).T) for x in point_set1]
        print '******'
        print np.asarray([np.dot(transformation, np.array([x[0], x[1], 1]).T) for x in first_set])
        print second_set
        print '******'
        distance_matrix = np.linalg.norm(new_point_set1 - point_set2, axis = 1)
        #print distance_matrix
        inlier = np.sum(distance_matrix <= tolerance)
        #print inlier
        if inlier > best_inlier:
            best_inlier = inlier
            best_M = transformation
            best_model = new_point_set1
    print best_inlier
    return best_M, best_model

def RunRANSAC(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    subprocess.call('rm %s'%(Info.GetGCPFileName(info)), shell=True)
    [frame_lst, reconstruct_set, latlon_set] = GetPointData(info)
    if len(reconstruct_set) == 0 or len(latlon_set) == 0:
        return
    #try:
    [M, model] = RANSAC_2D(reconstruct_set, latlon_set, iteration = 5000, tolerance = Info.Config.STEP_TEN_METER/5)
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
