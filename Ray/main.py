#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys
import ray


@ray.remote
def proc(arr,z,r,c,x0,x1,y0,y1,z0,z1):
    newArr = np.empty_like(arr)

    for y in range(c):
        for x in range(r):
            if(z>=z0 and z<z1 and y>=y0 and y<y1 and 
                x>=x0 and x<x1):
                newArr[y*c+x] = arr[y*c+x] + 5
            else:
                newArr[y*c+x] = arr[y*c+x]
                
    return newArr

                
def main():

    x0=int(sys.argv[1])-1
    y0=int(sys.argv[2])-1
    z0=int(sys.argv[3])-1
    x1=int(sys.argv[4])
    y1=int(sys.argv[5])
    z1=int(sys.argv[6])
    
    filepath = '/home/ilknull/Files/Code/HPC-Study-master/Ray/'
    
    if(int(sys.argv[7])==1):
        print("new")
        r=int(sys.argv[4])
        c=int(sys.argv[5])
        h=int(sys.argv[6])
        
        a = np.zeros((r,c,h),dtype=np.int16)
        # a = np.arange(0,r*c*h,dtype=np.int16).reshape((r,c,h))
        
        a.tofile(filepath+'test.bin')
            
        print('writing: \n',a)
        print('\n'*3)
        
        np.array((r,c,h),dtype=np.int16).tofile(filepath+'meta.bin')
        
    
    dims = np.fromfile(filepath+'meta.bin',dtype=np.int16,count=-1)
        
    r = dims[0]
    c = dims[1]
    h = dims[2]
    
    
    fpOut = open(filepath+'out.bin','wb',0)
    
    fpIn = open(filepath+'test.bin','rb')
    
    
    for z in range(0,h):
        offset = z*r*c*2
        fpIn.seek(offset)
        b = np.fromfile(fpIn,dtype=np.int16,count=(r*c))#.reshape(r,c)
        print('reading:',b)
        b_future = proc.remote(b,z,r,c,x0,x1,y0,y1,z0,z1)
        b = ray.get(b_future)
        fpOut.seek(offset)
        b.tofile(fpOut)
    
    
    fpIn.close()
    fpOut.close()
    
    fpIn = open(filepath+'out.bin','rb',0)
    a = np.fromfile(fpIn,dtype=np.int16,count=-1)
    print(a.reshape(r,c,h))
    
        
if __name__ == "__main__":

    ray.init()
    main()
    ray.shutdown()
    
    
