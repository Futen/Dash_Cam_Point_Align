import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import os
from multiprocessing import Pool
import Info
import moviepy.editor as mve
import subprocess
import SendEmail
import time

def CutVideo(video_info):
    ID = video_info[0]
    CutFrame = video_info[1]
    print ID,CutFrame

    f_name = Info.Config.VIDEO_SOURCE_FOLDER + '/%d.mp4'%int(ID)
    video = mve.VideoFileClip(f_name)
    end_second = (CutFrame-1)/video.fps
    start_second = end_second - 25
    if start_second < 0:
        return False
    else:
        return True
    #print f_name
    #print os.path.isfile(f_name)

if __name__ == '__main__':
    start = time.time()
    ID_lst = Info.GetAllVideoID()
    CutFrame_lst = Info.GetAllVideoCutFrame()
    Loc_lst = Info.GetAllVideoLoc()
    Name_lst = Info.GetAllVideoName()
    #print ID_lst
    arg = Info.ArgumentComprass(ID_lst, CutFrame_lst)
    #print CutVideo(arg[40])
    '''
    output = []
    for index in range(0, len(ID_lst)):
        output.append(True)
    '''
    pool = Pool(processes = 10)
    output = pool.map(CutVideo, arg)
    f_name = Info.Config.DATA_PATH + '/list_long_enough.txt'
    f = open(f_name,'w')
    for index in range(0, len(output)):
        if output[index] == True:
            s = '%s\t%d\t%f\t%f\t%s\n'%(ID_lst[index], CutFrame_lst[index], Loc_lst[index][0], Loc_lst[index][1], Name_lst[index])
            f.write(s)
    f.close()
    SendEmail.SendEmail(Text = 'Check video finish')
