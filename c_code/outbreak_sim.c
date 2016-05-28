#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "dynamic_array.c"

#define max( a, b ) ( ( a > b) ? a : b )
#define min( a, b ) ( ( a < b) ? a : b )
int smod(int x, int y) {
    int div = (int)(x/y);
    int result = x - div*y;
    result = (result < 0) ? result + y : result;
    return result;
}


Outbreak* simulate_outbreak(int N, double mu, unsigned char ug, int mp, int** seeds, int ns,
        int C, int L) {
    
    Outbreak* infected = (Outbreak*)malloc(sizeof(Outbreak));
    init(infected, 2*N*N);
    unsigned char** deme_matrix = (unsigned char**)malloc(L*sizeof(unsigned char*));
    for(int i=0; i <L; i++) {
        deme_matrix[i] = (unsigned char*)calloc(L,sizeof(unsigned char));
    }
    printf("Seeds are:\n");
    for(int i=0; i < ns; i++) {
        printf("(%d,%d,%d)\n",seeds[i][0],seeds[i][1],seeds[i][2]);
        append(infected,seeds[i]);
    }
    printf("\n");


    int new_infected[3] = {0,0,0};
    int j=1;
    size_t temp_size;
    while( (ug && j < N) || (!ug && infected->used < mp)) {
        temp_size = infected->used;
        printf("temp_size is: %zu\n",temp_size);
        printf("j: %u\n",j);
        for(int k=0; k < temp_size; k++) {
            double Y = (double)rand()/(double)RAND_MAX;
            double R = pow((Y*(pow((double)L,-mu-1)-pow(C,-mu-1))+pow((double)C,-mu-1)),(-1./(mu+1)));
            double theta = (double)2*M_PI*rand()/(double)RAND_MAX;

            new_infected[0] = infected->demes[k][0] + (int)(R*cos(theta));
            new_infected[1] = infected->demes[k][1] + (int)(R*sin(theta));
            new_infected[2] = j;
            if(!deme_matrix[smod(new_infected[0],L/2)][smod(new_infected[1],L/2)]) {
                append(infected, new_infected);
                deme_matrix[smod(new_infected[0],L/2)][smod(new_infected[1],L/2)] = 1;
            }
        }
        j++;
    }
    trim(infected);
    print(infected);
    printf("number infected: %zu\n",infected->size);
    return infected;
}

int main(int argc, char** argv) {

    if(argc < 2) {
        printf("usage: ./outbreak_sim func\n");
        printf("options for func are simtest or arrtest\n");
    }
    if(strcmp(argv[1], "simtest")==0) {
        int N = 5;
        float mu = 1.8;
        unsigned char ug = 1;
        int mp = -1;
        int C = 1;
        int L = 10000;
        int **seeds = (int**)malloc(sizeof(int*));
        seeds[0] = (int*)malloc(sizeof(int)*3);
        seeds[0][0] = 0; seeds[0][1] = 0; seeds[0][2] = 0;
        int ns = 1;
        Outbreak* new_outbreak;
        new_outbreak = simulate_outbreak(N,mu,ug,mp,seeds,ns,C,L);
        print(new_outbreak);
        printf("c size is: %zu\n",new_outbreak->size);
    } 
    else if(strcmp(argv[1], "arrtest")==0) {
        Outbreak outbreak;
        init(&outbreak, 10);
        int deme[3] = {0};
        for(int j=0;j<20;j++) {
            deme[0]=j; deme[1] = j; deme[2] = j;
            append(&outbreak, deme);
        }
        print(&outbreak);
        trim(&outbreak);
        free_outbreak(&outbreak);
    }
}
