"""List module for SScript."""


class SList:
    """List class for SScript."""

    def __init__(self, value):
        """Set value (anything[])."""
        self.value = value

    def get(self, name):
        """Get index ('address') by name."""
        for i, val in enumerate(self.value):
            if val.name == name:
                if val.name[0] == "*":
                    if hasattr(val, "value"):
                        # it's variable pointer,
                        # functions do not have value
                        # pointers are negative indexes (-1 points to 1)
                        return "-" + self.get(val.value)
                return str(i)
        print ("Error: " + name + " Not found in " + str(val))
        raise NameError

    def getValue(self):
        """Get value."""
        return self.value

    def getLen(self):
        """Get length of value[]."""
        return len(self.value)
