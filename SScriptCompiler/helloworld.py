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
                ["expr", ["$printString_ln", "text"]],
                ["expr", ["$printString_ln", "*p"]],

                ["expr", ["$clearString", "text_concat"]],
                ["expr", ["$concatString_String", "text_concat", "text"]],
                ["expr", ["$concatString_String", "text_concat", "sep"]],
                ["expr", ["$concatString_String", "text_concat", "pointerText"]],

                ["expr", ["$printString_ln", "text_concat"]]

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
