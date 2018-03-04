"""Print in a loop using pointers."""
from src.SProgram import SProgram as program


def main():
    """Print in a loop using pointers."""
    # program
    p = program(
        # ("i", "&a") == ("i", "a"), poth set i as pointer to point to a
        # in code, the form &a is required, see below
        [("i", "&a"), ("a", 333), ("b", 555), ("th", 1000)],
        # program (state, [expressions])
        program=[
            ("main", [
                # use i to as 'pointer' for a
                # *i -> variables[i.value].value == variables["a"].value

                # set i to point to b
                ["set", "i", "&b"],
                # print b
                ["printInt", "*i", True],
                # point i to point to a
                ["set", "i", "&a"],
                # print a
                ["printInt", "*i", True],
                # if else example
                ["IF",
                    # if (*i < 1000, i.e., a < 1000)
                    ["eval", "*i", "<", th],
                    #["eval", "*i", "<", 1000], # or this, both can be used
                        # then a++
                        ["inc", "*i"],
                        # else a = 0
                        ["set", "*i", "0"],
                ],
                #["set", "a", 0]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
