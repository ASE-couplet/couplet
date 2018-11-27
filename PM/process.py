import json
import os
from tqdm import tqdm
items = []
f = open('./items.txt','r', encoding='utf-8')
for line in f.readlines():
    items.append(line.strip())
print(items)
f_list = []
for dir,_,files in os.walk("./poetry/songci"):
    for file in files:
        f_list.append(os.path.join(dir, file))
for item in tqdm(items):
    f_out = open('./songci_extract/'+item+'.txt','w',encoding='utf-8')
    for file in f_list:
        file_data = open(file,'r', encoding='utf-8').read()
        text = json.loads(file_data)
        for poet in text:
            poet = poet['paragraphs']
            for line in poet:
                if line.find(item) != -1:
                    for line in poet:
                        f_out.write(line)
                        f_out.write('\n')
                    f_out.write('\n')
