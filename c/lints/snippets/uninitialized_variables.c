#include <stdio.h>

int main(void) {
    // These variables are not initialized and would trigger the lint rule
    int x;
    float y, z;
    char c;

    // The lint rule should not flag these variables since they're initialized
    int a = 10;
    float b = 3.14, d = 2.71;
    char e = 'A';

    // This could lead to undefined behavior
    printf("Uninitialized values: %d, %f, %f, %c\n", x, y, z, c);

    // This is safe
    printf("Initialized values: %d, %f, %f, %c\n", a, b, d, e);

    return 0;
}