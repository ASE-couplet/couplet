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
        return lines[0]+'('+keywords[0]+')' +'  '+lines[1]+'('+keywords[1]+')'+'  '+lines[2]+'('+keywords[2]+')'+'  '+lines[3]+'('+keywords[3]+')'
        
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--Input', type=str, 
        help='input from users',
        default='')

    return parser.parse_args(argv)

if __name__ == '__main__':
    input_ustr = parse_arguments(sys.argv[1:]).Input
    maker = Main_Poetry_maker()
    print(maker.predict(input_ustr))