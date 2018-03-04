"""List module for SScript."""


class SList:
    """List class for SScript."""

    def __init__(self, value):
        """Set value (anything[])."""
        self.value = value

    def append(self, val):
        """Append value into self.value."""
        self.value.append(val)

    def get(self, name):
        """Get index ('address') by name."""
        # check if it is a pointer
        isPointer = False
        if name[0] == "*":
            isPointer = True
        for i, val in enumerate(self.value):
            if isPointer and val.name == name[1:]:
                if hasattr(val, "value"):
                    # it's variable pointer,
                    # functions do not have value
                    # pointers are negative indexes (-1 points to 1)
                    return "-" + str(i)
            if val.name == name:
                return str(i)

        try:
            # test if it's a number, may or may not have already been converted
            # we want to test this last, because numbers can be variables
            i = int(name)
            return str(name)
        except ValueError:
            print ("raised NameError:" + name + " Not found in " + str(val))
            raise NameError

    def getValue(self):
        """Get value."""
        return self.value

    def getLen(self):
        """Get length of value[]."""
        return len(self.value)
