#include <stdio.h>
#include <stdlib.h>

/* TODO: Implement error handling */
int main(void) {
    int *data = malloc(sizeof(int) * 10);

    // FIXME: This could cause memory leak
    if (data == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    /* XXX: This algorithm is inefficient */
    for (int i = 0; i < 10; i++) {
        data[i] = i * 2;
    }

    // HACK: Temporary workaround for buffer issue
    printf("Data: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", data[i]);
    }
    printf("\n");

    /* NOTE: Consider using a better data structure */
    free(data);

    // BUG: Sometimes returns wrong exit code
    return 0;
}