#include <stdio.h>

int main(void) {
    int i = 0;

    // Using goto for a loop (bad practice)
start:
    printf("i = %d\n", i);
    i++;
    if (i < 5)
        goto start;

    // Using goto for error handling (common but often avoidable)
    FILE *file = fopen("data.txt", "r");
    if (file == NULL) {
        printf("Error opening file!\n");
        goto cleanup;
    }

    char buffer[100];
    if (fread(buffer, 1, sizeof(buffer), file) < 1) {
        printf("Error reading file!\n");
        goto cleanup;
    }

    printf("File read successfully.\n");

cleanup:
    if (file != NULL)
        fclose(file);

    return 0;
}