class EMPTY_TYPE:
    def __eq__(self, other):
        return isinstance(other, EMPTY_TYPE)


EMPTY = EMPTY_TYPE()
