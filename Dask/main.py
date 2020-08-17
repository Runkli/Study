#!/usr/bin/env python3
# -*- coding: utf-8 -*-from dask.distributed import Client


import h5py
import dask.array as da
from dask import delayed
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
from dask import delayed
import numpy as np
import sys
import os


def proc(arr,z,r,c,x0,x1,y0,y1,z0,z1):
    
    for y in range(c):
        for x in range(r):
            if(z>=z0 and z<z1 and y>=y0 and y<y1 and 
                x>=x0 and x<x1):
#                arr[y*c+x] += 5
                arr[x][y]+=5
        
    return arr

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
        
        da.to_hdf5('in.hdf5',{'/a': a})
        np.array((r,c,h),dtype=np.int16).tofile(filepath+'meta.bin')
        
 
    dims = np.fromfile(filepath+'meta.bin',dtype=np.int16,count=-1)
   
    r = dims[0]
    c = dims[1]
    h = dims[2]
    
    
    fpIn = h5py.File('in.hdf5',mode='r+')
    
    procArrays=[]
    ar = fpIn['/a']
#    print(ar.shape)
#    print('types: ',type(ar),type(ar[0]))
    for z in range(h):    
        slic = ar[z]
        slic = delayed(proc)(slic,z,r,c,x0,x1,y0,y1,z0,z1).compute()
        procArrays.append(slic)

    procDask = da.stack(procArrays)
    print(procDask)
    print(procDask.compute())  
    

    da.to_hdf5('out.hdf5',{'/arr',procDask})
    
#    f = h5py.File('out.hdf5',mode='w')
#    d = f.require_dataset('/arr', shape=procDask.shape, dtype=procDask.dtype)
#    da.store(procDask, d)
    
#   
    #client.shutdown()
    
if __name__ == "__main__":
	#client = Client()
	main()
    
