#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import SystemParameter as SP
import subprocess
import os

TYPE = 'pos'

def GetImageList(DIR):
    lst = [x for x in sorted(os.listdir(DIR)) if x.endswith('.jpg')]
    f = open('%s/list.txt'%DIR,'w')
    for one in lst:
        f.write(one + '\n')
    f.close()
def GetSiftList(DIR, OUTPUT_NAME): #output_name is output_dir + name
    lst = [x for x in sorted(os.listdir(DIR)) if x.endswith('.sift')]
    f = open('%s'%OUTPUT_NAME, 'w')
    for one in lst:
        f.write(one + '\n')
    f.close()
def ExtractSift(v_name):
    info = SP.GetPath(v_name, TYPE)
    if TYPE == 'pos':
    elif TYPE == 'neg':
    elif TYPE == 'NegSource':
