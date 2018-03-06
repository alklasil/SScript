#include <iostream>
#include "SScript.h"
// ESPConfiguration can be changed to another
// The configuration file must provide extern
// functions, nothing else.
// see https://github.com/alklasil/ESP/blob/master/teensySoftware/teensySoftware/ESPConfiguration.cpp
// for more detail
#include "ESPConfiguration.h"

// example configuration (not working anymore, too old):
// ./main "9 4 2 15 3 10 5 1 6 1 4 1 3 6 4 10 1 6 6 4 9 2 4 8 6 3 8 5 13 3 0 5 23 5 7 3 4 0 5 8 6 7 11 4 9 3 4 8 3 1 5 0 3 1 4 24 4 3 8 5 13 3 0 5 23 5 7 2 4 0 6 8 6 7 11 4 9 2 4 8"

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
  //strcpy(buffer, argv[1]);
  //sScript.set(buffer);

  while (1) {

      sScript.loop();

  }

}
