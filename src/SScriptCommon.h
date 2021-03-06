#ifndef _SSCRIPTCOMMON_h
#define _SSCRIPTCOMMON_h

#include <inttypes.h>
#if !defined(ARDUINO)
    #include <cstdlib>
#endif
#include <stdio.h>
#include <string.h>
#include "SScript.h"

#if defined(ARDUINO)
	#include "Arduino.h"
#endif

#define DEBUG
#if defined(DEBUG) && defined(ARDUINO)
   #define DEBUG_PRINT(fmt, ...) Serial.println(fmt);//sprintf(DEBUG_BUFFER, fmt, ##__VA_ARGS__); Serial.print(DEBUG_BUFFER);
#elif defined(DEBUG)
   #define DEBUG_PRINT(fmt, ...) printf(fmt, ##__VA_ARGS__);
#else
   #define DEBUG_PRINT(fmt, ...) ;
#endif

int32_t getInt();
String getString();

#endif
