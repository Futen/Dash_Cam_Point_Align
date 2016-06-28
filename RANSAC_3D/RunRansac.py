import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import RansacPointExtract as RPE
import RANSAC
import numpy as np
import json
import cv2
from multiprocessing import Pool
import SendEmail

def optical_center(shot):
    R = cv2.Rodrigues(np.array(shot['rotation'], dtype=float))[0]
    t = shot['translation']
    return -R.T.dot(t)
def RunExtract(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    RPE.RansacPointExtract(ID)
def RunRansac(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    data = np.load(Info.GetMatchResultExtractPointFileName(info))
    #data2 = data[1]
    #data[0] = data[0][np.abs(data[1]) <= 3000] 
    #data[1] = data[1][np.abs(data[1]) <= 3000]
    #data2 = data[1i]
    try:
        M, align_data = RANSAC.RANSAC_affine(data[0], data[1], 10000, 5)
    except:
        return
    if M is None:
        return
    print M
    #print np.reshape(M, [12])
    try:
        M = np.reshape(M, [12]).astype(float)
    except:
        return
    gcp = Info.ReadGCPData(info)
    data = Info.ReadReconstructionData(info)
    trajectory = {}
    for shot in data['shots']:
        [x, y, z] = optical_center(data['shots'][shot])
        trajectory[shot] = [x, y, z]
    data['gcp'] = gcp
    #print gcp
    data['transformation'] = list(M)
    #print type(M[0])
    data['trajectory'] = trajectory
    #print trajectory
    f_name = Info.Get3DRansacFileName(info)
    f = open(f_name, 'w')
    f.write(json.dumps(data, indent=4))
    f.close()
    print '%s ransac finish'%ID


if __name__ == '__main__':
    do_lst = Info.GetStateList(['ransac_2D','match_result'], ['yes', 'yes'])
    print do_lst
    print len(do_lst)
    pool= Pool(processes = 8)
    #pool.map(RPE.RansacPointExtract, do_lst)
    #for one in do_lst:
    #RunRansac(one)
    pool.map(RunRansac, do_lst)
    SendEmail.SendEmail()
    #RunExtract('000791')
    #RunRansac('000363')
