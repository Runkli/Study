#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "matfuncs.h"
#include "process.h"



int main(int argc, char *argv[]){
	int num;
	MPI_File fpIn,fpOut;
	int rank,size;
	int ierr;
	
	if(argc==8){
			gen(atoi(argv[4]),atoi(argv[5]),atoi(argv[6]));
	}
	
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	
	MPI_Request request[4];
	MPI_Status status[4];

	
	int r=0,c=0,h=0;
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
	}
	
	MPI_Bcast(&r,1,MPI_INT,0,MPI_COMM_WORLD);
	MPI_Bcast(&c,1,MPI_INT,0,MPI_COMM_WORLD);
	MPI_Bcast(&h,1,MPI_INT,0,MPI_COMM_WORLD);
	//printf("proc: %d r: %d, c: %d\n",rank,r,c);
	
	
	int x0=atoi(argv[1]),y0=atoi(argv[2]),z0=atoi(argv[3]);
	x0--;y0--;z0--;
	int x1=atoi(argv[4]),y1=atoi(argv[5]),z1=atoi(argv[6]);
	int x,y,z;
	int offset;
	
	ierr = MPI_File_open(MPI_COMM_WORLD,"in.bin",
	MPI_MODE_RDONLY,MPI_INFO_NULL,&fpIn);
	ierr = MPI_File_open(MPI_COMM_WORLD,"out.bin",
	MPI_MODE_WRONLY,MPI_INFO_NULL,&fpOut);
	for(z=z0+rank;z<z1;z=z+size){
		printf("rank %d\n",rank);
		for(y=y0;y<y1;y++){
			for(x=x0;x<x1;x++){
				offset = sizeof(int)*((c)*y+x+
				(z*r*(c)));
				
				MPI_File_read_at(fpIn,offset,&num,
				1,MPI_INT,MPI_STATUS_IGNORE);
				//fseek(fp,offset,SEEK_SET);
				//fread(&num,sizeof(int),1,fp);
				//printf("%d ",num);
				
				num = proc(num);
				//printf("mpi %d ",num);
				//fseek(fp,offset,SEEK_SET);
				//fwrite(&num,sizeof(int),1,fp);
				MPI_File_write_at(fpOut,offset,&num,
				1,MPI_INT,status);
				
				
			} 
		}
	}
	
	
	//printmat(fpIn);
	
	//MPI_Wait(request,status);
	MPI_File_close(&fpIn);
	MPI_File_close(&fpOut);
		
	if(rank==0){
		FILE *f;
		f = fopen("out.bin","rb");
		printf("\nNew matrix:\n");
		printmat(f,r,c,h);
		fclose(f);
	}

	MPI_Finalize();
	
	
	
}