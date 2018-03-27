## Compiler for SScript

### Compile

```bash
python3 filename.py
```

### Advanced

#### Memory reduction when using multiple instances of SScript

**Instead of using**
```bash
python3 simpleHelloworld.py
python3 sdcardTest.py
python3 thresholdCounter.py 100 -100 GyroZ_rads 10
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
>>> from simpleHelloworld import main as simpleHelloworldMain
>>> from sdcardTest import main as sdcardTestMain
>>> from thresholdCounter import main as thresholdCounterMain
>>> simpleHelloworldMain(None, [SStd(), SMpu9250(), SSdcard()])
>>> sdcardTestMain(None, [SStd(), SMpu9250(), SSdcard()])
>>> thresholdCounterMain(['100', '-100', 'GyroZ_rads', '10'], [SStd(), SMpu9250(), SSdcard()])
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
