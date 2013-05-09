#! /usr/bin/python2

import sys, argparse, csv

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./genLabels.py < train.csv > train.y
    3 cols output +1/-1.''', 
    formatter_class=argparse.RawTextHelpFormatter)
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    for line in list(csv.reader(sys.stdin))[1:]:
        authorId = int(line[0])
        assert len(line) == 3
        for paperId in map(int, line[1].split()):
            print "+1"
        for paperId in map(int, line[2].split()):
            print "-1"
