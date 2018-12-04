from utils import *
import pypinyin

class MatchUtil:

    def get_possible_tones(self, ch):
        """
        Args:
            ch: A unicode character

        Returns:
            [int]: A list of possible tones

        """
        final_tones = pypinyin.pinyin(ch, style=pypinyin.FINALS_TONE3, \
             heteronym=True, errors='default')[0] # select results for first and only char
        tones = [final_tone[-1] for final_tone in final_tones]
        # tones = [x.encode('raw_unicode_escape') for x in tones]
        filtered_tones = list(filter(str.isdigit, tones))
        tones_int = list(map(int, filtered_tones))

        # deduplication
        deduped_tones = []
        for tone in tones_int:
            if tone not in deduped_tones:
                deduped_tones.append(tone)

        return deduped_tones

    def get_possible_tone_types(self, ch):
        """

        Args:
            ch: A unicode character

        Returns:
            str: 'p' or 'z' or '*' representing possible tone types
        """
        tones = self.get_possible_tones(ch)
        pin_tones = {1, 2} & set(tones)
        ze_tones = {3, 4} & set(tones)

        if pin_tones and ze_tones:
            return '*'
        elif pin_tones:
            return 'p'
        elif ze_tones:
            return 'z'
        else:
            raise Exception('No tones associated with the character')

    def eval_rhyme(self, sentences):

        if len(sentences) != 4:
            return False
               

        return True