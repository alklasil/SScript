"""Program module for SScript."""
from src.SState import SState as ss
from src.SList import SList as sl
from src.STDSFunctions import STDSFunctions as stdf
from src.SCompiler import SCompiler as co


class SProgram:
    """Program class for SScript."""
    def __init__(self,
                 variableNameValuePairs=None,
                 initialState="main",
                 useSTDVariables=True,
                 useSTDFunctions=True,
                 program=[]):
        """parse program states & state, expression pairs (program)."""
        # stateExpressionsTuples =
        #   [(state, state.expressions) for state in states]

        """Set the program."""
        if len(program) == 1:
            self._stets = program
        else:
            self._stets = [("_main", [
                ["executeState"]
            ])] + program

        # parse states list
        self.st = []
        for stet in self._stets:
            self.st.append(stet[0])

        self.f = stdf(
            stateNames=self.st,
            variableNameValuePairs=variableNameValuePairs,
            initialState=initialState,
            useSTDVariables=useSTDVariables,
            useSTDFunctions=useSTDFunctions)
        # execute expression functions
        #   (easier job for the compiler)
        self.stets = []
        for stet in self._stets:
            expressions = []
            for expression in stet[1]:
                if len(expression) == 1:
                    function = getattr(self.f, expression[0])
                    expression = function()
                else:
                    function = getattr(self.f, expression[0])
                    args = expression[1:]
                    expression = function(*args)
                expressions.append(expression)
            self.stets.append((stet[0], expressions))

        # software, the code of the program
        self.s = sl([
            # ss(name, [expressions])
            ss(stet[0], stet[1])
            for stet in self.stets
        ])
        self.c = co(self)
        self.compiled = None

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
