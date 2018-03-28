//
//
//

#include "SScript.h"

SScript *sScript;

SScript::SScript() {

    variableCount = 0;
    variables = NULL; //new int32_t[variableCount];

    stringCount = 0;
    strings = NULL;

    stateCount = 0;
    states = NULL; //new State[stateCount];

}

SScript::~SScript() {

   if ( variables != NULL && _variables == NULL)
      delete[] variables;

   if ( strings != NULL && _strings == NULL)
      delete[] strings;

   if ( states != NULL && _states == NULL)
      delete[] states;

}

int32_t SScript::setFunctions(void(*(*_functions))()) {

    functions = _functions;

    DEBUG_PRINT("setFunctions()\n");
    return 0;

}

int32_t SScript::set(char *buffer, int32_t *__variables, String *__strings, State *__states) {

    // if _variables == NULL, allocate new array -> remove if reconfiguration
    //      same goes for _strings & _states
    DEBUG_PRINT("SScript::set");

    char *s = buffer;
    str = buffer;
    // allocate variables
    variableCount = getInt();
    DEBUG_PRINT("variableCount:%d\n", variableCount);
    DEBUG_PRINT("delete[] variables\n");
    if (variables != NULL && _variables == NULL) {
        delete[] variables;
    }
    // DEBUG_PRINT(variableCount);
    if (__variables == NULL) {
      variables = new int32_t[variableCount];
      for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;
    } else {
      // IF shared variables with for example another SScript instance
      // TODO: check that the sizes match?
      variables = __variables;
    }
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
    if ( strings != NULL && _strings == NULL) {
        delete[] strings;
    }

    if (__strings == NULL) {
      strings = new String[stringCount];
      for (int32_t i = 0; i < stringCount; i++) strings[i] = String(" ");
    } else {
      strings = __strings;
    }
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
    if (states != NULL && _states == NULL) {
        delete[] states;
    }
    if (__states == NULL) {
       states = new State[stateCount];
       // initialize states
       DEBUG_PRINT("Initialize states\n");
       for (int32_t i = 0; i < stateCount; i++) {
           states[i].set(s);
       }
    } else {
       states = __states;
       DEBUG_PRINT("Initialize states (_states != NULL)\n");
       for (int32_t i = 0; i < stateCount; i++) {
           // if states[i].expressionCount == 0:
           //   the state is not modified
           //   Otherwise, the state is modified
           // which means, set the states you do not want to modify to []
           states[i].set(s);
       }
    }

    // store _variables, _strings & _states for delete purposes
    _variables = __variables;
    _strings = __strings;
    _states = __states;

}

void SScript::executeState(int32_t index) {

    states[index].execute();

}

void SScript::loop() {

    if (stateCount > 0) { // if configured with states
        executeState(0);
    }
}
