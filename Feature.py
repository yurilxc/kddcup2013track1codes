class Feature:
    def __init__(self, size, lines):
        """line: [(0, 1), (7, 2.3)]"""
        self.__size = size
        self.__lines = lines

    def toString(self):
        """return:
        sparse\t8
        0:1 1:3 7:8
        1:2 3:2.3 7:3.0
        ..."""
        s = "sparse\t{:d}\n".format(self.size)
        for line in self.lines:
            line = map(lambda x: str(x[0]) + ':' + str(x[1]), line)
            s += ' '.join(line) + '\n'
        return s

    @property
    def size(self):
        return self.__size
    @property
    def lines(self):
        return self.__lines
