import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import os
import subprocess
import moviepy.editor as mve
from multiprocessing import Pool
import SendEmail

def RunMatch(ID):
    info = Info.GetVideoInfo(ID)
    command = '%s %s'%(Info.Config.OPENSFM_RUN_MATCH, info['video_path'])
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    ID_lst = Info.GetAllVideoID()
    #RunMatch(ID_lst[0])
    pool = Pool(processes = 1)
    pool.map(RunMatch, ID_lst)
    SendEmail.SendEmail(Text = 'RunMatch Finish!!!')
