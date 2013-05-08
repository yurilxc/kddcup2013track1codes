#! /usr/bin/python2

import argparse
from Feature import *

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./mergeFeatures.py featurefile0 featurefile1 ... > mergefeature''', 
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(dest='featurefiles',
                        nargs='+', 
                        type=argparse.FileType('r'), 
                        help='rgf feature files')
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    features = map(Feature.fromSting, map(lambda x: x.read(), args.featurefiles))
    mergedFeature = Feature.mergeFeatures(*features)
    print mergedFeature.toString()
