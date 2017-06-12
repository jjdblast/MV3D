import ctypes
import numpy as np
import matplotlib.pyplot as plt
import math
#import time

x_MIN = -45#0.0
x_MAX = 45#40.0
y_MIN =-10#-20.0
y_MAX =10# 20.0
z_MIN =-3# -0.4
z_MAX =1.0# 2
x_DIVISION = 0.2#0.1
y_DIVISION = 0.2#0.1
z_DIVISION = 0.5#0.3          #was 0.2 originally

x_MIN = -20#0.0
x_MAX = 20#40.0
y_MIN =-20#-20.0
y_MAX =20# 20.0
z_MIN =-2# -0.4
z_MAX =0.4# 2
x_DIVISION = 0.1#0.1
y_DIVISION = 0.1#0.1
z_DIVISION = 0.4#0.3          #was 0.2 originally

X_SIZE = int(math.floor((x_MAX-x_MIN)/x_DIVISION))  #400
Y_SIZE = int(math.floor((y_MAX-y_MIN)/y_DIVISION)) #400
Z_SIZE = int(math.floor((z_MAX-z_MIN)/z_DIVISION))   # 6

print('Image Size X_SIZE, Y_SIZE, Z_SIZE : '+ str(X_SIZE)+ ", " + str(Y_SIZE) + ", " +str(Z_SIZE))
print ('LiDAR data pre-processing starting...')

# initialize an np 3D array with 1's
indata = np.ones((X_SIZE, Y_SIZE, Z_SIZE+2), dtype = np.double)

# create a handle to LidarPreprocess.c
SharedLib = ctypes.cdll.LoadLibrary('./LidarPreprocess.so')

# CHANGE LIDAR DATA DIR HERE !!!!
lidar_data_src_dir = "../../raw/kitti/2011_09_26/2011_09_26_drive_0001_sync/velodyne_points/data/"

#tStart = time.time()
for frameNum in range(0,1):    # CHANGE LIDAR DATA FRAME NUMBER HERE !!!! 
	lidar_data_src_path = lidar_data_src_dir + str(frameNum).zfill(10) + ".bin"

	# OR OVERWRITE lidar_data_src_path TO SPICIFY THE PATH OF LIDAR DATA FILE !!!!
	#lidar_data_src_path = "0000000002.bin"

	b_lidar_data_src_path = lidar_data_src_path.encode('utf-8')
	# call the C function to create top view maps
	# The np array indata will be edited by createTopViewMaps to populate it with the 8 top view maps 
	SharedLib.createTopViewMaps(ctypes.c_void_p(indata.ctypes.data), ctypes.c_char_p(b_lidar_data_src_path), ctypes.c_float(x_MIN), 
								ctypes.c_float(x_MAX), ctypes.c_float(y_MIN), ctypes.c_float(y_MAX), ctypes.c_float(z_MIN), 
								ctypes.c_float(z_MAX), ctypes.c_float(x_DIVISION), ctypes.c_float(y_DIVISION), ctypes.c_float(z_DIVISION), 
								ctypes.c_int(X_SIZE), ctypes.c_int(Y_SIZE), ctypes.c_int(Z_SIZE)  )	

	# Code to visualize image one by one for one lidar frame (optional)
#	plt.figure()
#	for i in range(Z_SIZE+2):
#		plt.imshow(indata[:,:,i])
#	plt.show()

	# Code to visualize all images for one lidar frame(optional)
#	row = int(pow((Z_SIZE+2),0.5))
#	col = int(math.ceil((Z_SIZE+2)/row))
#	print(Z_SIZE)
#	print(row)
#	print(col)
#	if (int(row * col) != Z_SIZE +2 ):
#		col = col+1

#	plt.figure()
#	for i in range(Z_SIZE):
#		plt.subplot(row, col, i+1)
#		plt.imshow(indata[:,:,i])
#	plt.subplot(row, col, Z_SIZE+1)
#	plt.imshow(indata[:,:,Z_SIZE])
#	plt.title("density map")
#	plt.subplot(row, col, Z_SIZE+2)
#	plt.imshow(indata[:,:,Z_SIZE+1])
#	plt.title("intensity map")
#	plt.show()

print ('LiDAR data pre-processing complete for', frameNum + 1, 'frames')

#tEnd = time.time()
#print("It takes %f sec" % (tEnd-tStart))



