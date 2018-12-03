import argparse
import sys
import random
from plan import Planner
from predict import Seq2SeqPredictor
from match import MatchUtil

import tensorflow as tf

def main(args,cangtou=False):
    planner = Planner()
    predictor = Seq2SeqPredictor()

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
                keywords = planner.plan(input)

                lines = predictor.predict(keywords)

                    # whether the couplet is in accordance with the rules
                result = Judge.eval_rhyme(lines)

                while(result == False):
                    lines = predictor.predict(keywords)
                    result = Judge.eval_rhyme(lines)
                        # Print keywords and poem
                print('Keyword:\t\tPoem:')
                for line_number in range(2):
                    punctuation = u'，' if line_number % 2 == 0 else u'。'
                    print(u'{keyword}\t\t{line}{punctuation}'.format(
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
    main(parse_arguments(sys.argv[1:]),cangtou=False)