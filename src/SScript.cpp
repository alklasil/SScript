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

void SScript::allocateVariables(int32_t *variablesMasterNew) {

   DEBUG_PRINT("variableCount:%d\n", variableCount);
   DEBUG_PRINT("delete[] variables\n");

   if (IS_VARIABLES_MASTER) delete[] variables;

   variableCount = getInt();
   DEBUG_PRINT(variableCount);
   if (variablesMasterNew == NULL) {
     variables = new int32_t[variableCount];
     for (int32_t i = 0; i < variableCount; i++) variables[i] = 0;
   } else {
     variables = variablesMasterNew;
   }

   variablesMaster = variablesMasterNew;

}

void SScript::initializeVariables() {

   int32_t variablesToInitialize = getInt();
   DEBUG_PRINT("variablesToInitialize:%d\n", variablesToInitialize);
   if (variablesToInitialize != 0) {
      for (int32_t i = 0; i < variablesToInitialize; i++) {
           int32_t index = getInt();
           variables[index] = getInt();
           DEBUG_PRINT("variables[%d]: %d\n", index, variables[index]);
      }
   }

}


void SScript::allocateStrings(String *stringsMasterNew) {

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

}

void SScript::initializeStrings() {

   int32_t stringsToInitialize = getInt();
   DEBUG_PRINT("stringsToInitialize:%d\n", stringsToInitialize);
   if (stringsToInitialize != 0) {
       for (int32_t i = 0; i < stringsToInitialize; i++) {
           int32_t index = getInt();
           strings[index] = getString();
       }
   }

}

void SScript::allocateStates(State *statesMasterNew) {

   DEBUG_PRINT("stateCount: %d\n", stateCount);

   if (IS_STATES_MASTER) delete[] states;

   stateCount = getInt();
   if (statesMasterNew == NULL) {
      states = new State[stateCount];
   } else {
      states = statesMasterNew;
   }

   statesMaster = statesMasterNew;

}

void SScript::initializeStates() {

   for (int32_t i = 0; i < stateCount; i++) {
       states[i].set(str);
   }

}


int32_t SScript::set(
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

}

void SScript::executeState(int32_t index) {

    states[index].execute();

}

void SScript::loop() {

    if (stateCount > 0) { // if configured with states
        executeState(0);
    }
}
