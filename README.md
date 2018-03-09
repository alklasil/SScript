= SScript scripting Library for Arduino =

* SScript is a relatively high performance scripting library.
* The library enables the use of gustom c++ functions easily.
* The compiler is coded in python for ease of use.
* The 'intepreter' is coded in c++ for performance.
* SScript is a close cousing of [S2Script](https://github.com/alklasil/S2Script)
* TODO: separate stdFunctions & stdVariables from gustomFunctions & gustomVariables

### Hello world

#### Script file:

```python
"""Print in a loop."""
from src.SProgram import SProgram as program


def main():
    """Print 'Hello world!' int(count) in a loop."""
    # program
    p = program(
        variableNameValuePairs=[
            # initialize count = 0
            "count"
            # initialize count = 1
            # ("count", 1)
            # create list("count", 3) (= count[0], count[1], count[2])
            # ["count", 3]
        ],
        # set strings
        stringNameValuePairs=[
            ("helloworld_str", "Hello world! "),
        ],
        # set frames/second = 1
        #   (How to set fps for invidual states: See timerTest)
        #   (i.e., simple multithreading)
        fps=1,
        # program (state, [expressions])
        program=[
            ("main", [
                # increase count by one
                ["inc", "count"],
                # print("Hello world!", endl=False)
                ["printString", "helloworld_str"],
                # print(count, endl = True)
                ["printInt", "count", True],
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
```

#### Script compilation:

```bash
$ python3 simpleHelloworld.py

INITIALIZING PROGRAM...

states:
('main', [['readTimer'], ['timeout', '_lastTimedOut', '_timeoutLength'], ['inc', 'count'], ['printString', 'helloworld_str'], ['printInt', 'count', True]])

variables:
[['_lastTimedOut', ('_timeoutLength', 1000), 'count'], [('helloworld_str', 'Hello world! ')]]

PROGRAM INITIALIZED

COMPILING...

states:1
 state(0) expressions: 5
   expression(0) elements: 1 [13]
   expression(1) elements: 3 [27 28 15]
   expression(2) elements: 3 [29 3 0]
   expression(3) elements: 3 [2 30 29]
   expression(4) elements: 3 [2 29 28]

COMPILED...

31 3 3 1 4 0 28 1000 1 1 0 Hello world! ; 1 5 1 13 3 27 28 15 3 29 3 0 3 2 30 29 3 2 29 28

```

##### C++ file (example)

```c++
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
```

#### C++ compile
Platform depended. Can be compiled for arduino and linux (windows not supported yet).
 
#### (C++ test) compile (example)

```bash
$ g++ *.cpp ../src/*.cpp <Other files (such as configuration.cpp, sensors.cpp, etc), depends> -std=c++11 -I ../src -I <Other paths> -o main
```

#### (C++ test) run (DEBUG disabled)

```c++
$ ./main '31 3 3 1 4 0 28 1000 1 1 0 Hello world! ; 1 5 1 13 3 27 28 15 3 29 3 0 3 2 30 29 3 2 29 28'
Hello world! 1
Hello world! 2
Hello world! 3
Hello world! 4
Hello world! 5
Hello world! 6
Hello world! 7
Hello world! 8
Hello world! 9
Hello world! 10
Hello world! 11
Hello world! 12
Hello world! 13
Hello world! 14
Hello world! 15
...
```

#### Performance

* HOX! Performance depends on the platform, the script used and the SScript version used. 
* HOX! Printing the characters to the concole slows the execution down.
* HOX! The script file was modified (fps=None, which means there is no active fps limiter). 

##### On a laptop
 * Intel(R) Core(TM) i3-5010U CPU @ 2.10GHz
 * Ubuntu 16.04

```bash
$ time ./main '29 2 3 1 4 0 1 1 0 Hello world! ; 1 3 3 27 3 0 3 2 28 29 3 2 27 28'
...
Hello world! 1018421
Hello world! 1018422
Hello world! 1018423
Hello world! 1018424
Hello world! 1018425
Hello world! 1018426
Hello world! 1018427
Hello world! 1018428
Hello world! 1018429
Hello world! 1018430
Hello world! 1018431
^C

real	0m7.634s
user	0m1.123s
sys	0m4.494s

vs (while(1) cout << "Hello world! " << i++ << endl;)

Hello world! 1022510
Hello world! 1022511
Hello world! 1022512
Hello world! 1022513^C

real	0m5.618s (or ~7.5 if flush after "Helloworld!")
user	0m0.593s
sys	0m2.681s

conclusion: The performance is good.
 TODO: make flush optional in printString, as that is what causes the 2s difference in execution time.
 TODO: This test is not conclusive, as the real slowdown here is caused py printing the data.
       (would require different kind of test for conclusive result, perhaps in the future).
       Nevertheless, the performance is good enough for now, optimizations can be done in the future by flattening call stack (for example indirect function calls, etc..), but that is not required for now.
       
```

###### On a teensy3.2 board (coming...)


#### Example configuration file (provided in a configuration c++ file, e.g., configuration.cpp)

* Configuration file provides the functions for SScript.
* HOX! all the functions definitions are not shown. 

*ESPConfiguration.cpp*
```c++
#include "ESPConfiguration.h"

void add(int32_t *leftValue, int32_t *rightValue) { *leftValue += *rightValue; }
void sub(int32_t *leftValue, int32_t *rightValue) { *leftValue -= *rightValue; }
....
void readTimer(int32_t *leftValue, int32_t *rightValue) { ... }
...

void(*functions[])(int32_t *leftValue, int32_t *rightValue) = {
    add,
    sub,
    ...
    readTimer,
    ...
};
```
*ESPConfiguration.h*
```c++
...
extern void(*functions[])(int32_t *leftValue, int32_t *rightValue);
...
```

 * The functions must match the SScript functions defined in STDSfunctions.py and vise versa (at least the order of functions, not neseccarily the names).
 * The functions in STDSfunctions.py are for now hardcoded, this will change in the future. 

*STDSFunctions.py*
```python
...
            self.f = sl([
                sf("+"),                # leftValue += righValue
                sf("-"),
                ...
                sf("readTimer"),
                ...
            ])
...
```

*How to use the functions and configure the device:*

 * HOX! see the c++ (example) file above

```c++
...
  void(*(*_functions))(int32_t *leftValue, int32_t *rightValue) = functions;
  sScript.setFunctions(_functions);
  
  sScript.set(configuration_str); // where configuration_str might be '29 2 3 1 4 0 1 1 0 Hello world! ; 1 3 3 27 3 0 3 2 28 29 3 2 27 28'
```

#### Simple c++ arduino example

* The code is only an example, it is not supposed to do anything fancy.
* The code was tested using DCcduino UNO (see below: test run)

##### Simple c++ arduino example code

```c++
#include <SScript.h>

// functions provided for sScript
//   function prototype must always be: int32_t function_name(int32_t *leftValue, int32_t *rightValue);
void add(int32_t *leftValue, int32_t *rightValue) { *leftValue += *rightValue; }
void printInt_ln(int32_t *leftValue, int32_t *rightValue) {
    Serial.println(*rightValue);
}

// array of function pointers provided for sScript.
//   We only provide the pointer to the array of function ponters for sScript. It can use that to call the functions with indented parameters
void(*functions[])(int32_t *leftValue, int32_t *rightValue) = {
    // basic operations
    add,
    printInt_ln
};

void setup() {
  Serial.begin(9600);
  // Example program (set available functions)
  void(*(*_functions))(int32_t *leftValue, int32_t *rightValue) = functions;
  sScript.setFunctions(_functions);
  // Example program (configure):
  // 1 variables, 
  // 1 variable initializations
  // 0 2 set variables[0] = 2
  // 0 strings, 
  // 0 string initializations,
  // 1 state
  // 2 expressions
  // 3 elements (
  //   0 variables[0] 
  //   0 variables[0]
  //   0 = add (The functions that adds leftValue and rightValue & stores the result into leftValue)
  //     (in this case: variables[0] += variables[0];)
  // 3 elements (
  //    0 variables[0] [left value does not matter, but is required for > 1 element expressions, 2 elements -> constant set], 1 element -> function without arguments
  //    0 variables[0] (the variable that gets printed)
  //    1 printInt_ln (the function, that prints variables[0])
  //     (in this case: Serial.println(variables[0]))
  char buffer[] = "1 1 0 2 0 0 1 2 3 0 0 0 3 0 0 1";
  sScript.set(buffer);
}

void loop() {
  // Example program (loop):
  //    variables[0] += variables[0];
  //    Serial.println(variables[0]);
  sScript.loop();
}

//   (coming SOON...)
// Support for external libraries in the compiler is coming. for now though, it is required for the configuration_str to be assembled/compiled by hand

```
##### Simple c++ arduino example test run (DCcduino UNO)
```bash
...
256
512
1024
2048
4096
8192
16384
32768
65536
131072
262144
524288
...
Result: OK!
```
##### Simple c++ arduino example test run extra information (DCcduino UNO)
```bash
Used 16% of program memory (max 32256 B)
Used 13% (270 B) of dynamic memory by global variables, leaves 1778 B for local variables (max 2048 B).
   (most of the memory is used by the configuration buffer)
   (The buffer must be dynamic, or at least not constant, as that would defead the purpose (scripting, reconfiguring))
Used ~100 B of dynamic memory by local variables when configured.

conclusion:
   sScript does not require much memory and the memory usage is likely to be even less in the future.
   execution is fast even with somewhat lower end hardware.

More testing:

char buffer[] = "1 1 0 2 0 0 1 40 3 0 0 0 3 0 0 1 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 1 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0 3 0 0 0";
(Works fine, with 80 expressions worked too, but it's really too little memory to work with comfortably, and some artifacts are to be expected [see below optional way of interpreting the script {TODO}])

conclusion:
   optionally enabled "assenbly line" interpreter todo in the future, as buffer may take too much space
   (idea: until(lastElementReceived) receive 1 element at a time, interpret it
```

For more information about this library please visit us at
https://github.com/alklasil/SScript
