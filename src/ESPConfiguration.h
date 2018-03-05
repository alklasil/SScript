// Configuration.h

#ifndef _ESPCONFIGURATION_h
#define _ESPCONFIGURATION_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "wprogram.h"
#elif defined(ARDUINO)
	#include "WProgram.h"
#endif

#include <cstdint>
#include <cstdlib>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <climits>
#include "../SScript.h"

#define CONFIGURATION_TEST ""

extern void(*functions[])(int32_t *leftValue, int32_t *rightValue);

#endif
