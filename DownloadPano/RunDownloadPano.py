import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import os
import PanoProcess 
import time
import SendEmail
from multiprocessing import Pool

def DownloadPano(ID):
    info = Info.GetVideoInfo(ID)
    print ID
    circle = PanoProcess.GetCircleBound.GetCircleBound(info['location'])
    #print circle
    id_lst = []
    start_time = time.time()
    for loc in circle:
        #print loc
        try:
            panoid = PanoProcess.GetPanoID(loc)
        except:
            continue
        if panoid != None and not panoid in id_lst:
            id_lst.append(panoid)
            #a = time.time()
            PanoProcess.GetPanoByID.GetPanoByID(panoid, info['pano_download_path'])
            #print time.time() - a
    pano_lst = [x for x in sorted(os.listdir(info['pano_download_path'])) if x.endswith('.jpg')]
    f_name = '%s/pano_lst.txt'%info['pano_path']
    f = open(f_name, 'w')
    for img_name in pano_lst:
        s = img_name + '\n'
        f.write(s)
    f.close()
    end = time.time()
    print '%s use %f minutes and total %d images'%(ID, (end-start_time)/60, len(id_lst))

if __name__ == '__main__':
    #DownloadPano('000006')
    do_lst = Info.GetStateList(['reconstruction', 'downloadpano'], ['yes', 'no'])
    print 'Total %d videos to download'%len(do_lst)
    #do_lst = Info.GetAllVideoID()
    #DownloadPano('000006')
    pool = Pool(processes = 2)
    pool.map(DownloadPano, do_lst)
    SendEmail.SendEmail(Text = 'Downlaod finish')
