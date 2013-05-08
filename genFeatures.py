#! /usr/bin/python2

import argparse, ConfigParser
import csv

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./genFeatures.py feature.conf data/ train.csv train
    output: train.x train.y
    example: ./genFeatures.py feature.conf data/ test.csv test
    output: test.x test.y''', 
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(dest='config', 
                        type=argparse.FileType('r'),
                        help='configs: maxAuthorId, maxPaperId, etc.')
    parser.add_argument(dest='datadir', 
                        type=str, 
                        help='directory contains Author.csv, PaperAuthor.csv, etc.')
    parser.add_argument(metavar='INPUTFILE', 
                        dest='ifile', 
                        type=argparse.FileType('r'),
                        help='train.csv/valid.csv')
    parser.add_argument(dest='outputPrefix', 
                        type=str, 
                        help='train/valid')
    return parser.parse_args()

class Feature:
    def __init__(self, size, lines):
        self.__size = size
        self.__lines = lines

    @property
    def size(self):
        return self.__size
    @property
    def lines(self):
        return self.__lines

def genCoauthorFeature(instances, paperAuthorList, maxAuthorId):
    '''
    return (sparse, [features])
    '''
    d = {}
    for line in paperAuthorList:
        d.setdefault(line[0], [])
        d[line[0]].append(line[1])
    features = []
    for line in instances:
        authorId, paperId = line[1], line[2]
        features.append(d[paperId])
    return Feature(maxAuthorId, features)

if __name__ == "__main__":
    args = parseArgs()
    config = ConfigParser.ConfigParser()
    config.readfp(args.config)
    ifile = args.ifile
    ofilex = open(args.outputPrefix + '.x', 'w')
    ofiley = open(args.outputPrefix + '.y', 'w')
    instances = []
    for line in list(csv.reader(ifile))[1:]:
        authorId = int(line[0])
        if len(line) == 3:      # train file
            for paperId in map(int, line[1].split()):
                instances.append(("+1", authorId, paperId))
            for paperId in map(int, line[2].split()):
                instances.append(("-1", authorId, paperId))
        else:                   # pred file
            for paperId in map(int, line[1].split()):
                instances.append(("0", authorId, paperId))

    def genListFromCsv(filename):
        return list(csv.reader(file(args.datadir + '/' + filename)))[1:]
    authorList = genListFromCsv('Author.csv')
    for line in authorList:
        line[0] = int(line[0])
    paperAuthorList = genListFromCsv('PaperAuthor.csv')
    for line in paperAuthorList:
        line[0], line[1] = int(line[0]), int(line[1])
    
    features = []
    features.append(genCoauthorFeature(instances,
                                       paperAuthorList,
                                       int(config.get('global', 'maxAuthorId'))))

    ifile.close()
    ofilex.close()
    ofiley.close()

