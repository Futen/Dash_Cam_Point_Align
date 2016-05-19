import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import Info
import GoogleSV
import numpy as np
import os
from multiprocessing import Pool

THRESHOLD = 60
RATIO = 1.3

def GetResultLst(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    frame_sift_lst = [x for x in sorted(os.listdir(info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir(info['pano_sift_path'])) if x.endswith('.sift')]
    fisher_result = np.load(Info.GetFisherResultFileName(info))
    match_score = np.load(Info.GetMatchFunMFileName(info))
    #print match_score
    f = open(Info.GetMatchLstFileName(info), 'w')
    for frame_index, frame_sift_name in enumerate(frame_sift_lst):
        arg_sort_index = np.argsort(match_score[frame_index, :])
        highest_index = arg_sort_index[-1]
        highest_score = match_score[frame_index, highest_index]
        second_index = arg_sort_index[-2]
        second_score = match_score[frame_index, second_index]

        ratio = float(highest_score) / float(second_score)
        if highest_score >= THRESHOLD:
            frame_name = frame_sift_name.split('.')[0] + '.jpg'
            pano_sift_name = pano_sift_lst[fisher_result[frame_index, highest_index]]
            pano_name = pano_sift_name.split('.')[0] + '.jpg'
            pano_id = pano_name[5:27]
            #print pano_id
            loc = GoogleSV.getLocationbyID(pano_id)
            s = '%s\t%s\t%s\t%s\t%d\n'%(frame_name, pano_name, loc[0], loc[1], highest_score)
            f.write(s)
    f.close()
if __name__ == '__main__':
    do_lst = Info.GetStateList(['matchFunM'], ['yes'])
    #GetResultLst('000209')#000538
    pool = Pool(processes = 2)
    pool.map(GetResultLst, do_lst)
