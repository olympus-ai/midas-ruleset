// These will be flagged - lowercase identifiers after #define
#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))
#define square(x) ((x) * (x))
#define myConstant 42
#define pi 3.14159

// These are correct - UPPERCASE identifiers
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))
#define MY_CONSTANT 42
#define PI 3.14159
#define VERSION "1.0.0"

// Mixed case starting with capital is also inappropriate but not caught by this rule
#define MyFunction(x) do_something(x)