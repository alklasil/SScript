// Expression.h

#ifndef _EXPRESSION_h
#define _EXPRESSION_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "wprogram.h"
#elif defined(ARDUINO)
	#include "WProgram.h"
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

     int32_t *nextElement(int32_t *element);
     int32_t execute();

};

#endif
