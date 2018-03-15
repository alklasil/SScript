// SScript.h

#ifndef _SSCRIPT_h
#define _SSCRIPT_h

#if defined(ARDUINO)
	#include "Arduino.h"
#endif

#if !defined(ARDUINO)
   #include <iostream>
   using namespace std;
   //#define String string
   typedef string String;
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

     int32_t stringCount;
     String *strings;

     SScript();
     int32_t setFunctions(void(*(*__functions))());
     int32_t set(char *buffer);

     void executeState(int32_t index);
     void loop();

     inline int32_t *parseIndex(int32_t *p) {
       // in SScript pointers are represented with '-' sign
       if (*p < 0) p = &variables[-(*p)];
       return &variables[*p];
     }


     // helper variables
     int32_t abortExpressionExecution;
     int32_t abortStateExecution;
     int32_t millis_var;
     int32_t *element;

	  char *str;

};

extern SScript sScript;

#endif
