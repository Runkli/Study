To use it, use mpirun with the output file, and input ```x0,y0,z0,x1,y1,z1,flag``` as the arguments.
The use of flag is to generate a new default cube if used. It only checks if the final flag exists so it can be any input you like.

If the cube already exists, it will manipulate the given ranges. If it doesn't, it will create a cube using the outer bounds as the edges of the cube.
All information is stored in binary format.

Here is what ```mpirun ./a.out 1 1 1 2 2 3``` will produce, with the process being set to ```var = var + 5```
```
Current matrix:  
0 0 0 
0 0 0 
0 0 0 
-
0 0 0 
0 0 0 
0 0 0 
-
0 0 0 
0 0 0 
0 0 0 
-
```
```
New matrix:
5 5 0 
5 5 0 
0 0 0 
-
5 5 0 
5 5 0 
0 0 0 
-
5 5 0 
5 5 0 
0 0 0 
-
```
However it would've produced the following had a flag was introduced since ```x1=2,y1=2``` would be the maximum size
```
New matrix:
5 5 
5 5 
-
5 5 
5 5 
-
5 5 
5 5 
-
```



