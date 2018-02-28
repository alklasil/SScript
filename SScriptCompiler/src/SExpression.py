"""Expression module for SScript."""


class SExpression:
    """Expression class for SScript."""
    def __init__(self, value):
        """Set value str[]."""
        self.value = value

    def get(self):
        """Get Value (str)."""
        return ' '.join(self.value)

    def getLen(self):
        """Get length (number of elements)."""
        return len(self.value)
