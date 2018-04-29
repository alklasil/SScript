/*
 Name:		teensySoftware.ino
 Created:	1/25/2018 10:55:16 PM
 Author:	aleksi

 Used sources for code:
  * ESP8266 by Wozzy: see https://forum.pjrc.com/threads/27850-A-Guide-To-Using-ESP8266-With-TEENSY-3
  * SScript: see https://github.com/alklasil/SScript
*/

#include <SScript.h>
#include <SScriptconf\SConf.h>
#include <SScriptconf\SStd.h>
#include <SScriptconf\SMpu9250.h>
#include <SScriptconf\SEsp8266.h>
#include <SScriptconf\SSdcard.h>

SScript _sScript;

void(*functions[])() = {
  // std
  SSTD_FUNCTIONS_ALL,
  // sensor read
  SMPU_FUNCTIONS_ALL,
  // webServer
  SESP_FUNCTIONS_ALL,
  // sdcard
  SSDCARD_FUNCTIONS_ALL
};

void(*(*__functions))() = functions;

void setup() {
  Serial.println("begin setup.");

  // usb
  Serial.begin(9600);

  // ESP
  Serial1.begin(115200);
  while (!Serial1) {}
  webserver_setup();

  // sd-card
  _sdcard_setupSdCard(15); // _chipSelect = 15

  // SScript
  sScript = &_sScript;
  sScript->setFunctions(__functions);

  Serial.println("end setup.");
}

void loop() {
  // get -> serve html page.
  // post -> configure.
  webserver_loop();

  // if configured, run configuration.
  sScript->loop();
}
