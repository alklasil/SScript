"""State module for SScript."""
from src.SList import SList as sl
from src.SFunction import SFunction as sf


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

    @staticmethod
    def create(names):
        """List of names -> States."""
        return sl([
            sf(name) for name in names
        ])
