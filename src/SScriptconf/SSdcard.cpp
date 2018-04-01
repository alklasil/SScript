#include "SSdcard.h"

// external sources:
//  * https://github.com/greiman/SdFat/blob/master/examples/ReadWrite/ReadWrite.ino

#if defined(ARDUINO)

SdFat sd;
File file;

void _sdcard_setupSdCard(uint8_t _chipSelect) {
    if (!sd.begin(_chipSelect)) {
        Serial.println("initialization failed!");
        return;
    }
}

void _sdcard_open(const char *filename) {

    // open the file. note that only one file can be open at a time,
    // so you have to close this one before opening another.
    file = sd.open(filename, FILE_WRITE);

    if (!file)  {
        // if the file didn't open, print an error:
        Serial.println("error opening filename");
    }
}

void _sdcard_reopen(const char *filename) {

    // open the file. note that only one file can be open at a time,
    // so you have to close this one before opening another.
    file = sd.open(filename);

    if (!file) {
        // if the file didn't open, print an error:
        Serial.println("error opening file from sdcard");
    }

}

void _sdcard_write(const char *buf) {
    file.println(buf);
}

void _sdcard_clear() {
    // TODO
}

void _sdcard_read(char *buf) {
    int i;
    for (i = 0; file.available(); i++) {
        buf[i] = file.read();
    }
    buf[i] = '\0';
}

// optimize me (str += file.read(); is slow)
void _sdcard_readString(String *str) {
    int i;
    for (i = 0; file.available(); i++) {
        *str += file.read();
    }
}

void _sdcard_close() {
    file.close();
}

#if defined(NOT_DEFINED)
void _sdcard_testWriteRead() {
    _sdcard_open("test1.txt");
    if (file) {
        Serial.print("Writing to test1.txt...");
        _sdcard_write("testing 1, 2, 3.");
        // close the file:
        _sdcard_close();
        Serial.println("done.");
    }

    // re-open the file for reading:
    reopen("test1.txt");
    if (file) {
        Serial.println("test1.txt:");

        // read from the file until there's nothing else in it:
        char buf[BUFFER_SIZE];
        _sdcard_read(buf);
        Serial.println(buf);
        // close the file:
        _sdcard_close();
    }
}
#else
void _sdcard_testWriteRead() {
    ;
}
#endif

void _sdcard_loop() {
    ;
}

#endif

// SSCRIPT

void sdcard_open() {
    FUNCTION_LEFT_NOPARSE
#if defined(ARDUINO)
    _sdcard_open(sScript->strings[*leftValue].c_str());
#endif
    FUNCTION_END
}

void sdcard_reopen() {
    FUNCTION_LEFT_NOPARSE
#if defined(ARDUINO)
    _sdcard_open(sScript->strings[*leftValue].c_str());
#endif
    FUNCTION_END
}

void sdcard_write() {
    FUNCTION_LEFT_NOPARSE
#if defined(ARDUINO)
    _sdcard_write(sScript->strings[*leftValue].c_str());
#else
    cout << "(Store on sd-card:[" << sScript->strings[*leftValue].c_str() << "])";
#endif
   FUNCTION_END
}

void sdcard_readString() {
    FUNCTION_LEFT_NOPARSE
#if defined(ARDUINO)
    _sdcard_readString(&sScript->strings[*leftValue]);
#else
    sScript->strings[*leftValue] = "SDCARD data";
#endif
    FUNCTION_END
}

void sdcard_close() {
#if defined(ARDUINO)
    _sdcard_close();
#endif
    FUNCTION_END
}
