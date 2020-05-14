#include <stdio.h>
#include <stdlib.h>
#include "matfuncs.h"

void printmat(FILE *fp,int x, int y, int z){
	int num,i,j,k;
	fseek(fp,0,SEEK_SET);
	
	for(k=0;k<z;k++){
		for(j=0;j<y;j++){
			for(i=0;i<x;i++){
				fread(&num,sizeof(int),1,fp);
				printf("%d ",num);
			}
			printf("\n");
		}
		printf("-\n");
	}
}



int gen(int x, int y, int z){
	int num;
	FILE *fp,*fpOut,*fpMeta;
	
	fp = fopen("in.bin","wb");
	fpOut = fopen("out.bin","wb");
	fpMeta = fopen("meta.bin","wb");
	
	int i,j,k;
	
	num = 0;
	
	for(k=0;k<z;k++){
		for(i=0;i<y;i++){
			for(j=0;j<x;j++){
				fwrite(&num,sizeof(int),1,fp);
				fwrite(&num,sizeof(int),1,fpOut);
			}
			
		}
		
	}
	
	fwrite(&x,sizeof(int),1,fpMeta);
	fwrite(&y,sizeof(int),1,fpMeta);
	fwrite(&z,sizeof(int),1,fpMeta);
	
	fclose(fpMeta);
	fclose(fp);
	fclose(fpOut);
	
	
}
