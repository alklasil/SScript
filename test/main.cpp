#include <iostream>
#include "SScript.h"
#include "Configuration.h"

int main()
{
  // not tested as of yet

  void(*(*_functions))(int32_t *leftValue, int32_t *rightValue) = functions;

  sScript.setFunctions(_functions);

  while (1) {

      sScript.loop();

  }

}
