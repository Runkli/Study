#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from mpi4py import MPI
from numba import njit,prange
from mlflow import log_metric, log_param,set_tracking_uri,start_run
import os
import time
import sys

                
set_tracking_uri("http://localhost:5000/")


@njit
def proc(arr,z,r,c,x0,x1,y0,y1,z0,z1):
    for y in prange(c):
        for x in prange(r):
            if(z>=z0 and z<z1 and y>=y0 and y<y1 and 
                x>=x0 and x<x1):
                arr[y*c+x] += 5
                


def main():
    t0 = time.time()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    x0=int(sys.argv[1])-1
    y0=int(sys.argv[2])-1
    z0=int(sys.argv[3])-1
    x1=int(sys.argv[4])
    y1=int(sys.argv[5])
    z1=int(sys.argv[6])
    
    filepath = '/file/path/here/'
    
    if(int(sys.argv[7])==1 and rank==0):
        print("new")
        r=int(sys.argv[4])
        c=int(sys.argv[5])
        h=int(sys.argv[6])
        
        a = np.zeros((r,c,h),dtype=np.int16)
        # a = np.arange(0,r*c*h,dtype=np.int16).reshape((r,c,h))
        
        a.tofile(filepath+'test.bin')
            
        np.array((r,c,h),dtype=np.int16).tofile(filepath+'meta.bin')
        
    
    if(rank==0):
        dims = np.fromfile(filepath+'meta.bin',dtype=np.int16,count=-1)
    else:
        
        dims = np.zeros(3,dtype=np.int16)
        
        
    comm.Bcast(dims,root=0)
    
    r = dims[0]
    c = dims[1]
    h = dims[2]
    
    
    if(rank==0):
        fpOut = open(filepath+'out.bin','wb',0)
        while(os.path.exists(filepath+'out.bin')!=True):
            print("Waiting for file creation...")
    
    comm.barrier()
    
    if(rank!=0):
        fpOut = open(filepath+'out.bin','rb+',0)
    
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
    
    
    fpIn = open(filepath+'test.bin','rb')
    
    
    for z in range(start,end+1):
        offset = z*r*c*2
        fpIn.seek(offset)
        b = np.fromfile(fpIn,dtype=np.int16,count=(r*c))#.reshape(r,c)
        
        
        proc(b,z,r,c,x0,x1,y0,y1,z0,z1)
        fpOut.seek(offset)
        b.tofile(fpOut)
    
    fpIn.close()
    fpOut.close()
    
    comm.barrier()
    
    if(rank==0): 
        b = np.fromfile(filepath+'out.bin',dtype=np.int16,count=-1)
        
        print(b.reshape(h,r,c))
        
        os.remove(filepath+'out.bin')
        
        with start_run():
            log_param('a',[x0,y0,z0])
            log_param('b',[x1,y1,z1])
            log_param('NumRanks',size)
            log_param('Size',[r,c,h])
            log_metric("Time Elapsed", time.time()-t0)
        
        
    
    
    
if __name__ == "__main__":
    MPI.Init
    main()
    MPI.Finalize()
    
