#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int **demes;
    size_t used;
    size_t size;
    size_t d;
} Outbreak;

void init(Outbreak *a, size_t initial_size, size_t d) {
    a->demes = (int**)malloc(initial_size * sizeof(int*));
    for(int j=0; j<initial_size; j++) {
        a->demes[j] = (int *) malloc(d*sizeof(int));
    }
    a->used = 0;
    a->size = initial_size;
    a->d = d;
}

void print(Outbreak *a) {
    for(int j=0; j<a->used;j++) {
        printf("(%d", a->demes[j][0]);
        for(int m=1; m< a->d; m++) {
            printf(", %d", a->demes[j][m]);
        } printf(")\n");
    }
}

void append(Outbreak *a, int* deme) {
    if (a->used == a->size) {
        a->size *= 2;
        a->demes = (int**)realloc(a->demes, a->size * sizeof(int*));
        for(int j=a->used; j<a->size;j++) {
            a->demes[j] = (int *) malloc((a->d)*sizeof(int));
        }
    }
    for(int m=0; m< a->d; m++) {
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

