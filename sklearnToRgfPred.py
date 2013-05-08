#! /usr/bin/python2

import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./sklearnToRgfPred.py -i pred(valid) -o pred

    output pred.x
    inputFormat: 0\tf0,f1,f2
    pred.x's 1st line's outputFormat: sparse FEATURE_SIZE
    pred.x's rest line's outputFormat: 0:f0 1:f1 2:f2
    ''',
    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i',
                        dest='input',
                        type=argparse.FileType('r'),
                        help='sklearn valid feature file',
                        required=True)
         
    parser.add_argument('-o',
                        dest='outputPrefix',
                        type=str,
                        help='output file prefix',
                        required=True)
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    ifile = args.input
    ofilex = open(args.outputPrefix + '.x', 'w')
    featureSize = -1
    for line in ifile:
        label, features = line.strip().split('\t')
        features = features.split(',')
        if featureSize == -1:
            featureSize = len(features)
            ofilex.write('sparse\t' + str(featureSize) + '\n')
        for i, feature in enumerate(features):
            features[i] = str(i) + ':' + feature
        ofilex.write(' '.join(features) + '\n')
    ifile.close()
    ofilex.close()

