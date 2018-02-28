"""Variable class for SScript."""


class SVariable:
    """class for SScript variables."""
    def __init__(self, name, value=0):
        """Set name and value"""
        self.name = name
        self.value = value  # initial value

    def getValue(self):
        """Return name"""
        return self.value

        # stdVariables
    @staticmethod
    def stdVariables(st, intialState="main"):
        """Return std variables."""
        return [
            # basic variables
            SVariable("?"),
            SVariable("tmp"),
            SVariable("0"), SVariable("1", 1),
            SVariable("state", st.get(intialState)),

            # sensor variables
            # accelerometer
            SVariable("AccelX_mss"),             # amplitude in x-direction
            SVariable("AccelZ_mss"),             # amplitude in z-direction
            SVariable("AccelY_mss"),             # amplitude in y-direction
            SVariable("Accel_mss"),              # amplitude of [x,y,z]

            # gyroscope
            SVariable("GyroX_rads"),
            SVariable("GyroY_rads"),
            SVariable("GyroZ_rads"),
            SVariable("Gyro_rads"),

            # magnetometer
            SVariable("MagY_uT"),
            SVariable("MagX_uT"),
            SVariable("MagZ_uT"),
            SVariable("Mag_uT"),

            # temperature
            SVariable("Temperature_C"),
        ]
