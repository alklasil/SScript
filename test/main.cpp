#include <iostream>
#include "SScript.h"
#include "configuration.h"

int main()
{
  // not tested as of yet

  sScript.setFunctions(&functions);

  while (1) {

      sScript.loop();

  }

}
