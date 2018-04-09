## Compiler for SScript

### Compile

```bash
python3 -m examples.scriptname <arguments>
```


### Syntax


#### Variable, String, Function, State
```
$name -> get function where function.name == name
   e.g., "$mpu_readSensor" -> mpu_readSensor()
@name -> get state where state.name == name
   e.g., "$=(const)=", "state", "@<t>" -> state = <t>
#name -> get string where string.name == name
   e.g., -> "$printString", "#count" -> if "count" = "count: ", then print "count: "
name  -> get variable where variable.name == name
   e.g., "$+", "count", "1" -> count++ (now it is variable, not string)

See for example: thresholdCounter.py for an example
```

---

### Advanced

#### 1.Memory reduction when using multiple instances of SScript

**Instead of using**
```bash
python3 -m examples.simpleHelloworld
python3 -m examples.sdcardTest
python3 -m examples.thresholdCounter 100 -100 GyroZ_rads 10
```
**which would result into**
```c++
#include <SStd.h>

void(*functions[])() = {
   SSTD_FUNCTIONS_ALL
}
```
**and**
```c++
#include <SStd.h>
#include <SSdcard.h>

void(*functions[])() = {
   SSTD_FUNCTIONS_ALL,
   SSDCARD_FUNCTIONS_ALL
}
```
**and**
```c++
#include <SStd.h>
#include <SMpu9250.h>

void(*functions[])() = {
   SSTD_FUNCTIONS_ALL,
   SMPU_FUNCTIONS_ALL
}
```

**One might want to use**
```python
$ python3
>>> from src.conf.SStd import SStd
>>> from src.conf.SMpu9250 import SMpu9250
>>> from src.conf.SSdcard import SSdcard
>>> from examples.simpleHelloworld import main as simpleHelloworldMain
>>> from examples.sdcardTest import main as sdcardTestMain
>>> from examples.thresholdCounter import main as thresholdCounterMain
>>> simpleHelloworldMain(None, [SStd(), SMpu9250(False), SSdcard(False)])
>>> sdcardTestMain(None, [SStd(), SMpu9250(False), SSdcard()])
>>> thresholdCounterMain(['100', '-100', 'GyroZ_rads', '10'], [SStd(), SMpu9250(), SSdcard(False)])
```
**which would result into all the scripts using the same functions pointer array, there by reducing memory among other goodies.**
```c++
#include <SStd.h>
#include <SMpu9250.h>
#include <SSdcard.h>

void(*functions[])() = {
   SSTD_FUNCTIONS_ALL,
   SMPU_FUNCTIONS_ALL,
   SSDCARD_FUNCTIONS_ALL
}
```

#### 2. Memory reduction and performance boost

As longs as there are no if statements in consecutive expressions, the expressions can be merged.

**Instead of (1)**
```
("state", [
   ["$readTimer" ],
   ["$getTime", 'millis' ]
)]
```
**One might want to use (2)**
```
("state", [
   "$readTimer",
   "$getTime", 'millis'
)]
```
**Or (3)**
```
("state", [
   "$readTimer",
   "$getTime", [
      'millis'
   ]
)]
```
**As, 2 and 3 reduce memory & performance requirements.**
