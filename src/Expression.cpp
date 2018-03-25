//
//
//

#include "SScript.h"
#include "Expression.h"

Expression::~Expression() {

    delete[] elements;

}

int32_t Expression::set(char *s) {

    elementCount = getInt();
    elements = new int32_t[elementCount];
    DEBUG_PRINT("elements: %d\n", elementCount);

    for (int32_t i = 0; i < elementCount; i++) {
        elements[i] = getInt();
        DEBUG_PRINT("element[%d]: %d\n", i, elements[i]);
    }
}

int32_t Expression::execute() {
   sScript->element = &elements[0];

   while ((sScript->element - &elements[elementCount-1]) <= 0) {
      //printf("execute %d %d %d\n", *sScript->element, *(sScript->element + 1), *(sScript->element + 2));
      //getchar();
      // TODO: enable function pointers
      //printf("_begin_");
      //printf("Expression::execute: %d|%d|%d", *sScript->element, elements[*(sScript->element + 1)], elements[*sScript->parseIndex(sScript->element + 2)]);
      //printf("_end_\n");
      //Serial.println("_functions[*sScript->element](); begin");
      //Serial.println(*sScript->element);
      _functions[*sScript->element]();
      //Serial.println("_functions[*sScript->element](); end");
      //printf("_after_\n");
      // TODO: 0.2: remove abortExpressionExecution
      //            It is enough to simply set sScript->element = &elements[elementCount]
      if (sScript->abortExpressionExecution != 0) {
          // reset sScript->abortExpressionExecution -> other expressions
          // can be executed correctly
          sScript->abortExpressionExecution = 0;
          return 1;

      }
   }

   return 0;

#ifdef NOT_DEFINED

    int32_t *functionIndex;
    int32_t *rightValue;
    int32_t *leftValue;

    // There are always at least 1 elements:
    // leftValue must alywas be of mode pointer, it does not care about accessMode (-> somewhat restricted self modification of scripts, but faster)
    if (elementCount >= 3) { // "0 1" -> variables[0] = variables[1] or 1, TODO: perhaps combine this and the branch below into one -> clearer
        leftValue = &elements[0];
        leftValue = parseIndex(leftValue);
        // leftValue = &sScript->variables[*leftValue];
        // There can be more elements though
        for (int32_t i = 1; i < elementCount; i += 2) {
            rightValue = &elements[i];
            functionIndex = &elements[i + 1];
            rightValue = parseIndex(rightValue);
            _functions[*functionIndex](leftValue, rightValue);
            // printf("...%d...%d...%d/%d...%d\n", sScript->abortExpressionExecution, *functionIndex, i, elementCount, elements[i]);

            if (sScript->abortExpressionExecution != 0) {
                // reset sScript->abortExpressionExecution -> other expressions
                // can be executed correctly
                sScript->abortExpressionExecution = 0;
                return 1;

            }

        }
    } else {
      if (elementCount == 1) {
         // if elementCount == 1: always only a function
         leftValue = rightValue = functionIndex = &elements[0];
         _functions[*functionIndex](leftValue, rightValue);
         // there is nothing to set, simply return
         return 2;
      } else if (elementCount == 2) {
         //  (variable = constant)
         leftValue = &elements[0];
         leftValue = parseIndex(leftValue);
         rightValue = &elements[1];
         *leftValue = *rightValue;
      }
   }

   return 0;

#endif
}
