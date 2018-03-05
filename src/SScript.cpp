//
//
//

#include "SScript.h"

SScript sScript;

SScript::SScript() {

    variableCount = 0;
    variables = new int32_t[variableCount];

    stateCount = 0;
    states = new State[stateCount];

    abortStateExecution = 0;
    abortExpressionExecution = 0;
}

int32_t SScript::setFunctions(void(*(*__functions))(int32_t *leftValue, int32_t *rightValue)) {

    _functions = __functions;

    DEBUG_PRINT("setFunctions()\n");
    return 0;

}

int32_t SScript::set(char *buffer) {

    char *s = buffer;
    str = buffer;

    // allocate variables
    variableCount = getInt();
    DEBUG_PRINT("variableCount:%d\n", variableCount);
    delete[] variables;
    variables = new int32_t[variableCount];
    for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;

    // initialize variables
    int32_t variablesToInitialize = getInt();
    DEBUG_PRINT("variablesToInitialize:%d\n", variablesToInitialize);
    if (variablesToInitialize != 0) {
        for (int32_t i = 0; i < variablesToInitialize; i++) {
            int32_t index = getInt();
            int32_t value = getInt();

            variables[index] = value;
            DEBUG_PRINT("variables[%d]: %d\n", index, variables[index]);
        }
    }

    // allocate states
    stateCount = getInt();
    DEBUG_PRINT("stateCount: %d\n", stateCount);
    delete[] states;
    states = new State[stateCount];

    // initialize states
    DEBUG_PRINT("Initialize states\n");
    for (int32_t i = 0; i < stateCount; i++) {

        states[i].set(s);

    }


}

int32_t SScript::executeState(int32_t index) {

    return states[index].execute();

}

void SScript::loop() {

    // execute "main"-state. the index of "main"-state should always be 0
    // int32_t i = 24; _functions[i](&i, &i); // should print 24 (and does, at least 24.2.2018), i may have changed
    if (stateCount > 0) { // if configured with states
        executeState(0);
    }
}
