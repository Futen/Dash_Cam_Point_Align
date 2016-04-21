import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import Info
import os
import subprocess
import moviepy.editor as mve
from multiprocessing import Pool
import SendEmail

def ExtractFrame(video_info):
    ID = video_info[0]
    info = Info.GetVideoInfo(ID)
    CutFrame = video_info[1]
    print ID,CutFrame

    f_name = Info.Config.VIDEO_SOURCE_FOLDER + '/%d.mp4'%int(ID)
    video = mve.VideoFileClip(f_name)
    end_second = (CutFrame-1)/video.fps
    start_second = end_second - 25

    command = 'ffmpeg -i %s -r 5 -qscale:v 1 -ss %f -to %f %s/'%(f_name, start_second, end_second, info['frame_path'])
    command += 'image-%5d.jpg'
    print command
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    ID_lst = Info.GetAllVideoID()
    CutFrame_lst = Info.GetAllVideoCutFrame()
    Loc_lst = Info.GetAllVideoLoc()
    arg = Info.ArgumentComprass(ID_lst, CutFrame_lst)
    #print len(ID_lst)
    #print CutFrame_lst
    #print Loc_lst
    pool = Pool(processes = 10)
    pool.map(ExtractFrame, arg)
    #ExtractFrame(arg[2])
    SendEmail.SendEmail(Text = 'ExtractFrame finish!!')
