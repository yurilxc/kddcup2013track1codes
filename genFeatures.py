#! /usr/bin/python2

import argparse
import csv

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./genFeatures.py --datadir dir -i train.csv -o train
    output: train.x train.y
    example: ./genFeatures.py --datadir dir -i test.csv -o test
    output: test.x test.y''',
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--datadir',
                        dest='datadir', 
                        type=str, 
                        help='directory contains Author.csv, PaperAuthor.csv, etc.',
                        required=True)
    parser.add_argument('-i',
                        metavar='INPUTFILE', 
                        dest='ifile', 
                        type=argparse.FileType('r'),
                        help='train.csv/valid.csv', 
                        required=True)
    parser.add_argument('-o',
                        dest='outputPrefix', 
                        type=str, 
                        help='train/valid', 
                        required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    ifile = args.ifile
    ofilex = open(args.outputPrefix + '.x', 'w')
    ofiley = open(args.outputPrefix + '.y', 'w')
    def genListFromCsv(filename):
        return list(csv.reader(file(args.datadir + '/' + filename)))[1:]
    authorList = genListFromCsv('Author.csv')
    for line in authorList:
        line[0] = int(line[0])
    paperAuthorList = genListFromCsv('PaperAuthor.csv')
    for line in paperAuthorList:
        line[0], line[1] = int(line[0]), int(line[1])

    ifile.close()
    ofilex.close()
    ofiley.close()

