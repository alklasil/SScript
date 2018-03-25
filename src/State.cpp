//
//
//

#include "SScript.h"
#include "State.h"

State::~State() {

    delete[] expressions;

}

int32_t State::set(char *s)
{

    expressionCount = getInt();
    expressions = new Expression[expressionCount];
    DEBUG_PRINT("expressions: %d\n", expressionCount);

    for (int32_t i = 0; i < expressionCount; i++) {

        expressions[i].set(s);
    }
}

int32_t State::execute() {

    sScript->abortStateExecution = 0;
    for (int32_t i = 0; i < expressionCount; i++) {
        //printf("State::execute: %d", i);
        //Serial.println("expressions[i].execute(); begin");
        expressions[i].execute();
        //Serial.println("expressions[i].execute(); end");
        if (sScript->abortStateExecution) {
           return 1;
        }

    }
    return 0;
}
