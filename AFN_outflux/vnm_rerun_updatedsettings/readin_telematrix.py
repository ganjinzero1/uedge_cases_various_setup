import h5py
import numpy as np

fn = './tele-transport_matrix.h5'
f1 = h5py.File(fn,'r+')
print (f1.keys())

bbb.cftelematrix[1:com.nx+1,1:com.nx+1,0] = f1['Mat_Dtot']
