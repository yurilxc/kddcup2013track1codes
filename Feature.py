class Feature:
    def __init__(self, size, lines):
        """line: [(0, 1), (7, 2.3)]"""
        self.__size = size
        self.__lines = lines
        
    @property
    def size(self):
        return self.__size
    @property
    def lines(self):
        return self.__lines
