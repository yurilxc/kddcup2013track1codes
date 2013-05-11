#! /usr/bin/python2

import sys, re
import csv
import argparse
from Counter import Counter

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: cat file1 file2 | ./genWordCount.py > wordCount.csv''', 
    formatter_class=argparse.RawTextHelpFormatter)
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    csvWriter = csv.writer(sys.stdout)
    wordCountDict = {}
    spliter = re.compile("[^a-z]")
    counter = Counter("genWordCount", 100000)
    csvWriter.writerow(["id", "name" , "count"])
    for line in sys.stdin:
        counter.inc()
        words = spliter.split(line.lower())
        for word in words:
            wordCountDict.setdefault(word, 0)
            wordCountDict[word] += 1
    for wordId, wordCount in enumerate(sorted(wordCountDict.items(), cmp=lambda x, y: cmp(x[1], y[1]))):
        csvWriter.writerow([wordId] + list(wordCount))
