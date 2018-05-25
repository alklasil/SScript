 * This is simple sscript runner for linux.
 * To use this to run scripts for configuration modules (such as sensors, sd-card, esp8266 and so on), the modules must provide either dummy or simulated functions (or drivers for the hardware for linux, or proxys/runners for teensy/arduino boards (relatively simple to implement)). The required functionality is provided by the currently existing modules.

 * HOX! this is still work in progress (though functional), as the repo needs some refactoring.

### compile
```bash
$ g++ -g *.cpp ../../src/*.cpp ../../src/SScriptconf/*.cpp  -std=c++11 -I ../../src -I ../../src/SScriptconf -o main
```

### run
```bash
$ ./main <compiled scripts>
```
