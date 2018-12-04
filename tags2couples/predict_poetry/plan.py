#! /usr/bin/env python
#-*- coding:utf-8 -*-

import os

import jieba
from gensim import models
from random import shuffle, random, randint

from utils import uprintln, uprint, DATA_PROCESSED_DIR, split_sentences
from data_utils import get_kw_train_data
from segment import Segmenter
from quatrains import get_quatrains
from rank_words import get_word_ranks
from functools import reduce


_model_path = os.path.join(DATA_PROCESSED_DIR, 'kw_model.bin')


class Planner:

    def __init__(self):
        self.ranks = get_word_ranks()
        if not os.path.exists(_model_path):
            self._train()
        else:
            self.model = models.Word2Vec.load(_model_path)

    def _train(self):
        print("Start training Word2Vec for planner ...")
        quatrains = get_quatrains()
        segmenter = Segmenter()
        seg_lists = []
        for idx, quatrain in enumerate(quatrains):
            seg_list = []
            for sentence in quatrain['sentences']:
                seg_list.extend([seg for seg in segmenter.segment(sentence) if seg in self.ranks])
            seg_lists.append(seg_list)
            if 0 == (idx+1)%10000:
                print("[Plan Word2Vec] %d/%d quatrains has been processed." %(idx+1, len(quatrains)))
        print("Hold on. This may take some time ...")
        self.model = models.Word2Vec(seg_lists, size = 512, min_count = 5)
        self.model.save(_model_path)

    def expand(self, words, num):
        positive = [w for w in words if w in self.model.wv]
        similars = self.model.wv.most_similar(positive = positive) \
                if len(positive) > 0 else []
        words.extend(pair[0] for pair in similars[:min(len(similars), num-len(words))])
        if len(words) < num:
            _prob_sum = sum(1./(i+1) for i in range(len(self.ranks)))
            _prob_sum -= sum(1./(self.ranks[word]+1) for word in words)
            while len(words) < num:
                prob_sum = _prob_sum
                for word, rank in list(self.ranks.items()):
                    if word in words:
                        continue
                    elif prob_sum * random() < 1./(rank+1):
                        words.append(word)
                        break
                    else:
                        prob_sum -= 1./(rank+1)
        shuffle(words)

    def plan(self, text):
        def extract(sentence):
            return [x for x in jieba.lcut(sentence) if x in self.ranks]
        keywords = sorted(reduce(lambda x,y:x+y, list(map(extract, split_sentences(text))), []),
            key = lambda x : self.ranks[x])
        words = [keywords[idx] for idx in \
                [i for i in range(len(keywords)) if 0 == i or keywords[i] != keywords[i-1]]]
        if len(words) < 4:
            self.expand(words, 4)
        else:
            while len(words) > 4:
                words.pop()
        return words

if __name__ == '__main__':
    planner = Planner()
    kw_train_data = get_kw_train_data()
    for row in kw_train_data:
        num = randint(1,3)
        uprint(row[1:])
        print("num = %d" %num)
        guess = row[1:num+1]
        planner.expand(guess, 4)
        uprintln(guess)
        assert len(guess) == 4
        print()

