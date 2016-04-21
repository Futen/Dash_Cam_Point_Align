import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import os
import subprocess
import moviepy.editor as mve
from multiprocessing import Pool
import SendEmail

def CopyConfig(ID):
    info = Info.GetVideoInfo(ID)
    command = 'cp config.yaml %s'%info['video_path']
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    ID_lst = Info.GetAllVideoID()
    #print len(ID_lst)
    #print CutFrame_lst
    #print Loc_lst
    pool = Pool(processes = 10)
    pool.map(CopyConfig, ID_lst)
    #ExtractFrame(arg[2])
    #SendEmail.SendEmail(Text = 'ExtractFrame finish!!')
