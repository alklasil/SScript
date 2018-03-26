#include "SEsp8266.h"

// external sources:
//  * https://forum.pjrc.com/threads/27850-A-Guide-To-Using-ESP8266-With-TEENSY-3

String requestString;
SScript *requestStringGeneratorSscript;
int32_t requestStringGeneratorStateNum;

String *generateAndGetRequestString(){

   if (requestStringGeneratorSscript == NULL)
      return &requestString;
   SScript *_sScript = sScript;
   sScript = requestStringGeneratorSscript;

   //
   // requestStringGeneratorSscript, requestStringGeneratorState
   //   should set requestString
   (*sScript).executeState(requestStringGeneratorStateNum);

   sScript = _sScript;
   return &requestString;

}

void esp_setRequestString() {
    FUNCTION_LEFT_PARSE
    requestString = sScript->strings[*leftValue];
    FUNCTION_END
}

void esp_setRequestStringGenerator() {
   int32_t *val = FUNCTION_ONE_PARSE;
   requestStringGeneratorSscript = sScript;
   requestStringGeneratorStateNum = *val;
   FUNCTION_END
}
