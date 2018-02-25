#include "SScriptCommon.h"
#include "SScript.h"

void(*(*_functions))(int32_t *leftValue, int32_t *rightValue);

int32_t getInt() {

    // s = "int1 int2 int3 int4 int5", we parse int1 and return it as int32_t
    // we only need the buffer ones, after usage, it does not have to be usable anymore

    // return: parsed int32_t.
    // set s = NULL if last_element else next_element

    int32_t i;
    char *next = strchr(sScript.str, ' ');
    if (next != NULL) { // if not last element
        *next = '\0';   // null terminate
        next++;         // move to the beginning og the next element
    }
    i = atoi(sScript.str);
    sScript.str = next;
    // getchar();
    // DEBUG_PRINT("getInt[%d]\n", i);

    return i;
}
