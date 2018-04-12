#include "SStd.h"

// basic operations
void add() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue += *rightValue;
   FUNCTION_END
}

void sub() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue -= *rightValue;
   FUNCTION_END
}

void mul() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue *= *rightValue;
   FUNCTION_END
}

void div() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue /= *rightValue;
   FUNCTION_END
}

void set() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue = *rightValue;
   FUNCTION_END
}

void set_const() {
   FUNCTION_LEFT_PARSE_RIGHT_NOPARSE
   *leftValue = *rightValue;
   FUNCTION_END
}

void lt() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue = (*leftValue < *rightValue) ? 1 : 0;
   FUNCTION_END
}

void gt() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue = (*leftValue > *rightValue) ? 1 : 0;
   FUNCTION_END
}

void eq() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue = (*leftValue == *rightValue) ? 1 : 0;
   FUNCTION_END
}

void neq() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   *leftValue = (*leftValue != *rightValue) ? 1 : 0;
   FUNCTION_END
}

void maxXYZ() {
   int32_t *storeHere = FUNCTION_ONE_PARSE
   int32_t *x = storeHere + 1;
   int32_t *y = storeHere + 2;
   int32_t *z = storeHere + 3;
   *storeHere = *x;
   if (*y > *storeHere) *storeHere = *y;
   if (*z > *storeHere) *storeHere = *z;
   FUNCTION_END
}

void sumXYZ() {
   int32_t *storeHere = FUNCTION_ONE_PARSE
   int32_t *x = storeHere + 1;
   int32_t *y = storeHere + 2;
   int32_t *z = storeHere + 3;
   *storeHere = *x + *y + *z;
   FUNCTION_END
}

// helpers
void executeState() {
   FUNCTION_LEFT_PARSE

   // set return 'address
   int32_t *_element = sScript->element;
   int32_t *_lastElement = sScript->lastElement;
   Expression *_expression = sScript->expression;
   Expression *_lastExpression = sScript->lastExpression;

   sScript->executeState(*leftValue);

   // return
   sScript->element = _element;
   sScript->lastElement = _lastElement;
   sScript->expression = _expression;
   sScript->lastExpression = _lastExpression;

   FUNCTION_END
}

void _if() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   if (*rightValue != *leftValue) {
      sScript->element = sScript->lastElement + 1;
   } else {
     FUNCTION_END
   }
}

void _abortExpressionExecution() {
   sScript->element = sScript->lastElement + 1;
}

void _abortStateExecution() {
   sScript->expression = sScript->lastExpression + 1;
   sScript->element = sScript->lastElement + 1;
}

// timer
void readTimer() {
#if defined(ARDUINO)
   sScript->millis_var = millis();
#else
   // offset is not needed in teensy, as the millis() initializes to 0
   //static clock_t offset = clock()/CLOCKS_PER_SEC;
   clock_t c = clock();
   int32_t c_f = int32_t(((float(c)/float(CLOCKS_PER_SEC))*float(1000)));
   sScript->millis_var = c_f; //(c_f % LONG_MAX);
#endif
   FUNCTION_END
}

void getTime() {
   FUNCTION_LEFT_PARSE
   *leftValue = sScript->millis_var;
   FUNCTION_END
}

void timeout(){
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
   // abort executeState if timeOut
   if (sScript->millis_var - *leftValue < *rightValue) {
      sScript->expression = sScript->lastExpression + 1;
      sScript->element = sScript->lastElement + 1;
   } else {
      *leftValue = sScript->millis_var;
      FUNCTION_END
   }
}

// print
void printInt() {
   FUNCTION_LEFT_PARSE
#if defined(ARDUINO)
    Serial.print(*leftValue);
#else
    cout << *leftValue << flush;
#endif
   FUNCTION_END
}

void printInt_ln() {
    // Serial.println("printInt_ln() begin");
   FUNCTION_LEFT_PARSE
#if defined(ARDUINO)
    Serial.println(*leftValue);
#else
    cout << *leftValue << endl;
#endif
   FUNCTION_END
    // Serial.println("printInt_ln() end");
}

void printString() {
   FUNCTION_LEFT_NOPARSE
   #if defined(ARDUINO)
      Serial.print(sScript->strings[*leftValue]);
   #else
      cout << sScript->strings[*leftValue] << flush;
   #endif
   FUNCTION_END
}

void printString_ln() {
   // Serial.println("printString_ln() begin");
   FUNCTION_LEFT_NOPARSE
   #if defined(ARDUINO)
      Serial.println(sScript->strings[*leftValue]);
   #else
      cout << sScript->strings[*leftValue] << endl;
   #endif
   FUNCTION_END
   // Serial.println("printString_ln() end");
}

void clearString() {
   FUNCTION_LEFT_NOPARSE
   sScript->strings[*leftValue] = "";
   FUNCTION_END
}

void concatString_String() {
   FUNCTION_LEFT_PARSE_RIGHT_NOPARSE
   sScript->strings[*leftValue] += sScript->strings[*rightValue];
   FUNCTION_END
}

void concatString_Int() {
   FUNCTION_LEFT_NOPARSE_RIGHT_PARSE
   #if defined(ARDUINO)
      sScript->strings[*leftValue] += String(*rightValue);
   #else
      sScript->strings[*leftValue] += to_string(*rightValue);
   #endif
   FUNCTION_END
}

void concatString_Int_List() {
   // (where to, where from, hoe many) -> "val1, val2, ..., valn"
   // TODO: optimize (for example. first to char* and the to String)
   int32_t *store = FUNCTION_ONE_NOPARSE
   int32_t *to = FUNCTION_ONE_PARSE
   int32_t *from = FUNCTION_ONE_PARSE
   from--;
   while (from++ != to) {
      #if defined(ARDUINO)
         sScript->strings[*store] += String(*from);
      #else
         sScript->strings[*store] += to_string(*from);
      #endif
      if (from != to)
         sScript->strings[*store] += " ";
   }
   FUNCTION_END
}
