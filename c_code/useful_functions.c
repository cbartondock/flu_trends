#include<stdlib.h>
#include<stdio.h>
#include<math.h>

int smod(int x, int y) {
    int div = (int)(x/y);
    int result = x - div*y;
    result = (result < 0) ? result + y : result;
    return result;
}
