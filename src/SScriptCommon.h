#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>

#define DEBUG
#if defined(DEBUG) && defined(ARDUINO)
    #define DEBUG_PRINT(x) Serial.print(x);
#elif defined(DEBUG)
    #define DEBUG_PRINT(x) printf(x);
#else
    #define DEBUG_PRINT(x) ;
#endif

extern void(*(*_functions))(int32_t *leftValue, int32_t *rightValue);
int32_t getInt(char *s);
