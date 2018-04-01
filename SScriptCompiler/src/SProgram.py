"""Program module for SScript."""
from src.SState import SState
from src.SList import SList
from src.SCompiler import SCompiler
from src.conf.SStd import SStd
from src.SVariable import SVariable
from src.SFunction import SFunction
from src.SExpression import SExpression


class SProgram:
    """Program class for SScript."""
    def __init__(self,
                 variableNameValuePairs=[],
                 stringNameValuePairs=[],
                 initialState="main",
                 confs=[SStd()],
                 fps=60,
                 states=[]):
        """parse program states & state, expression pairs (program)."""
        # stateExpressionsTuples =
        #   [(state, state.expressions) for state in states]

        print("INITIALIZING PROGRAM...")

        print("")
        self.sConfs = confs
        self.states = self.flattenList(states)

        """Set the program."""

        # if there are more than 1 state, executeState is added automatically
        if len(self.states) > 1:
            self.addMain()

        # create variable for timeout if fps provided
        if fps is not None:
            variableNameValuePairs = self.addFps(variableNameValuePairs, fps)

        # get states first. Set expressions to None, we only need the names
        # at this stage
        self.sStates = SList([
            SState(state[0], None)
            for state in self.states
        ])

        # variables
        self.sVariables = SVariable.create(
            variableNameValuePairs=self.flattenList(variableNameValuePairs),
            states=self.sStates,
            confs=self.sConfs,
            initialState=initialState)

        # strings
        self.sStrings = SList([
            SVariable(stringNameValuePair[0], stringNameValuePair[1])
            for stringNameValuePair in self.flattenList(stringNameValuePairs)
        ])

        # Get functions from chosen configurations
        self.functions = []
        for conf in self.sConfs:
            self.functions += conf.getFunctions()
        self.sFunctions = SList(self.functions)

        # SStates (already exists, but expressions are set to None
        self.sStates = SList([
            # name, expressions
            SState(state[0], [
                self.expr(expression)
                for expression in state[1]
            ])
            for state in self.states
        ])

        self.c = SCompiler(self)
        self.compiled = None

        print("variables:")
        print(variableNameValuePairs)
        print("")
        print("PROGRAM INITIALIZED")

    def compile(self, printIt=True):
        """Compile the program using SCompiler."""
        self.compiled = self.c.compile()
        return self.getCopiled(printIt)

    def getCopiled(self, printIt=True):
        """Get the compiled program."""
        if printIt:
            print(self.compiled)
        return self.compiled

    def flattenList(self, l):
        l_flattened = []
        for item in l:
            if type(item) is list:
                l_flattened.extend(self.flattenList(item))
            else:
                l_flattened.append(item)
        return l_flattened

    def expr(self, l):
        """Enable simpler expression creation.

        Args:
            l = str[] (list of strings [states, variables, functions]
            (l = ["fun", "var", "var", "var", "fun", 1, "fun"])
        """

        expression = []
        for element in self.flattenList(l):
            # print(element)
            if type(element) is str and element[0] == '$':
                # function
                expression.append(self.sFunctions.get(element[1:]))
            elif type(element) is str and element[0] == '@':
                # state
                expression.append(self.sStates.get(element[1:]))
            elif type(element) is str and element[0] == '#':
                # string
                expression.append(self.sStrings.get(element[1:]))
            else:
                # variable
                expression.append(self.sVariables.get(element))
        # convert expression into SExpression and return it
        return SExpression(expression)

    def addMain(self):
        """Add main state."""
        self.states = [("_main", [
            ["$executeState", "state"]
        ])] + self.states

    def addFps(self, variableNameValuePairs, fps):
        print(variableNameValuePairs)
        variableNameValuePairs = [
            "_lastTimedOut",
            ("_timeoutLength", int((1/fps)*1000)),
        ] + variableNameValuePairs
        # add readTimer & timeout into main
        # (hox! if fps is None and user wants to use timer,
        #  readTimer is required to be added manually,
        #  if fps is not None, as is case here, do not add readTimer)
        self.states[0] = (
            # state-name
            self.states[0][0],
            # expressions
            [
                # readTimer does not store millis in,
                # use getTime to do that
                # first readTimer
                ["$readTimer"],
                # then check if timeout
                #  if timeout: abort stateExecution
                ["$timeout", "_lastTimedOut", "_timeoutLength"]
            ] + self.states[0][1]
        )
        return variableNameValuePairs
