#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <math.h>
#include <time.h>

#include "dynamic_array.c"
#include "hash_table.c"

#define C 1
#define d 2
#define L 1000000000

Outbreak* sim_cont_outbreak(double mu, int mp, int** seeds, int ns) {
    srand(clock());
    BoolTable* inf_table = (BoolTable*)malloc(sizeof(BoolTable));
    init_hash(inf_table);
    Outbreak* infected = (Outbreak*)malloc(sizeof(Outbreak));
    init_outbreak(infected, mp);
    for(int i=0; i < ns; i++) {
        append(infected,seeds[i]);
        install(inf_table,seeds[i][0],seeds[i][1]);
    }
    double scaled_t =0.;
    int* new_infected = (int*)malloc(d*sizeof(int));
    while(infected->used<mp) {
        scaled_t +=1./(1+infected->used-ns);
        int k = rand() % infected->used;
        double Y = (double)rand()/(double)RAND_MAX;
        double R = pow((Y*(pow((double)L,-mu-1)-pow(C,-mu-1))+pow((double)C,-mu-1)),(-1./(mu+1)));
        double theta = ((double)2*M_PI*rand())/(double)RAND_MAX;
        new_infected[0] = infected->demes[k][0] + (int)(R*cos(theta));
        new_infected[1] = infected->demes[k][1] + (int)(R*sin(theta));
        new_infected[2] = (int)round(scaled_t);
        new_infected[3] = infected->demes[k][3];
        if(!lookup(inf_table, new_infected[0],new_infected[1])) {
            append(infected, new_infected);
            install(inf_table, new_infected[0], new_infected[1]);
        }
    }
    trim(infected);
    free_hash(inf_table);
    return infected;
}



int main(int argc, char** argv) {
    if(argc < 2) {
        printf("usage: ./outbreak_sim testname\n");
        printf("options for testname are simtest or arrtest or hashtest\n");
    }
    else if(strcmp(argv[1], "simtest")==0) {
        srand(clock());
        int mp = 1000;
        float mu =1.9;
        int ns =100;
        int **seeds = (int**)malloc(ns*sizeof(int*));
        for(int n=0; n<ns; n++){
            seeds[n] = (int*)malloc(sizeof(int)*(d+2));
            for(int i=0; i<d; i+=1) {
                seeds[n][i] = (n+i)/3;
            }
            seeds[n][d]=0; seeds[n][d+1]=rand() % 2;
        }
        Outbreak* new_outbreak; 
        new_outbreak = sim_cont_outbreak(mu, mp, seeds, ns);
        save_outbreak(new_outbreak,"test_outbreak.txt");
        //print(new_outbreak);
        printf("total size is: %zu\n",new_outbreak->size);
    } else if(strcmp(argv[1], "arrtest")==0) {
        Outbreak outbreak;
        init_outbreak(&outbreak, 10);
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
        init_hash(tab);
        install(tab, 0,0);
        unsigned char result = lookup(tab,0,0);
        printf("true result %u\n", result);
        result = lookup(tab,0,1);
        printf("false result %u\n", result);
        free_hash(tab);
        BoolTable* tab2 = (BoolTable*)malloc(sizeof(BoolTable));
        init_hash(tab2);
        install(tab2,0,5);
    }
}
