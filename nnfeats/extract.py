import matio
import cv2
import numpy as np
import sys
import os
import shutil
import dlib
import json
import subprocess
import pipes
import argparse
from NeuralNet import NeuralNet

def getRep(imgPath, outPath, net, imgDim=224):
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        return None
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    rep = net.forward(rgbImg)
    return rep

def processDirList(outPath, parent, dirs, layer, gpuNum):
    net = NeuralNet('vgg19', 224, True, gpuNum)

    for directory in dirs:
        onlyFiles = [f for f in os.listdir(os.path.join(parent, directory)) if os.path.isfile(os.path.join(parent, directory, f))]

        # Try to make the output directory
        try:
            os.makedirs(os.path.join(outPath, directory))
        except:
            pass

        for fileName in onlyFiles:
            _, ext = os.path.splitext(fileName)

            # Only process images
            if 'jpg' in ext.lower() or 'png' in ext.lower():
                inFullPath = os.path.join(parent, directory, fileName)
                outFile = fileName + '_l' + layer + '_vgg.bin'
                outFullPath = os.path.join(outPath, directory, outFile)

                # Does the file already exist? if so lets skip.
                if not os.path.isfile(outFullPath):
                    rep = getRep(inFullPath, outFullPath, net)
                    if rep is not None:
                        matio.save_mat(outFullPath, rep)
                    else:
                        pass
                else:
                    pass

def splitList(l):
    return l[:len(l)/2], l[len(l)/2:]

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--source', type=str, required=True, help='Path to data to extract')
    argparser.add_argument('-d', '--destination', type=str, required=True, help='Path to send features')
    argparser.add_argument('-l', '--layer', type=str, required=True, help='Layer of features to grab')
    args = argparser.parse_args()

    try:
        os.makedirs(args.destination)
    except:
        pass

    onlyDirs = [f for f in os.listdir(args.source) if not os.path.isfile(os.path.join(args.source, f))]

    processDirList(args.destination, args.source, onlyDirs, 17, None)


if __name__ == "__main__":
    main()