import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import ReadSift
import Info
import SendEmail
import os
import numpy as np
from multiprocessing import Pool
from yael import ynumpy

def GetKnn(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    frame_sift_lst = [x for x in sorted(os.listdir(info['frame_sift_path'])) if x.endswith('.sift')]
    pano_sift_lst = [x for x in sorted(os.listdir(info['pano_sift_path'])) if x.endswith('.sift')]
    #print pano_sift_lst
    frame_desc = []
    pano_desc = []
    for one in frame_sift_lst:
        f_name = info['frame_sift_path'] + '/' + one
        desc = ReadSift.ReadSift(f_name)[1]
        if desc.size == 0:
            desc = np.zeros((0, 128), dtype = 'uint8')
        frame_desc.append(desc)
    for one in pano_sift_lst:
        f_name = info['pano_sift_path'] + '/' + one
        desc = ReadSift.ReadSift(f_name)[1]
        if desc.size == 0:
            desc = np.zeros((0, 128), dtype = 'uint8')
        pano_desc.append(desc)
    data = np.load(Info.Config.ROOT_PATH + '/gmm_2step.npz')
    gmm = (data['a'], data['b'], data['c'])
    mean = data['mean']
    pca_transform = data['pca_transform']

    image_fvs = []
    for image_dec in (frame_desc + pano_desc):
        image_dec = np.dot(image_dec - mean, pca_transform)
        fv = ynumpy.fisher(gmm, image_dec, include = 'mu')
        image_fvs.append(fv)
    image_fvs = np.vstack(image_fvs)
    image_fvs = np.sign(image_fvs) * np.abs(image_fvs) ** 0.5
    norms = np.sqrt(np.sum(image_fvs ** 2, 1))
    image_fvs /= norms.reshape(-1,1)
    image_fvs[np.isnan(image_fvs)] = 100
    
    frame_fvs = image_fvs[0:len(frame_sift_lst)]
    pano_fvs = image_fvs[len(frame_sift_lst):]
    
    results, distances = ynumpy.knn(frame_fvs, pano_fvs, nnn = 10)
    #print results 
    #print distances
    np.save(info['pano_path'] + '/fisher_results', results)


if __name__ == '__main__':
    do_lst = Info.GetStateList(['extractsift', 'fisher'], ['yes', 'no'])
    #print do_lst
    pool = Pool(processes = 4)
    pool.map(GetKnn, do_lst)
    SendEmail.SendEmail(Text = 'Fisher Finish!!!')
