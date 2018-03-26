#ifndef _SSDCARD_h
#define _SSDCARD_h

#include "SConf.h"

#if defined(ARDUINO)
    #include <SPI.h>
    #include "SdFat.h"
#endif

//
// TODO: clearer interface (for now, it is enough that this works)
//

// if direct access is required
#if defined(ARDUINO)
void _sdcard_setupSdCard(uint8_t _chipSelect);
void _sdcard_open(const char *filename);
void _sdcard_reopen(const char *filename);
void _sdcard_write(const char *buf);
void _sdcard_clear();
void _sdcard_read(char *buf);
void _sdcard_readString(String *str);
void _sdcard_close();

// for testing
void _sdcard_testWriteRead();
void _sdcard_loop();

#endif

// SSCRIPT
void sdcard_open();
void sdcard_reopen();
void sdcard_write();
void sdcard_readString();
void sdcard_close();

#define SSDCARD_FUNCTIONS_ALL  sdcard_open, \
    sdcard_reopen, \
    sdcard_write, \
    sdcard_readString, \
    sdcard_close



#endif
