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

   if ( variables != NULL && lastProvidedVariables == NULL)
      delete[] variables;

   if ( strings != NULL && lastProvidedStrings == NULL)
      delete[] strings;

   if ( states != NULL && lastProvidedStates == NULL)
      delete[] states;

}

int32_t SScript::setFunctions(void(*(*_functions))()) {

    functions = _functions;

    DEBUG_PRINT("setFunctions()\n");
    return 0;

}

int32_t SScript::set(
   char *buffer,
   int32_t *providedVariables,
   String *providedStrings,
   State *providedStates) {

    // if lastProvidedVariables == NULL, allocate new array -> remove if reconfiguration
    //      same goes for lastProvidedStrings & lastProvidedStates
    DEBUG_PRINT("SScript::set");

    char *s = buffer;
    str = buffer;
    // allocate variables
    variableCount = getInt();
    DEBUG_PRINT("variableCount:%d\n", variableCount);
    DEBUG_PRINT("delete[] variables\n");
    if (variables != NULL && lastProvidedVariables == NULL) {
        delete[] variables;
    }
    // DEBUG_PRINT(variableCount);
    if (providedVariables == NULL) {
      variables = new int32_t[variableCount];
      for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;
    } else {
      // IF shared variables with for example another SScript instance
      // TODO: check that the sizes match?
      variables = providedVariables;
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
    if ( strings != NULL && lastProvidedStrings == NULL) {
        delete[] strings;
    }

    if (providedStrings == NULL) {
      strings = new String[stringCount];
      for (int32_t i = 0; i < stringCount; i++) strings[i] = String(" ");
    } else {
      strings = providedStrings;
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
    if (states != NULL && lastProvidedStates == NULL) {
        delete[] states;
    }
    if (providedStates == NULL) {
       states = new State[stateCount];
       // initialize states
       DEBUG_PRINT("Initialize states\n");
       for (int32_t i = 0; i < stateCount; i++) {
           states[i].set(s);
       }
    } else {
       states = providedStates;
       DEBUG_PRINT("Initialize states (lastProvidedStates != NULL)\n");
       for (int32_t i = 0; i < stateCount; i++) {
           // if states[i].expressionCount == 0:
           //   the state is not modified
           //   Otherwise, the state is modified
           // which means, set the states you do not want to modify to []
           states[i].set(s);
       }
    }

    // store lastProvidedVariables, lastProvidedStrings & lastProvidedStates
    // for reconfiguration purposes
    lastProvidedVariables = providedVariables;
    lastProvidedStrings = providedStrings;
    lastProvidedStates = providedStates;

}

void SScript::executeState(int32_t index) {

    states[index].execute();

}

void SScript::loop() {

    if (stateCount > 0) { // if configured with states
        executeState(0);
    }
}
