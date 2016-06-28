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
import subprocess
import SendEmail
def Merge(ID):
    info = Info.GetVideoInfo(ID)
    f1_name = Info.Get3DRansacFileName(info)
    subprocess.call('cp %s %s/ransac_3D_result_old.json'%(f1_name, info['match_path']), shell=True)
    f2_name = info['match_path'] + '/timeline.json'
    f1 = open(f1_name, 'r')
    f2 = open(f2_name, 'r')
    data = json.load(f1)
    tim = json.load(f2)
    data['id'] = tim['id']
    data['time'] = tim['time']
    f1.close()
    f2.close()
    f1 = open(f1_name, 'w')
    f1.write(json.dumps(data, indent=4))
    f1.close()

if __name__ == '__main__':
    #Merge('000049')
    do_lst = Info.GetStateList(['ransac_3D'], ['yes'])
    print (do_lst)
    pool = Pool(processes = 4)
    pool.map(Merge, do_lst)
    
