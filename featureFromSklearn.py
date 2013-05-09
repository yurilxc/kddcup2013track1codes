#! /usr/bin/python2

import sys
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./featureFromSklearn.py < train > train.x
    train.x's 1st line's outputFormat: sparse FEATURE_SIZE
    train.x's rest line's outputFormat: 0:f0 1:f1 2:f2
    train.y's outputFormat: +1/-1
    ''',
    formatter_class=argparse.RawTextHelpFormatter)
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    featureSize = -1
    for line in sys.stdin:
        label, features = line.strip().split('\t')
        if label == "0":
            label = "-1"
        else:
            label = "+1"
        features = features.split(',')
        if featureSize == -1:
            featureSize = len(features)
            print 'sparse\t' + str(featureSize)
        for i, feature in enumerate(features):
            features[i] = str(i) + ':' + feature
        print ' '.join(features)
