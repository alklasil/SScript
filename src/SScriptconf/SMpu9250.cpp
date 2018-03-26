#include "SMpu9250.h"

// external sources:
//  * https://github.com/bolderflight/MPU9250

// Mpu is only read via SScript, faster if we introduce it here
#if defined(ARDUINO)
MPU9250 *IMU = NULL;
#endif

// sensor read (transform inline void Sernsors::(int &, int) to void (int &, int))



void mpu_readSensor() {
   // sensors.mpu_readSensor();
#if defined(ARDUINO)
   if (IMU == NULL) {
       IMU = new MPU9250(Wire, 0x68);
       IMU->begin();
   }
   IMU->readSensor();
#endif
   FUNCTION_END
}

#if !defined(ARDUINO)

int32_t sensorValue(int32_t *rightValue, int32_t avg = 0, int32_t range = 10, int32_t speed = 3) {

    static const int32_t accuracy = 10000;
    static float lastVal = 0;

    int32_t randVal = (rand() % (accuracy * 2)) - accuracy;

    lastVal = lastVal + 0.1*speed*(float(randVal) / accuracy);
    if (lastVal < -1) lastVal = -1;
    if (lastVal > 1) lastVal = 1;

    int32_t val = int32_t(lastVal * float(range));

    if (val > range) val = range;
    if (val < -range) val = -range;

    return (avg + val) * (*rightValue);

}

#endif


void mpu_getAccelX_mss() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getAccelX_mss() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getAccelY_mss() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getAccelY_mss() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getAccelZ_mss() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getAccelZ_mss() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getGyroX_rads() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getGyroX_rads() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getGyroY_rads() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getGyroY_rads() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getGyroZ_rads() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getGyroZ_rads() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getMagX_uT() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getMagX_uT() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getMagY_uT() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getMagY_uT() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getMagZ_uT() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   *leftValue = int32_t(IMU->getMagZ_uT() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue);
#endif
   FUNCTION_END
}

void mpu_getTemperature_C() {
   FUNCTION_LEFT_PARSE_RIGHT_PARSE
#if defined(ARDUINO)
   // sensors.mpu_getTemperature_C(leftValue, rightValue);
   *leftValue = int32_t(IMU->getTemperature_C() * (float)(*rightValue));
#else
   *leftValue = sensorValue(rightValue, 15);
#endif
   FUNCTION_END
}
