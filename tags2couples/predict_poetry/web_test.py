import argparse
import sys
import random
from plan import Planner
from predict import Seq2SeqPredictor
from match import MatchUtil

import tensorflow as tf

class Main_Poetry_maker:
    def __init__(self):
        self.planner = Planner()
        self.predictor = Seq2SeqPredictor()
        self.Judge = MatchUtil()

    def predict(self, input_ustr):
        input_ustr = input_ustr.strip()
        keywords = self.planner.plan(input_ustr)
        lines = self.predictor.predict(keywords)
        result = self.Judge.eval_rhyme(lines)
        while(result == False):
            lines = self.predictor.predict(keywords)
            result = self.Judge.eval_rhyme(lines)

        for line_number in range(4):
            punctuation = u'，' if line_number % 4 == 0 else u'。'
            print(u'{keyword}\t\t{line}{punctuation}'.format(
                    keyword=keywords[line_number],
                    line=lines[line_number],
                    punctuation=punctuation
            ))

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--Input', type=str, 
        help='input from users',
        default='')

    return parser.parse_args(argv)

if __name__ == '__main__':
    input_ustr = parse_arguments(sys.argv[1:]).Input
    maker = Main_Poetry_maker()
    maker.predict(input_ustr)