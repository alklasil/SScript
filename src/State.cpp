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
    sScript->lastExpression = &expressions[expressionCount-1];
    for (sScript->expression = &expressions[0]; sScript->expression <= sScript->lastExpression; sScript->expression++) {
        sScript->expression->execute();
    }
    return 0;
}
