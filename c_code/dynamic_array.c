#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int **demes;
    size_t used;
    size_t size;
} Outbreak;

void init(Outbreak *a, size_t initial_size) {
    a->demes = (int**)malloc(initial_size * sizeof(int*));
    for(int j=0; j<initial_size; j++) {
        a->demes[j] = (int *) malloc(3*sizeof(int));
    }
    a->used = 0;
    a->size = initial_size;
}

void print(Outbreak *a) {
    for(int j=0; j<a->used;j++) {
        printf("(%d,%d,%d)\n",a->demes[j][0],a->demes[j][1],a->demes[j][2]);
    }
}

void append(Outbreak *a, int deme[3]) {
    if (a->used == a->size) {
        a->size *= 2;
        a->demes = (int**)realloc(a->demes, a->size * sizeof(int*));
        for(int j=a->used; j<a->size;j++) {
            a->demes[j] = (int *) malloc(3*sizeof(int));
        }
    }
    a->demes[a->used][0] = deme[0];
    a->demes[a->used][1] = deme[1];
    a->demes[a->used][2] = deme[2];
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

