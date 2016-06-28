import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import Info
import GoogleSV as GSV
from multiprocessing import Pool
import json
from collections import OrderedDict

name = 'lat_lon_result.json'

def Merge(ID):
    print ID
    info = Info.GetVideoInfo(ID)
    f_name  = info['match_path'] + '/' + name
    f = open(f_name, 'r')
    data = json.load(f)
    f.close()
    key_lst = sorted(data.keys())
    pano_lst = []
    for key in key_lst:
        loc = data[key]
        print key
        try:
            panoid = GSV.getIDbyloc(lat = loc[0], lon = loc[1])
        except:
            data.pop(key)
            continue
        #print panoid
        if panoid is None:
            data.pop(key)
            continue
        elif not panoid in pano_lst:
            pano_lst.append(panoid)
            try:
                loc = GSV.getLocationbyID(panoid)
                data[key] = [float(loc[0]), float(loc[1])]
            except:
                data.pop(key)
                continue
        else:
            data.pop(key)
    f = open(info['match_path'] + '/google_info.json', 'w')
    f.write(json.dumps(data, indent=4))
    f.close()

if __name__ == '__main__':
    do_lst = Info.GetStateList(['lat_lon'], ['yes'])
    #print do_lst
    #print len(do_lst)
    Merge('000049')
