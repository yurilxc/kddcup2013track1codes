#! /usr/bin/python2

import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='''\
    example: ./sklearnToRgfTrain.py -i train -o train

    output 2 files: train.x and train.y
    inputFormat: 1/0\tf0,f1,f2
    train.x's 1st line's outputFormat: sparse FEATURE_SIZE
    train.x's rest line's outputFormat: 0:f0 1:f1 2:f2
    train.y's outputFormat: +1/-1
    ''',
    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i',
                        dest='input',
                        type=argparse.FileType('r'),
                        help='sklearn feature file',
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
    ofiley = open(args.outputPrefix + '.y', 'w')
    featureSize = -1
    for line in ifile:
        label, features = line.strip().split('\t')
        if label == "0":
            label = "-1"
        else:
            label = "1"
        features = features.split(',')
        if featureSize == -1:
            featureSize = len(features)
            ofilex.write(str(featureSize) + '\n')
        for i, feature in enumerate(features):
            features[i] = str(i) + ':' + feature
        ofilex.write(' '.join(features) + '\n')
    ifile.close()
    ofilex.close()
    ofiley.close()

