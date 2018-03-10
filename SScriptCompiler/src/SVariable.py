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

            # timer
            SVariable("millis"),
        ]

    @staticmethod
    def create(nameValuePairs, st, confs, initialState="init"):
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
            (nvp[0] if type(nvp) is tuple else nvp, nvpi)
            for nvpi, nvp in enumerate(nameValuePairs[1])
        ]

        nameValuePairs[1] = [
            # strings are named as '_name'
            (("_" + nvp[0], nvp[1]) if type(nvp) is tuple else "_" + nvp)
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
            if nvpi == 0 and confs is not None:
                # get variables from the configurations used
                for conf in confs:
                    v += conf.getVariables({
                        "st": st,
                        "initialState": initialState
                    })

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
