from .utils import DATA_RAW_DIR
import codecs
import random

all_usable = []
with codecs.open('data/raw/all_usable.txt', 'r', 'utf-8') as fin:
    # TODO: read from tags(default: one tag one line)
	line1 = fin.readline().strip()
	line2 = fin.readline().strip()
	fin.readline().strip()
	while line1 and line2:
		all_usable.append([line1,line2])
		line1 = fin.readline().strip()
		line2 = fin.readline().strip() 
		fin.readline().strip()
print('finished read')
couplet_weak = []
with codecs.open('data/raw/couplet_weak.txt', 'r', 'utf-8') as fin:
    # TODO: read from tags(default: one tag one line)
	line1 = fin.readline().strip()
	line2 = fin.readline().strip()
	fin.readline().strip()
	while line1 and line2:
		couplet_weak.append([line1,line2])
		line1 = fin.readline().strip()
		line2 = fin.readline().strip() 
		fin.readline().strip()
print('finished read')
tangshi_duizhang = []
with codecs.open('data/raw/tangshi_duizhang.txt', 'r', 'utf-8') as fin:
    # TODO: read from tags(default: one tag one line)
	line1 = fin.readline().strip()
	line2 = fin.readline().strip()
	fin.readline().strip()
	while line1 and line2:
		tangshi_duizhang.append([line1,line2])
		line1 = fin.readline().strip()
		line2 = fin.readline().strip() 
		fin.readline().strip()
print('finished read')
couplet = []
with codecs.open('data/raw/couplet.txt', 'r', 'utf-8') as fin:
    # TODO: read from tags(default: one tag one line)
	line1 = fin.readline().strip()
	line2 = fin.readline().strip()
	fin.readline().strip()
	while line1 and line2:
		couplet.append([line1,line2])
		line1 = fin.readline().strip()
		line2 = fin.readline().strip() 
		fin.readline().strip()
print('finished read')
data = []
data.extend(all_usable)
data.extend(couplet_weak)
data.extend(tangshi_duizhang)
result = []

for i in range(len(couplet)):
	index = random.randint(0,len(data))
	result.append(data[index])
result.extend(couplet)
result.extend(couplet)
with open('data/raw/merge_data.txt', 'w') as fout:
    print('create merge_data.txt')

with codecs.open('data/raw/merge_data.txt', 'a', 'utf-8') as fout:
    for couplet in result:
        fout.write(couplet[0])
        fout.write('\n')
        fout.write(couplet[1])
        fout.write('\n')
        fout.write('\n')
            