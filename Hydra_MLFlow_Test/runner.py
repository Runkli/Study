#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hydra
from omegaconf import DictConfig


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
    
    print('Running...')
    print('mpiexec -n {} main_hydra.py {} {} {} {} {} {} {}'
          .format(numProcs,x0,y0,z0,x1,y1,z1,gen))
    
    filepath = '/home/ilknull/Files/Code/Python/Proc_wHydraMLFlow/'

    os.system('mpiexec -n {} {}main_hydra.py {} {} {} {} {} {} {}'
              .format(numProcs,filepath,x0,y0,z0,x1,y1,z1,gen))
    
if __name__ == "__main__":
    run()