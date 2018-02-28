"""Count how many times a door has been opened based on temperature.

Increase count when temperature drops below down threshold.

Example output:
    21 4 3 1 4 1 19 15 20 10 5 1 3 2 4 10 1 7 4 2 9 2 4 2 8 4 3 1 3 13 3 17 3
    23 5 0 17 4 20 5 9 4 0 11 2 9 3 4 2 8 3 3 18 3 0 3 2 18 24 7 4 2 9 4 4 2 8
    4 3 1 3 13 3 17 3 23 5 0 17 4 19 5 9 4 0 11 2 9 2 4 2 8
"""

from src.SFunction import SFunction as sf
from src.STDSFunctions import STDSFunctions as stdf
from src.SVariable import SVariable as sv
from src.SState import SState as ss
from src.SExpression import SExpression as se
from src.SList import SList as sl
from src.SCompiler import SCompiler as co


def main():
    """Count how many times a door has been opened based on temperature."""
    # states
    st = sl([
        sf("main"), sf("init"), sf(">t"), sf("<t>"), sf("<t"),
    ])
    # variables
    v = sl(sv.stdVariables(st, intialState="init") + [
        sv("count"),                      # = door opened "count" times
        # threshold up (assume roomTemperature > 15)
        sv("tUP", 15),
        # threshold down (assume outsideTemperature < 10)
        sv("tDOWN", 10),
    ])
    # functions
    f = stdf(st, v)
    # program
    s = sl([
        # main state always first
        ss("main", [
            # goto execute the sate set by variable "state"
            f.executeState(),
        ]),
        ss("init", [
            # calibrate (thresholds), set tUP and tDOWN
            # & only then set state = "process"
            # (TODO)

            # set state = '>t' (above threshold)
            f.setState(">t")

        ]),
        ss(">t", [
            # read mpu sensor
            f.readMPU(),

            # get temperature
            f.getMpuValue("Temperature_C"),

            # [?] = temperature < tDOWN
            f.setConditional("Temperature_C", "<", "tDOWN"),

            # if [?] state = "<t>" for processing
            f.conditionalSetState("<t>"),

        ]),
        ss("<t>", [
            # state = "opening the door", do not execute when closing the door
            # increase count by one
            f.inc("count"),
            # "debug" print the increased value
            f.printInt("count"),
            # set state
            f.setState("<t")
        ]),
        ss("<t", [
            # read mpu sensor
            f.readMPU(),

            # get temperature
            f.getMpuValue("Temperature_C"),

            # [?] = temperature > tDOWN
            f.setConditional("Temperature_C", ">", "tUP"),

            # if [?] state = "<t"
            f.conditionalSetState(">t")
        ]),
    ])

    c = co(s, f, v)
    print (c.compile())


if __name__ == "__main__":
    # execute only if run as a script
    main()
