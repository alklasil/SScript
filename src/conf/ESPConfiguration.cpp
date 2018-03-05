//
//
//
#include "ESPConfiguration.h"

// basic operations
void add(int32_t *leftValue, int32_t *rightValue) { *leftValue += *rightValue; }
void sub(int32_t *leftValue, int32_t *rightValue) { *leftValue -= *rightValue; }
void mul(int32_t *leftValue, int32_t *rightValue) { *leftValue *= *rightValue; }
void div(int32_t *leftValue, int32_t *rightValue) { *leftValue /= *rightValue; }
void set(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void lt(int32_t *leftValue, int32_t *rightValue) { *leftValue = (*leftValue < *rightValue) ? 1 : 0; }
void gt(int32_t *leftValue, int32_t *rightValue) { *leftValue = (*leftValue > *rightValue) ? 1 : 0; }
void eq(int32_t *leftValue, int32_t *rightValue) { *leftValue = (*leftValue == *rightValue) ? 1 : 0; }

// helpers
void executeState(int32_t *leftValue, int32_t *rightValue) { sScript.executeState(*rightValue); };
void _if(int32_t *leftValue, int32_t *rightValue) { if (*rightValue == 0) sScript.abortExpressionExecution = 1; }
void _else(int32_t *leftValue, int32_t *rightValue) { if (*rightValue != 0) sScript.abortExpressionExecution = 1; }
void _abortExpressionExecution(int32_t *leftValue, int32_t *rightValue) { sScript.abortExpressionExecution = 1; };
void _abortStateExecution(int32_t *leftValue, int32_t *rightValue) { sScript.abortStateExecution = 1; };

// sensor read (transform inline void Sernsors::(int &, int) to void (int &, int))
void mpu_readSensor(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getAccelX_mss(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getAccelZ_mss(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getAccelY_mss(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getGyroX_rads(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getGyroY_rads(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getGyroZ_rads(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getMagX_uT(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getMagY_uT(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getMagZ_uT(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }
void mpu_getTemperature_C(int32_t *leftValue, int32_t *rightValue) { *leftValue = *rightValue; }

// timer
void readTimer(int32_t *leftValue, int32_t *rightValue) {
   // offset is not needed in teensy, as the millis() initializes to 0
   static clock_t offset = clock();
   clock_t c = clock() - offset;
   int32_t c_f = (((float)c)/CLOCKS_PER_SEC)*1000;
   sScript.millis = (c_f % LONG_MAX);
}
void getTime(int32_t *leftValue, int32_t *rightValue) {
   *leftValue = sScript.millis;
}
void timeout(int32_t *leftValue, int32_t *rightValue){
   // abort executeState if timeOut
   if (sScript.millis - *leftValue < *rightValue) {
      sScript.abortStateExecution = 1;
   } else {
      *leftValue = sScript.millis;
   }
}

// print
void printInt(int32_t *leftValue, int32_t *rightValue) { printf("%d", *rightValue); }
void printInt_ln(int32_t *leftValue, int32_t *rightValue) { printf("%d\n", *rightValue); }

void(*functions[])(int32_t *leftValue, int32_t *rightValue) = {
    // basic operations
    add,
    sub,
    div,
    mul,
    set,
    lt,
    gt,
    eq,
    // helpers
    executeState,
    _if,
    _else,
    _abortExpressionExecution,
    _abortStateExecution,
    // timer
    readTimer,
    getTime,
    timeout,
    // sensor read
    mpu_readSensor,
    mpu_getAccelX_mss,
    mpu_getAccelY_mss,
    mpu_getAccelZ_mss,
    mpu_getGyroX_rads,
    mpu_getGyroY_rads,
    mpu_getGyroZ_rads,
    mpu_getMagX_uT,
    mpu_getMagY_uT,
    mpu_getMagZ_uT,
    mpu_getTemperature_C,
    // print
    printInt,
    printInt_ln
};
