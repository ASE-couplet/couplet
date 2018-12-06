# -*- coding:utf-8 -*-

import codecs
import json
from web_test import Main_Poetry_maker
from rank_words import rank_path

target_words_couplet = []
maker = Main_Poetry_maker()

with codecs.open(rank_path, 'r', 'utf-8') as fin:
    ranks = json.load(fin)

out_file = open('out_words.txt', 'w', encoding='utf-8')

for i in range(0, 100):
    word = ranks[i][0]
    target_words_couplet.append(word)
    result_couplet = maker.predict(word)
    out_file.write(word + '   ' + result_couplet + '\n')
    print(word + '   ' + result_couplet + '\n')

out_file.close()