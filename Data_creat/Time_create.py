import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import os
from multiprocessing import Pool
import Info
import moviepy.editor as mve
import subprocess
import SendEmail
import time
import json
from collections import OrderedDict


def GetVideoTime(video_info):
    ID = video_info[0][0]
    CutFrame = video_info[0][1]
    Name = video_info[1]
    print ID,CutFrame
    info = Info.GetVideoInfo(ID)
    f_name = Info.Config.VIDEO_SOURCE_FOLDER + '/%d.mp4'%int(ID)
    video = mve.VideoFileClip(f_name)
    end_second = (CutFrame-1)/video.fps
    start_second = end_second - 25
    frame_lst = [x for x in sorted(os.listdir(info['frame_path'])) if x.endswith('.jpg')]
    if start_second >= 0:
        f = open('%s/timeline.json'%info['match_path'] , 'w')
        t = start_second
        inter = 0.2 # 0.25 s
        d = {}
        d['time'] = {}
        for i in frame_lst:
            #print i
            d['time'][i] = t
            t += inter
        d['time'] = OrderedDict(sorted(d['time'].items()))
        d['id'] = Name
        f.write(json.dumps(d, indent=4) + '\n')
        f.close()
        return False
    else:
        return True
    #print f_name
    #print os.path.isfile(f_name)

if __name__ == '__main__':
    ID_lst = Info.GetAllVideoID()
    CutFrame_lst = Info.GetAllVideoCutFrame()
    Name_lst = Info.GetAllVideoName()
    arg = Info.ArgumentComprass(ID_lst, CutFrame_lst)
    arg = Info.ArgumentComprass(arg, Name_lst)
    #print arg
    #GetVideoTime(arg[0])
    for one in arg:
        if one[0][0] == '000067':
            print one
            GetVideoTime(one)
    '''
    for one in arg:
        try:
            GetVideoTime(one)
        except:
            pass
    '''
