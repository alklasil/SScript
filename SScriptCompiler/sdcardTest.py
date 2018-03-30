"""Count steps.

SDCARD test

"""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd
from src.conf.SSdcard import SSdcard


def main(argv=[], confs=[SStd(), SSdcard()]):
    """Write & read data from sdcard."""
    # program

    p = program(
        # variables (count & thresholds)
        [],
        [
            ("filename", "sdcart.test"),
            ("store", "TEST String"),
            "load"
        ],
        confs=confs,
        fps=2,
        states=[
            ("main", [

                # open

                # store

                # close

                # reopen

                # read

                # close

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
