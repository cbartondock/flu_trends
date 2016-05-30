#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "dynamic_array.c"
#include "hash_table.c"

Outbreak* simulate_outbreak(int N, double mu, unsigned char ug, int mp, int** seeds, int ns,
        int C, int L) {
    srand(clock());
    BoolTable* tab = (BoolTable*)malloc(sizeof(BoolTable));

    init_h(tab, L);
    Outbreak* infected = (Outbreak*)malloc(sizeof(Outbreak));
    if(ug) {
        init(infected, 2*N*N);
    } else {
        init(infected, mp);
    }
    for(int i=0; i < ns; i++) {
        //printf("seed: (%d,%d,%d)\n",seeds[i][0],seeds[i][1],seeds[i][2]);
        append(infected,seeds[i]);
        install(tab, seeds[i][0],seeds[i][1]);
    }
    int new_infected[3] = {0,0,0};
    int j=1;
    size_t temp_size;
    while( (ug && j < N) || (!ug && infected->used < mp)) {
        temp_size = infected->used;
        for(int k=0; k < temp_size; k++) {
            if(!ug && infected->used==mp) {break;}
            double Y = (double)rand()/(double)RAND_MAX;
            double R = pow((Y*(pow((double)L,-mu-1)-pow(C,-mu-1))+pow((double)C,-mu-1)),(-1./(mu+1)));
            double theta = (double)2*M_PI*rand()/(double)RAND_MAX;
            new_infected[0] = infected->demes[k][0] + (int)(R*cos(theta));
            new_infected[1] = infected->demes[k][1] + (int)(R*sin(theta));
            new_infected[2] = j;
            if(!lookup(tab, new_infected[0],new_infected[1])) {
                append(infected, new_infected);
                install(tab, new_infected[0], new_infected[1]);
            }
        }
        j++;
    }
    trim(infected);
    free_hash(tab);
    return infected;
}


int main(int argc, char** argv) {
    if(argc < 2) {
        printf("usage: ./outbreak_sim func\n");
        printf("options for func are simtest or arrtest\n");
    }
    if(strcmp(argv[1], "simtest")==0) {
        int N = 10;
        float mu = 1.8;
        unsigned char ug = 0;
        int mp = 1;
        int C = 1;
        int L = 10000000;
        int **seeds = (int**)malloc(2*sizeof(int*));
        seeds[0] = (int*)malloc(sizeof(int)*3);
        //seeds[1] = (int*)malloc(sizeof(int)*3);
        seeds[0][0] = 0; seeds[0][1] = 0; seeds[0][2] = 0;
        //seeds[1][0] = 1; seeds[1][1] = 0; seeds[1][2] = 0;
        int ns = 1;
        Outbreak* new_outbreak;
        new_outbreak = simulate_outbreak(N,mu,ug,mp,seeds,ns,C,L);
        print(new_outbreak);
        printf("c size is: %zu\n",new_outbreak->size);
    } else if(strcmp(argv[1], "arrtest")==0) {
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
    } else if(strcmp(argv[1], "hashtest")==0) {
        BoolTable* tab = (BoolTable*)malloc(sizeof(BoolTable));
        int L = 10000;
        init_h(tab, L);
        install(tab,0,0);
        unsigned char result = lookup(tab,0,0);
        printf("true result %u\n", result);
        result = lookup(tab,0,1);
        printf("false result %u\n", result);
        free_hash(tab);
        BoolTable* tab2 = (BoolTable*)malloc(sizeof(BoolTable));
        init_h(tab2, L);
        install(tab2,0,5);
    }
}
