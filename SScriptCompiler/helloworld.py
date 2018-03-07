"""Print in a loop."""
from src.SProgram import SProgram as program


def main():
    """Print 'Hello world!' and similar texts in loop."""
    # program
    p = program(
        #either
        [
            ("p", "&pointerText"),
        ],
        [
            ("text", "Hello world!"),
            ("pointerText", "Hello pointer!"),
            ("sep", " - "),
            ("text_concat"),
        ],
        # or (if there are only strings, no int variables)
        #stringNameValuePairs=[
            # if string (or variable) name begins with '_'
            # the name is set as is, no modifications are
            # tried (such as name search or the like)
            # (or you can use lists, though initialization
            # must be performed in 'init'-state in that case)
            #("_text", "Hello world!")
        #],
        fps=2,
        # program (state, [expressions])
        program=[
            ("main", [
                ["printString", "text", True],
                ["printString", "*p", True],

                ["clearString", "text_concat"],
                ["concatString_String", "text_concat", "text"],
                ["concatString_String", "text_concat", "sep"],
                ["concatString_String", "text_concat", "pointerText"],

                ["printString", "text_concat", True],

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
