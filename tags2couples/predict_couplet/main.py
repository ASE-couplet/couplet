#! /usr/bin/env python
# -*- coding:utf-8 -*-

from .plan import Planner
from .predict import Seq2SeqPredictor
import sys
import argparse
import random
from .match import MatchUtil

import tensorflow as tf
tf.app.flags.DEFINE_boolean('cangtou', False, 'Generate Acrostic Poem')

reload(sys)
sys.setdefaultencoding('utf8')

def get_cangtou_keywords(input):
    assert(len(input) == 4)
    return [c for c in input]

def main(args,cangtou=False):
    planner = Planner()
    with Seq2SeqPredictor() as predictor:
        # Run loop
        terminate = False
        Judge = MatchUtil()
        while not terminate:
            try:
                input = args.Input.decode('utf-8').strip()
                if not input:
                    print('Input cannot be empty!')
                elif input.lower() in ['quit', 'exit']:
                    terminate = True
                else:
                    if cangtou:
                        keywords = get_cangtou_keywords(input)
                    else:
                        # Generate keywords
                        keywords = planner.plan(input)

                    # Generate poem
                    lines = predictor.predict(keywords)

                    # whether the couplet is in accordance with the rules
                    result = Judge.eval_rhyme(lines)

                    if result == True:
                        # Print keywords and poem
                        print('Keyword:\t\tPoem:')
                        for line_number in range(2):
                            punctuation = '，' if line_number % 2 == 0 else '。'
                            print('{keyword}\t\t{line}{punctuation}'.format(
                                keyword=keywords[line_number],
                                line=lines[line_number],
                                punctuation=punctuation
                            ))
                            terminate = True
                                              


            except EOFError:
                terminate = True
            except KeyboardInterrupt:
                terminate = True
    print('\nTerminated.')

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--Input', type=str, 
        help='input from users',
        default='')

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]),cangtou=tf.app.flags.FLAGS.cangtou)