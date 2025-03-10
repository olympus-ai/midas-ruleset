#include <stdio.h>

// This function has consistent indentation (4 spaces per level)
void correct_indentation(void) {
    if (1) {
        printf("This is properly indented with 4 spaces\n");
        if (2) {
            printf("Nested block with consistent indentation\n");
        }
    }
}

// This function has inconsistent indentation
void wrong_indentation(void) {
  printf("This line uses 2 spaces instead of 4\n");  // Will be flagged
   if (1) {  // 3 spaces instead of 4, will be flagged
      printf("This uses different indentation\n");  // Inconsistent
        printf("Back to 8 spaces here\n");  // Correct but inconsistent with above
	printf("This line uses a tab instead of spaces\n");  // Will be flagged
	  printf("Tab plus spaces\n");  // Will be flagged
    }
}

// Missing indentation in control structure
void missing_indentation(void) {
    if (1)
    printf("This line should be indented\n");  // Will be flagged

    for (int i = 0; i < 10; i++)
    printf("%d ", i);  // Will be flagged
}