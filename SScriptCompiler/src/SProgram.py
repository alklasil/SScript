"""Program module for SScript."""
from src.SState import SState as ss
from src.SList import SList as sl
from src.STDSFunctions import STDSFunctions as stdf
from src.SCompiler import SCompiler as co
from src.conf.std import Std as Std


class SProgram:
    """Program class for SScript."""
    def __init__(self,
                 variableNameValuePairs=[],
                 stringNameValuePairs=[],
                 initialState="main",
                 confs=[Std()],
                 fps=60,
                 program=[]):
        """parse program states & state, expression pairs (program)."""
        # stateExpressionsTuples =
        #   [(state, state.expressions) for state in states]

        print("INITIALIZING PROGRAM...")
        print("")

        """Set the program."""
        if len(program) == 1:
            self._stets = program
        else:
            self._stets = [("_main", [
                ["expr", ["$executeState", "state"]]
            ])] + program

        nameValuePairs = [
            variableNameValuePairs,
            stringNameValuePairs
        ]

        if fps is not None:
            # create variable for timeout with the fps provided
            nameValuePairs[0] = [
                "_lastTimedOut",
                ("_timeoutLength", int((1/fps)*1000)),
            ] + nameValuePairs[0]
            # add readTimer & timeout into main
            # (hox! if fps is None and user wants to use timer,
            #  readTimer is required to be added manually,
            #  if fps is not None, as is case here, do not add readTimer)
            self._stets[0] = (
                # state-name
                self._stets[0][0],
                # expressions
                [
                    # readTimer does not store millis in,
                    # use getTime to do that
                    # first readTimer
                    ["expr", ["$readTimer"]],
                    # then check if timeout
                    #  if timeout: abort stateExecution
                    ["expr", ["$timeout", "_lastTimedOut", "_timeoutLength"]]
                ] + self._stets[0][1]
            )

        # parse states list
        self.st = []
        for stet in self._stets:
            self.st.append(stet[0])

        self.f = stdf(
            stateNames=self.st,
            nameValuePairs=nameValuePairs,
            initialState=initialState,
            confs=confs)
        # execute expression functions
        #   (easier job for the compiler)
        self.stets = []
        print("states:")
        for stet in self._stets:
            print(stet)
            print("")
            expressions = []
            for expression in stet[1]:
                if len(expression) == 1:
                    function = getattr(self.f, expression[0])
                    _expression = function()
                else:
                    function = getattr(self.f, expression[0])
                    args = expression[1:]
                    _expression = function(*args)
                expressions.append(_expression)
            self.stets.append((stet[0], expressions))
        # software, the code of the program
        self.s = sl([
            # ss(name, [expressions])
            ss(stet[0], stet[1])
            for stet in self.stets
        ])
        self.c = co(self)
        self.compiled = None

        print("variables:")
        print(nameValuePairs)
        print("")
        print("PROGRAM INITIALIZED")

    def getSoftware(self):
        """Return the program."""
        return self.s

    def getStates(self):
        """Return programs possible states."""
        return self.st

    def getFunctions(self):
        """Return all (std) functions."""
        return self.f

    def gf(self):
        """Short verion for getFunctions."""
        return self.getFunctions()

    def compile(self, printIt=True):
        """Compile the program using SCompiler."""
        self.compiled = self.c.compile()
        return self.getCopiled(printIt)

    def getCopiled(self, printIt=True):
        """Get the compiled program."""
        if printIt:
            print(self.compiled)
        return self.compiled
