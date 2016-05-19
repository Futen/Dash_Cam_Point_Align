import numpy as np
import RANSAC
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import RouteShow


def optical_center(shot):
    R = cv2.Rodrigues(np.array(shot['rotation'], dtype=float32))[0]
    t = shot['translation']
    return -R.T.dot(t)


data = np.load('result.npy')
#data2 = data[1]
#data[0] = data[0][np.abs(data[1]) <= 3000] 
#data[1] = data[1][np.abs(data[1]) <= 3000]
#data2 = data[1]

M, align_data = RANSAC.RANSAC_myMethod(data[0], data[1], 10000, 3)
print M
#ratio, align_data, M = RANSAC.Super(data[0], data[1], 0)

fig = plt.figure()
ax = fig.gca(projection='3d')
#align_data = data[0]    ###############3
ax.scatter(align_data[:,0], align_data[:,1], align_data[:,2], c = 'r', label='gg')
data2 = data[1]
#data2[np.abs(data2) > 3000] = 0
#print data2
ax.scatter(data2[:,0], data2[:,1], data2[:,2], c = 'b', label='kk')
tmp = RouteShow.RouteShow('reconstruction.json')
tmp = np.dot(M, tmp)[0:3,:]
x = tmp[0,:]
y = tmp[1,:]
z = tmp[2,:]
ax.scatter(x,y,z, c='g')
ax.legend()
plt.show()

'''
fig = plt.figure()
ax = fig.gca(projection='3d')
data2 = data[1]
ax.scatter(data2[0,:], data2[1,:], data2[2,:], c = 'b', label='kk')
plt.show()
'''
