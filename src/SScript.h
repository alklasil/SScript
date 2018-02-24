// SScript.h

#ifndef _SSCRIPT_h
#define _SSCRIPT_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "wprogram.h"
#elif defined(ARDUINO)
	#include "WProgram.h"
#endif

#include "SScriptCommon.h"
#include "State.h"

class SScript
{
 protected:

     // for now all scriptable variables are integers
     int32_t stateCount;
     State *states;

 public:

     int32_t variableCount;
     int32_t *variables;

     SScript();
     // int32_t setFunctions(void(**__functions)(int32_t *leftValue, int32_t *rightValue));
     int32_t setFunctions(void(*(*__functions))(int32_t *leftValue, int32_t *rightValue));
     int32_t set(char *buffer);

     void loop();
     int32_t executeState(int32_t index);

     // helper variables
     const static int32_t accessModePointer = 0;
     const static int32_t accessModeValue = 1;
     int32_t accessMode;
     int32_t abortExpressionExecution;

     // functions used in scripts (pointers)
     // void(*functions[])(int32_t *leftValue, int32_t *rightValue);

};

extern SScript sScript;

#endif
