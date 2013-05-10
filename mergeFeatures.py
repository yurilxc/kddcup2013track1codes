#! /usr/bin/python2

import sys
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
    sys.stderr.write('mergeFeatures\n')
    args = parseArgs()
    features = map(Feature.fromFile, args.featurefiles)
    mergedFeature = Feature.mergeFeatures(sys.stdout, *features)








