"""Helper module for accessing functions."""
from src.SFunction import SFunction
from src.SVariable import SVariable


class SMpu9250:
    """Standard functions class for SScript."""
    def __init__(self, useVariables=True):
        self.useVariables = useVariables

    def getFunctions(self):
        """"Return a list of functions by mpu9250."""
        return [
            SFunction("mpu_readSensor"),
            SFunction("mpu_getAccelX_mss"),
            SFunction("mpu_getAccelY_mss"),
            SFunction("mpu_getAccelZ_mss"),
            SFunction("mpu_getGyroX_rads"),
            SFunction("mpu_getGyroY_rads"),
            SFunction("mpu_getGyroZ_rads"),
            SFunction("mpu_getMagX_uT"),
            SFunction("mpu_getMagY_uT"),
            SFunction("mpu_getMagZ_uT"),
            SFunction("mpu_getTemperature_C")
        ]

    def getVariables(self, sdict):
        """Return list of variables by mpu9250."""
        if not self.useVariables:
            return []

        return [
            # basic variables
            # If you do not use stdVariables, the first variable is not allowed
            # to be a list
            # sensor variables
            # accelerometer
            SVariable("Accel_mss"),              # amplitude of [x,y,z]
            SVariable("AccelX_mss"),             # amplitude in x-direction
            SVariable("AccelZ_mss"),             # amplitude in z-direction
            SVariable("AccelY_mss"),             # amplitude in y-direction

            # gyroscope
            SVariable("Gyro_rads"),
            SVariable("GyroX_rads"),
            SVariable("GyroY_rads"),
            SVariable("GyroZ_rads"),

            # magnetometer
            SVariable("Mag_uT"),
            SVariable("MagY_uT"),
            SVariable("MagX_uT"),
            SVariable("MagZ_uT"),

            # temperature
            SVariable("Temperature_C"),
        ]

    def firstVariable(self):
        """Return the first variable. Can be used in indexing lists."""
        return "Accel_mss"

    def lastVariable(self):
        """Return the last variable. Can be used in indexing lists."""
        return "Temperature_C"

    def getCpp(self, identifier):
        """Return c++ code related to this conf."""
        if identifier == "include":
            return ["#include <SMpu9250.h>"]
        elif identifier == "functions_all":
            return ["SMPU_FUNCTIONS_ALL"]
        return []
