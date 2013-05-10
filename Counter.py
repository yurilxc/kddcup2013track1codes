import sys

class Counter:
    def __init__(self, name, interval=10000):
        self.__count = 0
        self.__name = name
        self.__interval = interval
    def inc(self):
        self.__count += 1
        if self.__count % self.__interval == 0:
            sys.stderr.write("{}:\t{:d}\r".format(self.__name, self.__count))
    def __del__(self):
        sys.stderr.write("\n")
