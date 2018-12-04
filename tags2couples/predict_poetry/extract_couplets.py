from .utils import DATA_PROCESSED_DIR, embed_w2v, apply_one_hot, apply_sparse, pad_to, SEP_TOKEN, PAD_TOKEN, DATA_RAW_DIR
import codecs
from . import quatrains
from .segment import *
import os



class ExtractUtil:

    def extract_couplets_with_tag(self, tag_dir, tag_name):
        tag_path = os.path.join(tag_dir, tag_name)
        if not os.path.exists(tag_path):
            raise ValueError('There is no valid tags')

        tag_sets = set()
        with codecs.open(tag_path, 'r', 'utf-8') as fin:
            # TODO: read from tags(default: one tag one line)
            line = fin.readline().strip()
            while line:
                tag_sets.add(line)
                line = fin.readline().strip()
        
        couplets_dict = quatrains.get_quatrains()
        couplets = [couplet['sentences'] for couplet in couplets_dict]

        seg = Segmenter()
        tag_couplet_path = os.path.join(DATA_PROCESSED_DIR, 'tag_couplets.txt')
        
        with open(tag_couplet_path, 'w') as fout:
            print('create tag_couplets.txt')

        data = []
        
        with codecs.open(tag_couplet_path, 'a', 'utf-8') as fout:
            for couplet in couplets:
                seg_list_0 = seg.segment(couplet[0])
                seg_list_1 = seg.segment(couplet[1])
                flag_0 = set(seg_list_0) & tag_sets
                flag_1 = set(seg_list_1) & tag_sets
                if flag_0 or flag_1:
                    fout.write(couplet[0])
                    fout.write('\n')
                    fout.write(couplet[1])
                    fout.write('\n')
                    fout.write('\n')
                    data.append(couplet)
        return data


if __name__ == '__main__':

    tag_dir = 'data/raw/'
    tag_name = 'tag.txt'
    extract = ExtractUtil()
    data = extract.extract_couplets_with_tag(tag_dir, tag_name)
    print("Size of the tag couplets: %d" % len(data))
        
            
        
