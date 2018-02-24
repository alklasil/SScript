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

    accessMode = accessModePointer;
}

int32_t SScript::setFunctions(void(*(*__functions))(int32_t *leftValue, int32_t *rightValue)) {

    _functions = __functions;

}

int32_t SScript::set(char *buffer) {

    char *s = buffer;

    // allocate variables
    variableCount = getInt(s);
    delete[] variables;
    variables = new int32_t[variableCount];
    for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;

    // initialize variables
    int32_t variablesToInitialize = getInt(s);
    if (variablesToInitialize != 0) {
        for (int32_t i = 0; i < variablesToInitialize; i++) {
            int32_t index = getInt(s);
            int32_t value = getInt(s);

            variables[index] = value;
        }
    }

    // allocate states
    stateCount = getInt(s);
    delete[] states;
    states = new State[stateCount];

    // initialize states
    for (int32_t i = 0; i < stateCount; i++) {

        states[i].set(s);

    }


}

int32_t SScript::executeState(int32_t index) {

    return states[index].execute();

}

void SScript::loop() {

    // execute "main"-state. the index of "main"-state should always be 0
    DEBUG_PRINT("executeState(0)\n");
    // int32_t i = 24; _functions[i](&i, &i); // should print 24 (and does, at least 24.2.2018), i may have changed
    if (stateCount > 0) { // if configured with states
        executeState(0);
    }
}
