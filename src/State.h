// State.h

#ifndef _STATE_h
#define _STATE_h

#if defined(ARDUINO)
	#include "Arduino.h"
#endif

#include "SScriptCommon.h"
#include "Expression.h"

class State
{
 protected:

     Expression *expressions;
     unsigned expressionCount;

 public:
	int32_t set(char *s);
    int32_t execute();
    State();
    ~State();
};

#endif
