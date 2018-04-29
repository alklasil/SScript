//
//
//

#include "SScript.h"

// master = has items and does not have masterItems
#define IS_VARIABLES_MASTER (variables != NULL && variablesMaster == NULL)
#define IS_STRINGS_MASTER (variables != NULL && variablesMaster == NULL)
#define IS_STATES_MASTER (variables != NULL && variablesMaster == NULL)

SScript *sScript;

SScript::SScript() {

    variableCount = 0;
    variables = NULL;

    stringCount = 0;
    strings = NULL;

    stateCount = 0;
    states = NULL;

}



SScript::~SScript() {

   if (IS_VARIABLES_MASTER) delete[] variables;
   if (IS_STRINGS_MASTER) delete[] strings;
   if (IS_STATES_MASTER) delete[] states;

}


int32_t SScript::setFunctions(void(*(*_functions))()) {

   DEBUG_PRINT("setFunctions()\n");
   functions = _functions;
   return 0;

}

char * SScript::allocateVariables(int32_t *variablesMasterNew) {

   DEBUG_PRINT("variableCount:%d\n", variableCount);
   DEBUG_PRINT("delete[] variables\n");

   if (IS_VARIABLES_MASTER) delete[] variables;

   variableCount = getInt();
   if (variablesMasterNew == NULL) {
     variables = new int32_t[variableCount];
     for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;
   } else {
     variables = variablesMasterNew;
   }

   variablesMaster = variablesMasterNew;

   return str;
}

char * SScript::initializeVariables() {

   int32_t variablesToInitialize = getInt();
   DEBUG_PRINT("variablesToInitialize:%d\n", variablesToInitialize);
   if (variablesToInitialize != 0) {
      for (int32_t i = 0; i < variablesToInitialize; i++) {
           int32_t index = getInt();
           variables[index] = getInt();
           DEBUG_PRINT("variables[%d]: %d\n", index, variables[index]);
      }
   }

   return str;
}


char * SScript::allocateStrings(String *stringsMasterNew) {

   DEBUG_PRINT("stringCount:%d\n", stringCount);

   if (IS_STRINGS_MASTER) delete[] strings;

   stringCount = getInt();
   if (stringsMasterNew == NULL) {
     strings = new String[stringCount];
     for (int32_t i = 0; i < stringCount; i++) strings[i] = String(" ");
   } else {
     strings = stringsMasterNew;
   }

   stringsMaster = stringsMasterNew;

   return str;
}

char * SScript::initializeStrings() {

   int32_t stringsToInitialize = getInt();
   DEBUG_PRINT("stringsToInitialize:%d\n", stringsToInitialize);
   if (stringsToInitialize != 0) {
       for (int32_t i = 0; i < stringsToInitialize; i++) {
           int32_t index = getInt();
           strings[index] = getString();
       }
   }

   return str;
}

char * SScript::allocateStates(State *statesMasterNew) {

   DEBUG_PRINT("stateCount: %d\n", stateCount);

   if (IS_STATES_MASTER) delete[] states;

   stateCount = getInt();
   if (statesMasterNew == NULL) {
      states = new State[stateCount];
   } else {
      states = statesMasterNew;
   }

   statesMaster = statesMasterNew;

   return str;
}

char * SScript::initializeStates() {

   for (int32_t i = 0; i < stateCount; i++) {
       states[i].set(str);
   }

   return str;
}

void SScript::setStr(char *buffer) {
   str = buffer;
}

char * SScript::set(
    char *buffer,
    int32_t *variablesMasterNew,
    String *stringsMasterNew,
    State *statesMasterNew) {

    DEBUG_PRINT("SScript::set");

    str = buffer;

    allocateVariables(variablesMasterNew);
    initializeVariables();

    allocateStrings(stringsMasterNew);
    initializeStrings();

    allocateStates(statesMasterNew);
    initializeStates();

    return str;
}

void SScript::executeState(int32_t index) {

    states[index].execute();

}

void SScript::loop() {

    if (stateCount > 0) { // if configured with states
        executeState(0);
    }
}
