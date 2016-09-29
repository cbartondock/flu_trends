#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define d 2

//demes have the form (x1, ... , xN, t, q) where q is an attr number.

typedef struct {
    int **demes;
    size_t used;
    size_t size;
} Outbreak;

void init_outbreak(Outbreak *a, size_t initial_size) {
    a->demes = (int**)malloc(initial_size * sizeof(int*));
    for(int j=0; j<initial_size; j++) {
        a->demes[j] = (int *) malloc((d+2)*sizeof(int));
    }
    a->used = 0;
    a->size = initial_size;
}

void print(Outbreak *a) {
    for(int j=0; j<a->used;j++) {
        printf("(%d", a->demes[j][0]);
        for(int m=1; m< d+2; m++) {
            printf(", %d", a->demes[j][m]);
        } printf(")\n");
    }
}

void save_outbreak(Outbreak* infected, char* filename) {
    FILE *fp;
    fp = fopen(filename,"w");
    for(int n=0; n<infected->used; n++) {
        fprintf(fp,"%d,%d,%d,%d\n",infected->demes[n][0],infected->demes[n][1],infected->demes[n][2],infected->demes[n][3]);
    }
    fclose(fp);
}

void append(Outbreak *a, int* deme) {
    if (a->used == a->size) {
        a->size *= 2;
        a->demes = (int**)realloc(a->demes, a->size * sizeof(int*));
        for(int j=a->used; j<a->size;j++) {
            a->demes[j] = (int *) malloc((d+2)*sizeof(int));
        }
    }
    for(int m=0; m< d+2; m++) {
        a->demes[a->used][m] = deme[m];
    }
    a->used+=1;
}

void free_outbreak(Outbreak *a) {
    for(int j=0; j< a->size; j++) {
        free(a->demes[j]);
    }
    free(a->demes);
}
void trim(Outbreak *a) {
        for(int j=a->used+1; j<a->size;j++) {
            free(a->demes[j]);
        }
        a->size=a->used;
}

