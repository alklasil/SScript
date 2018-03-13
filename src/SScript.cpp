//
//
//

#include "SScript.h"

SScript sScript;

SScript::SScript() {

    variableCount = 0;
    variables = NULL; //new int32_t[variableCount];

    stringCount = 0;
    strings = NULL;

    stateCount = 0;
    states = NULL; //new State[stateCount];

    abortStateExecution = 0;
    abortExpressionExecution = 0;
}

int32_t SScript::setFunctions(void(*(*__functions))(int32_t *leftValue, int32_t *rightValue)) {

    _functions = __functions;

    DEBUG_PRINT("setFunctions()\n");
    return 0;

}

int32_t SScript::set(char *buffer) {
    DEBUG_PRINT("SScript::set");

    char *s = buffer;
    str = buffer;
    // allocate variables
    variableCount = getInt();
    DEBUG_PRINT("variableCount:%d\n", variableCount);
    DEBUG_PRINT("delete[] variables\n");
    if (variables != NULL)
        delete[] variables;

    DEBUG_PRINT(variableCount);
    variables = new int32_t[variableCount];
    for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;

    // initialize variables
    int32_t variablesToInitialize = getInt();
    DEBUG_PRINT("variablesToInitialize:%d\n", variablesToInitialize);
    if (variablesToInitialize != 0) {
        for (int32_t i = 0; i < variablesToInitialize; i++) {
            int32_t index = getInt();
            variables[index] = getInt();
            DEBUG_PRINT("variables[%d]: %d\n", index, variables[index]);
        }
    }

    // allocate strings
    stringCount = getInt();
    DEBUG_PRINT("stringCount:%d\n", stringCount);
    if (strings != NULL)
        delete[] strings;
    strings = new String[stringCount];
    for (int32_t i = 0; i < stringCount; i++) strings[i] = String(" ");

    // initialize strings
    int32_t stringsToInitialize = getInt();
    DEBUG_PRINT("stringsToInitialize:%d\n", stringsToInitialize);
    if (stringsToInitialize != 0) {
        for (int32_t i = 0; i < stringsToInitialize; i++) {
            int32_t index = getInt();
            strings[index] = getString();
            // cout << strings[index] << endl;
            //DEBUG_PRINT("strings[%d]: %d\n", index, strings[index]);
        }
    }
    // allocate states
    stateCount = getInt();
    DEBUG_PRINT("stateCount: %d\n", stateCount);
    if (states != NULL)
        delete[] states;
    states = new State[stateCount];

    // initialize states

    DEBUG_PRINT("Initialize states\n");
    for (int32_t i = 0; i < stateCount; i++) {

        states[i].set(s);

    }

}

void SScript::executeState(int32_t index) {

    states[index].execute();

}

void SScript::loop() {
    // Serial.println("a");

    // execute "main"-state. the index of "main"-state should always be 0
    // int32_t i = 24; _functions[i](&i, &i); // should print 24 (and does, at least 24.2.2018), i may have changed
    if (stateCount > 0) { // if configured with states

#if defined(ARDUINO) // for testing, remove when ok (TODO)
        static auto lastTime = millis();
        auto _time = millis();
        if (_time - lastTime > 30) {
            lastTime = _time;
            executeState(0);
        }
#else
        executeState(0);
#endif
    }
}
