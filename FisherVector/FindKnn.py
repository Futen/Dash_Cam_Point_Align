import sys
sys.path.append('/media/external2/Dash_Cam_Point_Align')
import ReadSift
import Info
import SendEmail
import os
import numpy as np
from multiprocessing import Pool
from yael import ynumpy

def GetKnn(ID):
    info = Info.GetVideoInfo(ID)
