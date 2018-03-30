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
        self.confs = confs
        self.states = states

        """Set the program."""
        # if there are more than 1 state, executeState is added automatically
        if len(states) > 1:
            self.states = [("_main", [
                ["expr", ["$executeState", "state"]]
            ])] + self.states

        # create variable for timeout if fps provided
        if fps is not None:
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
                    ["expr", ["$readTimer"]],
                    # then check if timeout
                    #  if timeout: abort stateExecution
                    ["expr", ["$timeout", "_lastTimedOut", "_timeoutLength"]]
                ] + self.states[0][1]
            )

        # parse state names from states list
        self.stateNames = []
        for state in self.states:
            # state[0] = state name
            self.stateNames.append(state[0])
        self.sStateNames = SList([
            SFunction(_stateName)
            for _stateName in self.stateNames
        ])

        self.sVariables = SVariable.create(
            variableNameValuePairs=variableNameValuePairs,
            stateNames=self.sStateNames,
            confs=confs,
            initialState=initialState)

        # strings
        self.sStrings = SList([
            SVariable(stringNameValuePair[0], stringNameValuePair[1])
            for stringNameValuePair in stringNameValuePairs
        ])

        # Get functions from chosen configurations
        self.functions = []
        for conf in confs:
            self.functions += conf.getFunctions()
        self.sFunctions = SList(self.functions)

        # sConf
        self.sConfs = self.confs

        # (name) strings -> integers (index / constant)
        self._states = []
        print("reformat states:")
        for _state in self.states:
            print(_state)
            print("")
            expressions = []
            for expression in _state[1]:
                if len(expression) == 1:
                    function = getattr(self, expression[0])
                    _expression = function()
                else:
                    function = getattr(self, expression[0])
                    args = expression[1:]
                    _expression = function(*args)
                expressions.append(_expression)
            self._states.append((_state[0], expressions))
        # States -> SStates
        self.sStates = SList([
            # ss(name, [expressions])
            SState(_state[0], _state[1])
            for _state in self._states
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

    def expr(self, l):
        """Enable simpler expression creation.

        Args:
            l = str[] (list of strings [states, variables, functions]
            (l = ["fun", "var", "var", "var", "fun", 1, "fun"])
        """

        expression = []
        for element in l:
            # print(element)
            if type(element) is str and element[0] == '$':
                # function
                expression.append(self.sFunctions.get(element[1:]))
            elif type(element) is str and element[0] == '@':
                # state
                expression.append(self.sStateNames.get(element[1:]))
            elif type(element) is str and element[0] == '#':
                # string
                expression.append(self.sStrings.get(element[1:]))
            else:
                # variable
                expression.append(self.sVariables.get(element))
        # convert expression into SExpression and return it
        return SExpression(expression)
