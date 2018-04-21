// Expression.h

#ifndef _EXPRESSION_h
#define _EXPRESSION_h

#if defined(ARDUINO)
	#include "Arduino.h"
#endif

#include "SScriptCommon.h"

class Expression
{
 protected:

    // for now all elements, i.e., variable-indexes, function-indexes, and constants are integers
    int32_t *elements;
    int32_t elementCount;

 public:

     ~Expression();
     int32_t set(char *s);

     int32_t execute();

};

#endif
