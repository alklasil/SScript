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

    int32_t *leftValue;
    int32_t *rightValue;
    int32_t *functionIndex;

    // There are always at least 2 elements: leftValue rightValue, often function, default function is *leftValue = *rightValue
    // leftValue must alywas be of mode pointer, it does not care about accessMode (-> somewhat restricted self modification of scripts, but faster)
    leftValue = &elements[0];
    leftValue = &sScript.variables[*leftValue];

    if (elementCount == 2) { // "0 1" -> variables[0] = variables[1] or 1, TODO: perhaps combine this and the branch below into one -> clearer
        rightValue = &elements[1];
        if (sScript.accessMode == sScript.accessModePointer) {
            rightValue = &sScript.variables[*rightValue];
        }
    } else {
        // There can be more elements though
        for (int32_t i = 1; i < elementCount; i += 2) {

            rightValue = &elements[i];
            functionIndex = &elements[i + 1];

            if (sScript.accessMode == sScript.accessModePointer) {

                rightValue = &sScript.variables[*rightValue];
                _functions[*functionIndex](leftValue, rightValue);

            }
            else if (sScript.accessMode == sScript.accessModeValue) {

                _functions[*functionIndex](leftValue, rightValue);

            }

            if (sScript.abortExpressionExecution != 0) {

                return -1;

            }

        }
    }

    *leftValue = *rightValue;
    return 0;

}
