#!/usr/bin/env python3
# -*- coding: utf-8 -*-from dask.distributed import Client


import h5py
import dask.array as da
from dask import delayed
from dask.distributed import LocalCluster
import numpy as np
import sys
import os

def main():

    x0=int(sys.argv[1])-1
    y0=int(sys.argv[2])-1
    z0=int(sys.argv[3])-1
    x1=int(sys.argv[4])
    y1=int(sys.argv[5])
    z1=int(sys.argv[6]) 
    
    filepath = '/home/ilknull/Files/Code/HPC-Study-master/Dask/'
    
    if(int(sys.argv[7])==1):
#        print("new")
        r=int(sys.argv[4])
        c=int(sys.argv[5])
        h=int(sys.argv[6])
        
        
        a = da.ones((r,c,h),dtype=np.int16)
        
        da.to_hdf5('test.hdf5',{'/a': a})
        np.array((r,c,h),dtype=np.int16).tofile(filepath+'meta.bin')
        
 
    dims = np.fromfile(filepath+'meta.bin',dtype=np.int16,count=-1)
   
    r = dims[0]
    c = dims[1]
    h = dims[2]
    
    
    fpIn = h5py.File('test.hdf5',mode='r+')
    
    ar = fpIn['/a']
    b = da.from_array(ar)
    
    
    newb = da.from_array(ar)
    
    newb += da.exp(b)[z0:z1,y0:y1,x0:x1]
    
    
    result = newb.compute()
    c = da.from_array(result)
#    print('after proc',c.compute())
    
    da.to_hdf5('out.hdf5',{'/a': c}) 
    
    fpIn.close()
    
    fpOut = h5py.File('out.hdf5',mode='r')
    ar = fpOut['/a']
    dd = da.from_array(ar)
    print(dd.compute())
   
    os.remove('out.hdf5')
    
if __name__ == "__main__":
    client = LocalCluster(n_workers=4, ip='127.0.0.1')
    main()
    
