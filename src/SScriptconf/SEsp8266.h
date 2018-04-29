#ifndef _SESP8266_h
#define _SESP8266_h

#if defined(ARDUINO) && ARDUINO >= 100
  #include "wprogram.h"
#elif defined(ARDUINO)
  #include "WProgram.h"
#endif

#include "SConf.h"

#define HWSERIAL Serial1
#define SSID  "unknown1"
#define PASS  "cf3609bc"
#define PORT  "15164"
#define OKrn  "OK\r\n"
#define BUFFER_SIZE 2048

void webserver_setup();
byte webserver_wait_for_esp_response(int timeout, char* term = (char *)("OK\r\n"));
bool webserver_read_till_eol(int timeout);
void webserver_serve_page(int ch_id);
void webserver_setupWiFi();
void webserver_loop();
void webserver_htmlRootPage(String *requestString);

String *generateAndGetRequestString();
void esp_setRequestString();
// esp_setRequestStringGenerator is used to set the SScript instance and state,
// which will be executed when generateAndGetRequestString is called. This is a
// example of sending messages to specific SScript instances and receiving
// information from it in return. The same kind of techinque can be used to
// share information (for example variable values, strings, etc, depending
// on need.)
void esp_setRequestStringGenerator();
//void esp_setRequestStringHTML() {}
void esp_setRequestStringHTMLWithTime();

#define SESP_FUNCTIONS_ALL esp_setRequestString, \
    esp_setRequestStringGenerator, \
    esp_setRequestStringHTMLWithTime

#endif
