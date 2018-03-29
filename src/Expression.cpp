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
   if (elementCount == 0)
      return 1;

   sScript->element = &elements[0];
   sScript->lastElement = &elements[elementCount-1];

   while ((sScript->element - sScript->lastElement) <= 0) {
      sScript->functions[*sScript->element]();
   }

   return 0;
}
