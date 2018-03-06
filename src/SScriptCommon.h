#ifndef _SSCRIPTCOMMON_h
#define _SSCRIPTCOMMON_h

#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>
#include "SScript.h"

#if defined(ARDUINO) && ARDUINO >= 100
	#include "wprogram.h"
#elif defined(ARDUINO)
	#include "WProgram.h"
#endif

#define DEBUG
#if defined(DEBUG) && defined(ARDUINO)
   #define DEBUG_PRINT(fmt, ...) ;//sprintf(DEBUG_BUFFER, fmt, ##__VA_ARGS__); Serial.print(DEBUG_BUFFER);
#elif defined(DEBUG)
   #define DEBUG_PRINT(fmt, ...) printf(fmt, ##__VA_ARGS__);
#else
   #define DEBUG_PRINT(fmt, ...) ;
#endif

extern void(*(*_functions))(int32_t *leftValue, int32_t *rightValue);
int32_t getInt();
String getString();

#endif
