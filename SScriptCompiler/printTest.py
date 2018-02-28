"""Print 0 in a loop."""

from src.SFunction import SFunction as sf
from src.STDSFunctions import STDSFunctions as stdf
from src.SVariable import SVariable as sv
from src.SState import SState as ss
from src.SExpression import SExpression as se
from src.SList import SList as sl
from src.SCompiler import SCompiler as co


def main():
    """Print 0 in loop."""
    # states
    st = sl([sf("main")])
    # variables
    v = sl(sv.stdVariables(st) + [
        sv("i")
    ])
    # functions
    f = stdf(st, v)
    # program
    s = sl([
        # main state always first
        ss("main", [
            f.printInt("i"),
        ]),
    ])

    c = co(s, f, v)
    print(c.compile())


if __name__ == "__main__":
    # execute only if run as a script
    main()
