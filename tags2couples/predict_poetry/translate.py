# -*- coding:utf-8 -*-
import os
import codecs
import json

from gensim import models
from utils import DATA_PROCESSED_DIR

_model_path = os.path.join(DATA_PROCESSED_DIR, 'kw_model.bin')
_morden_model_path = os.path.join(DATA_PROCESSED_DIR, 'zh.bin')

class Translater:

    def __init__(self):
        self.morden_model = models.Word2Vec.load(_morden_model_path)
        self.model = models.Word2Vec.load(_model_path)
        self.possible_words = []
        self.step = 0

    def translate(self, word, max_step=500):
        if word in self.model.wv:
            return word
        if word not in self.morden_model.wv:
            return "BAD TAG !"
        while self.step < max_step:
            similars = self.morden_model.wv.most_similar(positive = [word])
            if len(self.possible_words) < max_step:
                self.possible_words.extend(pair[0] for pair in similars)
            if self.possible_words[0] in self.model.wv:
                return self.possible_words[0]
            self.step = self.step + 1
            word = self.possible_words.pop(0)
            
if __name__ == '__main__':
    translater = Translater()
    print(translater.translate("街道"))