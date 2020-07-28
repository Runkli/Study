#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import hydra
from omegaconf import DictConfig
import subprocess
from mlflow import log_metric, log_param, set_tracking_uri, start_run, set_experiment


set_tracking_uri("http://localhost:5000/")
set_experiment('C Benchmark')

@hydra.main(config_path="config.yaml")
def run(cfg : DictConfig):
    x0 = cfg['coordinates']['x0']
    x1 = cfg['coordinates']['x1']
    y0 = cfg['coordinates']['y0']
    y1 = cfg['coordinates']['y1']
    z0 = cfg['coordinates']['z0']
    z1 = cfg['coordinates']['z1']
    numProcs = cfg['ranks']
    gen = cfg['gen']
    numThreads = 4//numProcs

    print('Running...')

#    time = ('time ls',shell=True)
#    print(time)

    filepath = '/home/ilknull/Files/Code/HPC-Study-master/C_benchmark/'
    
    print('time OMP_NUM_THREADS={} mpirun -n {} {}a.out {} {} {} {} {} {} {}'
              .format(numThreads,numProcs,filepath,x0,y0,z0,x1,y1,z1,gen))
    

    output = subprocess.check_output('time mpirun -n {} {}a.out {} {} {} {} {} {} {}'
              .format(numProcs,filepath,x0,y0,z0,x1,y1,z1,gen),shell=True,executable='/bin/bash',stderr=subprocess.STDOUT)
    output = output.decode()
    output = output[output.index('real')+5:output.index('user')-2]
    output = output.split('m')
    mins = int(output[0])
    secs = output[1].split(',')[0] + output[1].split(',')[1]
    secs = int(secs)/1000
    
    time = mins*60 + secs
    print(output,time)
    
    with start_run():
        log_param('NumRanks',numProcs)
        log_param('Size',[x1,y1,z1])
        log_metric("Time Elapsed", time)
    
    
    
if __name__ == "__main__":
    run()
