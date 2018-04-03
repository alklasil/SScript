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
    FUNCTION_LEFT_NOPARSE
    requestString = sScript->strings[*leftValue];
    FUNCTION_END
}

void esp_setRequestStringGenerator() {
   FUNCTION_LEFT_NOPARSE;
   requestStringGeneratorSscript = sScript;
   requestStringGeneratorStateNum = *leftValue;
   FUNCTION_END
}

void esp_setRequestStringHTMLWithTime() {
   // esp_setRequestStringHTML(#requestString, #timeOffset)
   int32_t *str = FUNCTION_ONE_NOPARSE;
   int32_t *timeOffset_millis = FUNCTION_ONE_NOPARSE;

   requestString = "";
   requestString += "<script>";
   requestString += "function f(o) {";
   requestString += "    document.getElementById('s').innerHTML = new Date(new Date().getTime() - o) + ': ' + " + sScript->strings[*str] + ";";
   requestString += "}";
   requestString += "</script>";
   requestString += "<body onload='f('>" + sScript->strings[*timeOffset_millis] + ")'>";
   requestString += "<p id='s'>df</p>";

   FUNCTION_END
}
