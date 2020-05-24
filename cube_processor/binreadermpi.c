#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <unistd.h>
#include "matfuncs.h"
#include "process.h"
#include <omp.h>
#include <math.h>

int main(int argc, char *argv[]){

	double start_t = MPI_Wtime();
	
	int num;
	
	int rank,size;
	int ierr;
	omp_set_nested(1);
	
	
	//MPI Inits
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	
	
	//generates a default 0 cube if the flag exists
	if(argc==8 && rank==0){
	
		genInput(atoi(argv[4]),atoi(argv[5]),atoi(argv[6]));
		//gen(atoi(argv[4]),atoi(argv[5]),atoi(argv[6]));
	}
	
	
	
	MPI_Request request[4];
	MPI_Status status[4];

	
	int r=0,c=0,h=0;
	
	/*Master reads the dims from the metadata file and 
	broadcasts it to the other ranks
	*/
	if(rank==0){
		
		FILE* fp;
		fp = fopen("meta.bin","rb");
		fread(&r,sizeof(int),1,fp);
		fread(&c,sizeof(int),1,fp);
		fread(&h,sizeof(int),1,fp);
		fclose(fp);
		
	
		fp = fopen("in.bin","rb");
		printf("Current matrix:\n");
		printmat(fp,r,c,h);
		fclose(fp);
		//genOutput(r,c,h);
	}
	
	
	MPI_Bcast(&r,1,MPI_INT,0,MPI_COMM_WORLD);
	MPI_Bcast(&c,1,MPI_INT,0,MPI_COMM_WORLD);
	MPI_Bcast(&h,1,MPI_INT,0,MPI_COMM_WORLD);
	
	//Take endpoints from argv
	int x0=atoi(argv[1]),y0=atoi(argv[2]),z0=atoi(argv[3]);
	x0--;y0--;z0--;
	int x1=atoi(argv[4]),y1=atoi(argv[5]),z1=atoi(argv[6]);
	int x,y,z;
	int offset;
	
	FILE *fpIn, *fpOut;
	
	fpIn = fopen("in.bin","rb");
	
	int* buffer = (int*)malloc(sizeof(int)*(x1-x0+1));
	
	int temp;
	if(rank==0){
		fpOut = fopen("out.bin","wb");
		while(access("out.bin",F_OK)==1){
			printf("Waiting for file open...\n");
		}
	}
	MPI_Barrier(MPI_COMM_WORLD);
	if(rank!=0){
		fpOut = fopen("out.bin","rb+");	
	}
	
	setvbuf(fpOut,NULL,_IONBF,0);
	
	/*Each rank takes slices that are increments of
	the num of ranks
	*/
	int start,end;
	int buf=0;
	int tid;
	int pad = h/size;
	int rem = h%size;
	
	if(rank<rem){
		start = rank*(pad+1);
		end = start+pad;
	}else{
		start = rank*pad+rem;
		end = start + (pad-1);
	}

	int* volbuffer = (int*)malloc(sizeof(int)*r*c);
	int* tempbuffer = (int*)malloc(sizeof(int)*r*c);
	for(z=start;z<=end;z++){
		offset=sizeof(int)*(z*r*c);
		fseek(fpIn,offset,SEEK_SET);
		fread(tempbuffer,sizeof(int),r*c,fpIn);
		
		#pragma omp parallel for collapse(2) private(x,y,z) schedule(static)
		for(y=0;y<c;y++){
			for(x=0;x<r;x++){
				if(z>=z0 && z<z1 && y>=y0 && y<y1 && x>=x0 && x<x1){
					volbuffer[y*c+x] = proc(tempbuffer[y*c+x]);
				}
			}
		}
		fseek(fpOut,offset,SEEK_SET);
		fwrite(volbuffer,sizeof(int),r*c,fpOut);
	}
		
	
	
	MPI_Barrier(MPI_COMM_WORLD);
	
	fclose(fpIn);
	fclose(fpOut);
	
	if(rank!=0){
		MPI_Finalize();
	}else{
		FILE *fpOut = fopen("out.bin","rb");
		fseek(fpOut,0,SEEK_SET);
		
		printf("\nNew matrix:\n");
		printmat(fpOut,r,c,h);
	
		fclose(fpOut);
		MPI_Finalize();
		if(remove("out.bin")!=0){
			printf("\nFile not deleted succesfully.\n");
		}
		
	}
	
	double end_t = MPI_Wtime();
	
	printf("\nProcess took: %f seconds\n",end_t-start_t);
	
}
