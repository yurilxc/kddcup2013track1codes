#! /usr/bin/python2

import sys
import argparse, ConfigParser
import csv
from Feature import *

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./genFeatures.py feature.conf data/ < train.csv > train.x
    output: train.x train.y
    example: ./genFeatures.py feature.conf data/ < test.csv > test.x
    output: test.x test.y''', 
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(dest='config', 
                        type=argparse.FileType('r'),
                        help='configs: maxAuthorId, maxPaperId, etc.')
    parser.add_argument(dest='datadir', 
                        type=str, 
                        help='directory contains Author.csv, PaperAuthor.csv, etc.')
    return parser.parse_args()

def genCoauthorFeature(instances, paperAuthorList, maxAuthorId):
    '''
    return Feature(sparse, [features])
    '''
    sys.stderr.write("genCoauthorFeature\n")
    d = {}
    for line in paperAuthorList:
        d.setdefault(line[0], set())
        d[line[0]].add(line[1])
    feature = Feature(maxAuthorId)
    for line in instances:
        authorId, paperId = line[0], line[1]
        feature.addLine(map(lambda x: [int(x), 1.0], d[paperId]))
    feature.fix()
    return feature

def genConferenceIdFeature(instances, paperList, maxConferenceId):
    sys.stderr.write("genConferenceIdFeature\n")
    d = {}
    for line in paperList:
        paperId = int(line[0])
        conferenceId = int(line[3])
        d[paperId] = conferenceId
    feature = Feature(maxConferenceId)
    for instance in instances:
        authorId, paperId = instance[0], instance[1]
        conferenceId = d[paperId] + 1 # -1
        feature.addLine([[conferenceId, 1.0]])
    feature.fix()
    return feature

def genJournalIdFeature(instances, paperList, maxJournalId):
    sys.stderr.write("genJournalIdFeature\n")
    d = {}
    for line in paperList:
        paperId = int(line[0])
        journalId = int(line[4])
        d[paperId] = journalId
    feature = Feature(maxJournalId)
    for instance in instances:
        authorId, paperId = instance[0], instance[1]
        journalId = d[paperId] + 1 # -1
        feature.addLine([[journalId, 1.0]])
    feature.fix()
    return feature
        

if __name__ == "__main__":
    args = parseArgs()
    config = ConfigParser.ConfigParser()
    config.readfp(args.config)
    instances = []
    for line in list(csv.reader(sys.stdin))[1:]:
        authorId = int(line[0])
        if len(line) == 3:      # train file
            for paperId in map(int, line[1].split()):
                instances.append([authorId, int(paperId)])
            for paperId in map(int, line[2].split()):
                instances.append([authorId, int(paperId)])
        else:                   # pred file
            for paperId in map(int, line[1].split()):
                instances.append([authorId, int(paperId)])

    def genListFromCsv(filename):
        return list(csv.reader(file(args.datadir + '/' + filename)))[1:]
    authorList = genListFromCsv('Author.csv')
    for line in authorList:
        line[0] = int(line[0])
    paperAuthorList = genListFromCsv('PaperAuthor.csv')
    for line in paperAuthorList:
        line[0], line[1] = int(line[0]), int(line[1])
    paperList = genListFromCsv('Paper.csv')
    for line in paperList:
        line[0] = int(line[0])
        line[2] = int(line[2])
        line[3] = int(line[3])
        line[4] = int(line[4])
    features = []
    features.append(genCoauthorFeature(instances,
                                       paperAuthorList,
                                       int(config.get('global', 'maxAuthorId'))))
    features.append(genConferenceIdFeature(instances,
                                          paperList,
                                          int(config.get('global', 'maxConferenceId'))))
    features.append(genJournalIdFeature(instances,
                                       paperList,
                                       int(config.get('global', 'maxJournalId'))))

    mergedFeature = Feature.mergeFeatures(*features)
    mergedFeature.toFile(sys.stdout)
