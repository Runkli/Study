#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dask.array as da
from dask import delayed
from dask.distributed import Client
import numpy as np
import h5py

    

def main():
    procArray = da.ones((3,3,3))
    
    procArray.to_hdf5('testout.hdf5','/arr')
    
    client.shutdown()
    
if __name__ == "__main__":
	client = Client()
	main()
