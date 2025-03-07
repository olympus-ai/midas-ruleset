#include <stdio.h>

int main() {
    // This line is fine - well within the 80 character limit
    int x = 10;

    // This line exceeds the 80 character limit and will trigger the line_too_long rule
    printf("This is an extremely long string that definitely exceeds the maximum allowed line length of 80 characters and will be flagged by our linter");

    return 0;
}