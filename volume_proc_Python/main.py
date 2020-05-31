#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from mpi4py import MPI
import sys
import os.path
from numba import njit,prange

@njit(parallel=True)
def proc(arr,z,r,c,x0,x1,y0,y1,z0,z1):
    for y in prange(c):
        for x in prange(r):
            if(z>=z0 and z<z1 and y>=y0 and y<y1 and 
                x>=x0 and x<x1):
                arr[y*c+x] = 0


MPI.Init

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


x0=int(sys.argv[1])-1
y0=int(sys.argv[2])-1
z0=int(sys.argv[3])-1
x1=int(sys.argv[4])
y1=int(sys.argv[5])
z1=int(sys.argv[6])


if(len(sys.argv)==8 and rank==0):
    
    r = int(sys.argv[4])
    c = int(sys.argv[5])
    h = int(sys.argv[6])
    
    # a = np.zeros((r,c,h),dtype=np.int16)
    a = np.arange(0,r*c*h,dtype=np.int16).reshape((r,c,h))
    
    a.tofile('test.bin')
        
    # print(a.shape)
    np.array((r,c,h),dtype=np.int16).tofile('meta.bin')
    

if(rank==0):
    dims = np.fromfile('meta.bin',dtype=np.int16,count=-1)
else:
    
    dims = np.zeros(3,dtype=np.int16)
    
    
comm.Bcast(dims,root=0)

r = dims[0]
c = dims[1]
h = dims[2]


if(rank==0):
    fpOut = open('out.bin','wb',0)
    while(os.path.exists('out.bin')!=True):
        print("Waiting for file creation...")

comm.barrier()

if(rank!=0):
    fpOut = open('out.bin','rb+',0)

pad = h//size
rem = h%size

start = np.int16(0)
end = np.int16(0)


if(rank<rem):
    start = rank*(pad+1)
    end = start + pad
else:
    start = rank*pad+rem
    end = start + (pad-1)


fpIn = open('test.bin','rb')


for z in range(start,end+1):
    offset = z*r*c*2
    fpIn.seek(offset)
    b = np.fromfile(fpIn,dtype=np.int16,count=(r*c))#.reshape(r,c)
    
    
    proc(b,z,r,c,x0,x1,y0,y1,z0,z1)
# =============================================================================
#     for y in range(c):
#         for x in range(r):
#             if(z>=z0 and z<z1 and y>=y0 and y<y1 and 
#                x>=x0 and x<x1):
#                 b[y*c+x] = 0
# =============================================================================
    
    
    fpOut.seek(offset)
    b.tofile(fpOut)

fpIn.close()
fpOut.close()

comm.barrier()

if(rank==0): 
    b = np.fromfile('out.bin',dtype=np.int16,count=-1)
    
    print('B',b.size)
    print(b.reshape(h,r,c))
    
    os.remove('out.bin')
    
    

MPI.Finalize()






