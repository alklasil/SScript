// webServer.h

#ifndef _WEBSERVER_h
#define _WEBSERVER_h

#if defined(ARDUINO) && ARDUINO >= 100
  #include "wprogram.h"
#elif defined(ARDUINO)
  #include "WProgram.h"
#endif

#include <SScript.h>
#include <SScriptconf\SEsp8266.h>

#define HWSERIAL Serial1
#define SSID  "unknown1"
#define PASS  "cf3609bc"
#define PORT  "15164"
#define OKrn  "OK\r\n"
#define BUFFER_SIZE 2048

class WebServer {
protected:
  //char buffer[BUFFER_SIZE];
  int bufferIndex;
  char *buffer;
  String requestString;
  SScript *requestStringGeneratorSscript;
  int32_t requestStringGeneratorStateNum;
  String header;
  String content;
public:
  WebServer() {
    buffer = new char[BUFFER_SIZE];
    requestString = "";
    requestStringGeneratorSscript = NULL;
    requestStringGeneratorStateNum = 0;
  }
  byte wait_for_esp_response(int timeout, char* term = (char *)("OK\r\n"));
  bool read_till_eol(int timeout);
  void serve_page(int ch_id);
  void setupWiFi();
  void loop();
  void htmlRootPage(String *requestString);
};

extern WebServer webServer;

#endif
