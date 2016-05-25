#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define max( a, b ) ( ( a > b) ? a : b )
#define min( a, b ) ( ( a < b) ? a : b )

void simulate_outbreak(int N, float mu, unsigned char ug, int mp, int** seeds) {
    for(int i=0; i < N; i++) {
        printf("i: %u\n", i);
        printf("i squared: %u\n", i*i);
    }
}

int main(int argl, char** args) {
    //test suite
}
