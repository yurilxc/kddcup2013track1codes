import tempfile, operator
from Counter import Counter

class Feature:
    def __init__(self, size):
        self.__size = int(size)
        self.__isFixed = False
        self.__lineFp = tempfile.TemporaryFile(dir='./tmp')

    def addLine(self, line):
        """line: [[0, 1], [7, 2.3]]"""
        assert not self.__isFixed
        for f in line:
            assert 0 <= f[0] < self.size
        self.__lineFp.write(repr(line) + '\n')

    def fix(self):
        self.__isFixed = True
        self.__lineFp.seek(0)

    def getItrerable(self):
        self.fix()
        while True:
            line = self.__lineFp.readline()
            if line == '':
                break
            yield eval(line)

    def toFile(self, fp):
        """return:
        sparse\t8
        0:1 1:3 7:8
        1:2 3:2.3 7:3.0
        ..."""
        fp.write("sparse\t{:d}\n".format(self.size))
        for line in self.getItrerable():
            line = map(lambda x: str(x[0]) + ':' + str(x[1]), line)
            fp.write(' '.join(line) + '\n')

    @property
    def size(self):
        return self.__size
    @property
    def lines(self):
        return self.__lines

    @staticmethod
    def fromFile(fp):
        """input:
        sparse\t8
        0:1 1:3 7:8
        1:2 3:2.3 7:3.0
        ..."""
        size = int(fp.readline().split('\n')[0].strip()[len('sparse'):])
        feature = Feature(size)
        for i, line in enumerate(fp):
            line = line.split()
            line = map(lambda x: x.split(':'), line)
            line = map(lambda x: [int(x[0]), float(x[1])], line)
            feature.addLine(line)
        feature.fix()
        return feature
        
    @staticmethod
    def mergeFeatures(fp, *features):
        offsets = [0]
        for size in map(lambda x: x.size, features):
            offsets.append(offsets[-1] + size)
        size = offsets.pop()
        fp.write("sparse\t{:d}\n".format(size))
        iterables = map(lambda x: x.getItrerable(), features)
        counter = Counter("mergeFeatures", 100)
        while True:
            counter.inc()
            try:
                lines = map(lambda x: x.next(), iterables)
                for offset, line in zip(offsets, lines):
                    for f in line:
                        f[0] += offset
                line = reduce(operator.add, lines)
                line = map(lambda x: str(x[0]) + ':' + str(x[1]), line)
                fp.write(' '.join(line) + '\n')
            except StopIteration:
                break
