import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import os
import subprocess
import moviepy.editor as mve
from multiprocessing import Pool
import SendEmail

def RunReconstruct(ID):
    info = Info.GetVideoInfo(ID)
    command = '%s %s'%(Info.Config.OPENSFM_RECONSTRUCT, info['video_path'])
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    ID_lst = Info.GetAllVideoID()
    #RunReconstruct(ID_lst[0])
    pool = Pool(processes = 10)
    pool.map(RunReconstruct, ID_lst)
    SendEmail.SendEmail(Text = 'Reconstruct finish!!!!!')
