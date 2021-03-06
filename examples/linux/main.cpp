#include <iostream>
#include <stdio.h>
#include <SScript.h>
#include <SConf.h>
#include <SStd.h>
#include <SMpu9250.h>
#include <SEsp8266.h>
#include <SSdcard.h>

// example usage:
// ./main '8 2 3 1 4 0 1 1 0 Hello world! ; 1 3 3 0 6 3 2 20 7 2 18 6'

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

int main(int argc, char* argv[])
{
  if (argc < 2) {
     printf("Usage: %s <CONFIGURATION_1> <CONFIGURATION_2> <CONFIGURATION_N>\n", argv[0]);
     return 1;
  }

  void(*(*_functions))() = functions;

  int32_t sScriptInstanceCount = argc - 1;
  SScript *_sScript = new SScript[sScriptInstanceCount];

  char buffer[1024];
  for (int i = 0; i < sScriptInstanceCount; i++) {

     sScript = &_sScript[i];
     sScript->setFunctions(_functions);
     strcpy(buffer, argv[i + 1]);
     //if (i == 0)
      sScript->set(buffer);
     //else {
      //sScript->set(buffer, _sScript[0].variables, _sScript[0].strings, _sScript[0].states);
     //}
  }

  // HOX! when setting sScript. the buffer gets destroyed
  // If there is a change you may need to reuse the configuration,
  // Do copy it somewhere safe first.
  //  (This approach was chosen due to having limited memory in arduino devices)

  //  (This may change in the future to be optional depending on need and time)
  while (true) {
      // do here what ever you want!
      // for example: check if there are requests for a web page.
      //              or do what ever it is that needs doing.
      for (int i = 0; i < sScriptInstanceCount; i++) {
         sScript = &_sScript[i];
         sScript->loop();
      }
  }

}
