import h5py
import numpy as np
from uedge import com

xcuts = com.ixpt1[0]
# initialize tele-transport matrix
bbb.cftelematrix[:,:,:,:] = 0.

# outer wall boundary tele-matrix
with h5py.File('tele-transport_matrix.h5', 'r') as f:
    print("keys:", list(f.keys()))
    print("number of elements of the tele-matrix for outer wall, nx*nx",com.nx**2 == f['Mat_Dtot'].shape[0]*f['Mat_Dtot'].shape[1])
    # Read a dataset into memory before the file closes
    bbb.cftelematrix[1,1:com.nx+1,1:com.nx+1,0] = f['Mat_Dtot']

# pfr boundary
filname = 'pf_lowres_telematrix99.h5'
with h5py.File(filname, 'r') as f:
    print("keys:", list(f.keys()))
    print("number of elements of the matrix for PFR, ",(com.ixpt1[0]+com.nx-com.ixpt2[0])**2 == f['cftelematrix_pf'].shape[0]*f['cftelematrix_pf'].shape[1])
    # UEDGE cftelematrix cij, i denotes sourcing segment index and j denotes receiving segment index
    # pf_lowres_telematrix99.h5 seems to to be oppose to the UEDGE definition ?
    temp = np.transpose(f['cftelematrix_pf'])
    # Read a dataset into memory before the file closes
    bbb.cftelematrix[0,1:com.ixpt1[0]+1,1:com.ixpt1[0]+1,0] = temp[:xcuts,:xcuts]
    bbb.cftelematrix[0,1:com.ixpt1[0]+1,com.ixpt2[0]+1:com.nx+1,0] = temp[:xcuts,xcuts:]
    bbb.cftelematrix[0,com.ixpt2[0]+1:com.nx+1,1:com.ixpt1[0]+1,0] = temp[xcuts:,:xcuts]
    bbb.cftelematrix[0,com.ixpt2[0]+1:com.nx+1,com.ixpt2[0]+1:com.nx+1,0] = temp[xcuts:,xcuts:]

