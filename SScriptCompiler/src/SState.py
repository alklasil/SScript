"""State module for SScript."""


class SState:
    """State class for SScript."""

    def __init__(self, name, expressions):
        """Set name and expressions."""
        self.name = name
        self.expressions = expressions

    def getExpressions(self):
        """Get expressions."""
        return self.expressions

    def getLen(self):
        """Count expressions."""
        return len(self.expressions)
