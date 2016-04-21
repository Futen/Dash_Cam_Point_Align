#! /usr/bin/env python

import os
import subprocess
import sys
sys.path.append('/home/Futen/Dash_Cam_2016/Google_Library')
import GoogleSV
import GetCutout
import math
import cv2
import numpy as np
import GetPanoByID
import GetCircleBound

wfov = 70
wfov = math.radians(wfov)
yaw = 0

def GetPanoID(latlon):
    return GoogleSV.getIDbyloc(lat = latlon[0], lon = latlon[1])

if __name__ == '__main__':
    #name = 'pano_nKASUC9FjDDijTyhtDLAHg.jpg' 
    
    #a = GetPanoID((25.0454202604, 121.55787478))
    #print a
    test_id = 'X8dCxQEPFLJpXnntuKRFLA'
    GetPanoByID.GetPanoByID(test_id, '.')
    '''
    GetPanoByID(a, 'tt')
    a = 'tt/pano_' + a + '.jpg'
    
    #a = 'tt/pano_MZH5QF-NIGNwNQquVjRZHg.jpg'
    CutPano(a, 'tt/tt')
    '''
