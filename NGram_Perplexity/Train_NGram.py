#!/usr/bin/env python3
# coding: utf-8

from random import random
import pprint
import operator
import pickle
import argparse
from collections import *

from utils.Ngram import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create N-Gram Model or Test exists model.')
    parser.add_argument("train_data_file" , help = "train data file path" , default="")
    parser.add_argument("model_type" , help = "character n gram or syllable n gram model character/syllable" )
    parser.add_argument("model_file" , help = "model file name" , )
    parser.add_argument("n" , help = "n for N-gram number" , type = int )


    args = parser.parse_args()


    model_type = args.model_type

    train_data_file = args.train_data_file
    n = args.n

    model_file = args.model_file



    for i in range(1 , n + 1):
        model = NGram(train_data_file , model_type)
        print("{}-Gram model creating!!".format(i))
        model.create_NGram(i)
        model.save_model(model_file + str(i))
        print("{}-Gram model created!!".format(i))
