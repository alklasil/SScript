// Configuration.h

#ifndef _CONFIGURATION_h
#define _CONFIGURATION_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "wprogram.h"
#else
	#include "WProgram.h"
#endif

#include <iostream>

#define CONFIGURATION_TEST ""

extern void(*functions[])(int32_t *leftValue, int32_t *rightValue);

#endif
