#include <iostream>
#include "SScript.h"
// ESPConfiguration can be changed to another
// The configuration file must provide extern
// functions, nothing else.
// see https://github.com/alklasil/ESP/blob/master/teensySoftware/teensySoftware/ESPConfiguration.cpp
// for more detail
#include "ESPConfiguration.h"

// example usage:
// ./main "31 3 3 1 4 0 28 1000 1 1 0 Hello world! ; 1 5 1 13 3 27 28 15 3 29 3 0 3 2 30 29 3 2 29 28"

int main(int argc, char* argv[])
{

  if (argc < 2) {
     printf("Usage: %s %s \n", argv[0], "<CONFIGURATION>");
     return 1;
  }

  void(*(*_functions))(int32_t *leftValue, int32_t *rightValue) = functions;

  sScript.setFunctions(_functions);
  char buffer[1024];
  strcpy(buffer, argv[1]);
  sScript.set(buffer);
  // HOX! when setting sScript. the buffer is destroyed
  // If there is a change you may need to reuse the configuration,
  // Do copy it somewhere safe first.
  //  (This approach was chosen due to having limited memory in arduino devices)
  //  (This may change in the future to be optional depending on need and time)

  while (1) {
      // do here what ever you want!
      // for example: check if there are requests for a web page.
      //              or do what ever it is that needs doing.
      sScript.loop();
  }
}
