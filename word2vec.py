import io
import re
import string
import tqdm
import random
import Helpers
from collections import defaultdict

import numpy as np

import tensorflow as tf
from tensorflow.keras import layers
import gensim.downloader as api

'''
This is an interface for the gensim implementation of word2vec using the glove-twitter-25 dataset
'''
class word2vec:
    def __init__(self):
        self.model = api.load("glove-twitter-25")  # download the model and return as object ready for us

    def getWordsInCategory(self, num, cutoff, categories):
        words = defaultdict(list)
        for i in range(num//len(categories)):
            for category in categories:
                words[category].append(self.getWordInCategory(0.8, category))
        return words

    def getWordInCategory(self, cutoff, category):
        similar_words = self.model.most_similar(category)
        filtered_similar_words = list(filter(lambda x: x[1] > cutoff, similar_words))
        thresholds = Helpers.get_thresholds([[word[1] for word in filtered_similar_words]])[0]
        random_generated = random.uniform(0, thresholds[-1])
        index = Helpers.threshold_index(random_generated, thresholds)
        return filtered_similar_words[index][0]
