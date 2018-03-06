"""Variable class for SScript."""
from src.SList import SList as sl


class SVariable:
    """class for SScript variables."""
    def __init__(self, name, value=0):
        """Set name and value"""
        self.name = name
        self.value = value  # initial value

    def getName(self):
        """Get the name of the variable."""
        return self.name

    def getValue(self):
        """Return name"""
        return self.value

        # stdVariables
    @staticmethod
    def stdVariables(st, intialState="main"):
        """Return std variables."""
        return [
            # basic variables
            # If you do not use stdVariables, the first variable is not allowed
            # to be a list
            SVariable("tmp"),
            SVariable("?"),
            SVariable("0"), SVariable("1", 1),
            SVariable("state", st.get(intialState)),

            # a few 'registers' for general use

            SVariable("r1"), SVariable("r2"),
            SVariable("r3"), SVariable("r4"),
            SVariable("r5"), SVariable("r6"),
            SVariable("r7"), SVariable("r8"),

            # timer
            SVariable("millis"),

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
        """nameValuePairs -> [[variables(name, value)],[strings(name, value)]]."""
        vs = []

        # lists -> names
        _nvpss = []
        for nvpi, nvps in enumerate(nameValuePairs):
            _nvps = []
            for nvp in nvps:
                if type(nvp) is list:
                    for i in range(0, nvp[1]):
                        _s = nvp[0] + "[" + str(i) + "]"
                        _nvps.append(_s)
                else:
                    _nvps.append(nvp)
            _nvpss.append(_nvps)
        nameValuePairs = _nvpss

        # add strings (indexes) as variables
        # (this can be optimized by optional initializations, TODO)
        nameValuePairs[0] = nameValuePairs[0] + [
            # strings' variables are named as name, instead of _name
            (nvp[0][1:] if type(nvp) is tuple else nvp[1:], nvpi)
            for nvpi, nvp in enumerate(nameValuePairs[1])
        ]

        # get names (so that they can be referenced in initializations)
        namess = []
        for nvpi, nvps in enumerate(nameValuePairs):
            names = []
            for nvp in nvps:
                if type(nvp) is str:
                    names.append(nvp)
                else:
                    names.append(nvp[0])
            namess.append(names)

        for nvpi, nvps in enumerate(nameValuePairs):
            v = []
            if nvpi == 0 and useSTDVariables:
                v = SVariable.stdVariables(st, initialState)
                vn = [
                    var.getName()
                    for var in v
                ]
                namess[0] = vn + namess[0]

            for nvp in nvps:
                if type(nvp) is tuple:
                    # (name, value)
                    if type(nvp[1]) is str and nvp[0][0] != "_":
                        if nvp[1][0] == "&":
                            # extract variable name from index if using &
                            # in initializations, using & is not required,
                            # though it is recommended, as that is what is
                            # required in the code
                            nvp = (nvp[0], nvp[1][1:])
                        for si, names in enumerate(namess):
                            for i, name in enumerate(names):
                                if name == nvp[1]:
                                    # always set the value as index
                                    # as there is no need for getting
                                    # the values.
                                    # there are better ways of doing so
                                    v.append(SVariable(nvp[0], i))
                    else:
                        v.append(SVariable(nvp[0], nvp[1]))
                #elif type(nvp) is list:
                #    # [name, size]
                #    for i in range(0, nvp[1]):
                #        _s = nvp[0] + "[" + str(i) + "]"
                #        v.append(SVariable(_s))
                else:
                    # name
                    v.append(SVariable(nvp))
            vs.append(v)
        return sl(vs)
