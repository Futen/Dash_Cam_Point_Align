import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import lib_SIFTmatch
import ReadSift
import Info
import SendEmail
import os
import numpy as np
from multiprocessing import Pool

def MatchFunM(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    frame_sift_lst = [x for x in sorted(os.listdir(info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir(info['pano_sift_path'])) if x.endswith('.sift')]

    results = np.load('%s/fisher_results.npy'%info['pano_path'])
    MM = []
    for index, name in enumerate(frame_sift_lst):
        Mi = []
        frame_short_name = name.split('.')[0]
        for i in range(0,results.shape[1]):
            pano_name = pano_sift_lst[results[index, i]]
            pano_short_name = pano_name.split('.')[0]
            kp_pairs = lib_SIFTmatch.flann_match('%s/%s'%(info['frame_sift_path'],frame_short_name),
                                                 '%s/%s'%(info['pano_sift_path'],pano_short_name))
            try:
                (mkp1, mkp2) = zip(*kp_pairs)
                mkp1_pts = [ (x[0],x[1]) for x in mkp1 ]
                mkp2_pts = [ (x[0],x[1]) for x in mkp2 ]
                mkp1_pts = np.float32(mkp1_pts)
                mkp2_pts = np.float32(mkp2_pts)
                F, mask = cv2.findFundamentalMat(mkp1_pts,mkp2_pts,cv2.FM_RANSAC,20)
                q_pts = mkp1_pts[mask.ravel()==1]
                t_pts = mkp2_pts[mask.ravel()==1]
                Mi.append(len(q_pts))
            except:
                Mi.append(0)
                continue
        MM.append(Mi)
    np.save('%s/results_fundM'%info['pano_path'],MM)    

if __name__ == '__main__':
    do_lst = Info.GetStateList(['fisher', 'matchFunM'], ['yes', 'no'])
    #print do_lst
    #MatchFunM(do_lst[0])
    pool = Pool(processes = 8)
    pool.map(MatchFunM, do_lst)
    SendEmail.SendEmail(Text = 'Match Finish')
