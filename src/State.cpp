//
//
//

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

    for (int32_t i = 0; i < expressionCount; i++) {

        expressions[i].execute();

    }
}
