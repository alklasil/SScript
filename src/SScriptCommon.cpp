#include "SScriptCommon.h"

char *getNext(char sep) {

   char *next = strchr(sScript->str, sep);

   if (next != NULL) { // if not last element

      *next = '\0';   // null terminate

      next++;         // move to the beginning og the next element
   }
   return next;
}

int32_t getInt() {

    // s = "int1 int2 int3 int4 int5", we parse int1 and return it as int32_t
    // we only need the buffer ones, after usage, it does not have to be usable anymore

    // return: parsed int32_t.
    // set s = NULL if last_element else next_element

    char *next = getNext(' ');

    int32_t i = atoi(sScript->str);

    sScript->str = next;

    return i;
}

String getString() {
   // strings are separated by ';' in the buffer

   char *next = getNext(';') + 1;
   String s = String(sScript->str);
   sScript->str = next;
   return s;
}
