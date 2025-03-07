#include <stdio.h>

// This function name is deliberately longer than 20 characters
void thisIsAReallyReallyLongFunctionNameThatShouldBeAvoided(int param1, int param2) {
    printf("This function has a very long name: %d, %d\n", param1, param2);
}

// This function name is acceptable (less than 20 chars)
void shortFunctionName(int x) {
    printf("This function has a reasonable name: %d\n", x);
}

int main() {
    thisIsAReallyReallyLongFunctionNameThatShouldBeAvoided(42, 123);
    shortFunctionName(42);
    return 0;
}