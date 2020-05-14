#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "matfuncs.h"
#include "process.h"
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char *argv[]){
	int num;
	
	int rank,size;
	int ierr;
	
	//generates a default 0 cube if the flag exists
	if(argc==8){
		gen(atoi(argv[4]),atoi(argv[5]),atoi(argv[6]));
	}
	
	//MPI Inits
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	
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
	fpOut = fopen("out.bin","rb+");
	setvbuf(fpOut,"",_IONBF,0);
	
	/*Each rank takes slices that are increments of
	the num of ranks
	*/
	
	for(z=z0+rank;z<z1;z=z+size){
		for(y=y0;y<y1;y++){
			for(x=x0;x<x1;x++){
				offset = sizeof(int)*(c*y + x + z*r*c);
				
				fseek(fpIn, offset, SEEK_SET);
				fread(&num, sizeof(int),1,fpIn);
				
				num = proc(num);
				
				fseek(fpOut, offset, SEEK_SET);	
				fwrite(&num, sizeof(int),1,fpOut);
				
			} 
		}
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
		
	}
	
	
}
