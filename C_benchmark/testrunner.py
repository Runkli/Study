#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import os

filepath = '/home/ilknull/Files/Code/HPC-Study-master/C_benchmark/'

output = subprocess.check_output('time ./a.out 1 1 1 3 3 3 0',shell=True,executable='/bin/bash')

print(output)

#subprocess.check_output('time mpirun -n {} {}a.out {} {} {} {} {} {} {}'
#              .format(numProcs,filepath,x0,y0,z0,x1,y1,z1,gen),shell=True)