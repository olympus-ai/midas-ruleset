// These would correctly be flagged as reserved
int __internal_var = 5;     // Double underscore prefix (reserved)
char _Bool_custom = 'a';    // Conflicts with _Bool keyword
typedef struct Data _Atomic_data;  // Conflicts with _Atomic keyword
size_t my_size;             // Using reserved type
uint32_t value;             // Using reserved type

// These would be fine
int _hello = 10;            // Single underscore + lowercase (not reserved)
char my_var_name = 'x';     // Underscores in middle (not reserved)