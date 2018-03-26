#ifndef _SESP8266_h
#define _SESP8266_h

#include "SConf.h"

// HOX! This file is not polished and is not the final version.
// This includes only helper functions for now.
//   More will probably come in the future.

String *generateAndGetRequestString();
void esp_setRequestString();
// esp_setRequestStringGenerator is used to set the SScript instance and state,
// which will be executed when generateAndGetRequestString is called. This is a
// example of sending messages to specific SScript instances and receiving
// information from it in return. The same kind of techinque can be used to
// share information (for example variable values, strings, etc, depending
// on need.)
void esp_setRequestStringGenerator();

#define SESP_FUNCTIONS_ALL esp_setRequestString, \
    esp_setRequestStringGenerator

#endif
