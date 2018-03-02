"""Variable class for SScript."""
from src.SList import SList as sl


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

            # a few 'registers' for general use

            SVariable("r1"), SVariable("r2"),
            SVariable("r3"), SVariable("r4"),
            SVariable("r5"), SVariable("r6"),
            SVariable("r7"), SVariable("r8"),

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

    @staticmethod
    def create(nameValuePairs, st, initialState="init", useSTDVariables=True):
        """NameValuePairs -> variables(name, value)."""
        v = []
        if useSTDVariables:
            v = SVariable.stdVariables(st, initialState)
        for nvp in nameValuePairs:
            if type(nvp) is tuple:
                # (name, value)
                v.append(SVariable(nvp[0], nvp[1]))
            elif type(nvp) is list:
                # [name, size]
                for i in range(0, nvp[1]):
                    _s = nvp[0] + "[" + str(i) + "]"
                    v.append(SVariable(_s))
            else:
                # name
                v.append(SVariable(nvp))
        return sl(v)
