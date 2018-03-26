#ifndef _SMPU9250_h
#define _SMPU9250_h

#include "SConf.h"

#if defined(ARDUINO)
   #include "MPU9250.h"
#endif

void mpu_readSensor();

#if !defined(ARDUINO)

int32_t sensorValue(int32_t *rightValue, int32_t avg, int32_t range, int32_t speed);

#endif

void mpu_getAccelX_mss();
void mpu_getAccelY_mss();
void mpu_getAccelZ_mss();
void mpu_getGyroX_rads();
void mpu_getGyroY_rads();
void mpu_getGyroZ_rads();
void mpu_getMagX_uT();
void mpu_getMagY_uT();
void mpu_getMagZ_uT();
void mpu_getTemperature_C();

#define SMPU_FUNCTIONS_ALL mpu_readSensor, \
    mpu_getAccelX_mss, \
    mpu_getAccelY_mss, \
    mpu_getAccelZ_mss, \
    mpu_getGyroX_rads, \
    mpu_getGyroY_rads, \
    mpu_getGyroZ_rads, \
    mpu_getMagX_uT, \
    mpu_getMagY_uT, \
    mpu_getMagZ_uT, \
    mpu_getTemperature_C

#endif
