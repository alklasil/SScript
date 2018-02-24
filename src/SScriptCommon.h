#ifndef _SSCRIPTCOMMON_h
#define _SSCRIPTCOMMON_h

#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>

#if defined(ARDUINO) && ARDUINO >= 100
	#include "wprogram.h"
#elif defined(ARDUINO)
	#include "WProgram.h"
#endif

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

#endif
