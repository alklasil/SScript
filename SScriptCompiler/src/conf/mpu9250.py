"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv


class Mpu9250:
    """Standard functions class for SScript."""
    def __init__(self):
        """"""
        pass

    def getFunctions(self):
        """"Return a list of functions by mpu9250."""
        return [
            sf("mpu_readSensor"),
            sf("mpu_getAccelX_mss"),
            sf("mpu_getAccelY_mss"),
            sf("mpu_getAccelZ_mss"),
            sf("mpu_getGyroX_rads"),
            sf("mpu_getGyroY_rads"),
            sf("mpu_getGyroZ_rads"),
            sf("mpu_getMagX_uT"),
            sf("mpu_getMagY_uT"),
            sf("mpu_getMagZ_uT"),
            sf("mpu_getTemperature_C")
        ]

    def getVariables(self, sdict):
        """Return list of variables by mpu9250."""
        return [
            # basic variables
            # If you do not use stdVariables, the first variable is not allowed
            # to be a list
            # sensor variables
            # accelerometer
            sv("Accel_mss"),              # amplitude of [x,y,z]
            sv("AccelX_mss"),             # amplitude in x-direction
            sv("AccelZ_mss"),             # amplitude in z-direction
            sv("AccelY_mss"),             # amplitude in y-direction

            # gyroscope
            sv("Gyro_rads"),
            sv("GyroX_rads"),
            sv("GyroY_rads"),
            sv("GyroZ_rads"),

            # magnetometer
            sv("Mag_uT"),
            sv("MagY_uT"),
            sv("MagX_uT"),
            sv("MagZ_uT"),

            # temperature
            sv("Temperature_C"),
        ]
