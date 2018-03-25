"""Count steps.

SDCARD test

"""
from src.SProgram import SProgram as program
from src.conf.std import Std as Std
from src.conf.sdcard import Sdcard as Sdcard


def main():
    """Write & read data from sdcard."""
    # program

    std = Std()
    sdcard = Sdcard()

    p = program(
        # variables (count & thresholds)
        [],
        [
            ("filename", "sdcart.test"),
            ("store_str", "TEST String"),
            "load_str"
        ],
        confs=[std, sdcard],
        fps=2,
        program=[
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
