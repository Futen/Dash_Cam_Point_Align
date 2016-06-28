import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import Info
import subprocess
import GoogleSV as GSV
import os

def Label(ID):
    info = Info.GetVideoInfo(ID)
    frame_lst = [x for x in sorted(os.listdir(info['frame_path'])) if x.endswith]
    i = 0
    f = open(Info.GetMatchLstFileName(info), 'w')
    while True:
        f_name = info['frame_path'] + '/' + frame_lst[i]
        command = 'eog %s'%f_name
        subprocess.call(command, shell=True)
        panoid = raw_input('Pano ID : ')
        loc = GSV.getLocationbyID(panoid)
        print loc
        s = '%s\t%s\t%s\t%s\n'%(frame_lst[i], panoid, loc[0], loc[1])
        f.write(s)
        i += 10
        if i >= 125:
            f.close()
            return
    f.close()
if __name__ == '__main__':
    Label('000067')
