import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import numpy as np
import cv2
import subprocess
import SendEmail
from multiprocessing import Pool
import matplotlib.pyplot as plt
def optical_center(shot):
    R = cv2.Rodrigues(np.array(shot['rotation'], dtype=float))[0]
    t = shot['translation']
    a = -R.T.dot(t)
    a[0] *= -1
    #a[0] *= -1
    #t = a[0]
    #a[0] = a[1]  
    #a[1] = -t
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
        reconstruction_data.append([x, y])
        latlon_data.append([lat,lon])
    f.close()
    reconstruction_data = np.array(reconstruction_data, dtype=np.float32)
    latlon_data =  np.array(latlon_data, dtype=np.float32)

    plt.figure()
    plt.subplot('111')
    plt.plot(reconstruction_data[:,0], reconstruction_data[:,1], 'o')
    plt.show()

    return [frame_lst, reconstruction_data, latlon_data]

def RANSAC_2D(point_set1, point_set2, iteration, tolerance):
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
        #transformation[0, 1] *= -1
        #transformation[1, 0] *= -1

        print '******'
        print first_set
        print second_set
        print '******'
        #transformation[1,2] *= -1
        new_point_set1 = np.asarray([np.dot(transformation, np.transpose(np.array([x[0], x[1], 1], dtype=np.float32))) for x in point_set1], dtype=np.float32)
        distance_matrix = np.linalg.norm(new_point_set1 - point_set2, axis = 1)
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
    try:
        [M, model] = RANSAC_2D(reconstruct_set, latlon_set, iteration = 5000, tolerance = Info.Config.STEP_TEN_METER)
        print M
    except:
        return
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
    RunRANSAC('000067')
    #pool.map(RunRANSAC, do_lst)
    #SendEmail.SendEmail(Text = 'RANSAC finish!!!')
    #print do_lst
