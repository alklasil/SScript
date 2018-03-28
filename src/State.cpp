//
//
//

#include "SScript.h"
#include "State.h"

State::State() {

   expressionCount = 0;
   expressions = NULL;

}

State::~State() {

    delete[] expressions;

}

int32_t State::set(char *s)
{
    expressionCount = getInt();
    DEBUG_PRINT("expressions: %d\n", expressionCount);
    if (expressionCount > 0) {
       if (expressions != NULL) {
          delete[] expressions;
       }
       expressions = new Expression[expressionCount];
       for (int32_t i = 0; i < expressionCount; i++) {
           expressions[i].set(s);
       }
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
