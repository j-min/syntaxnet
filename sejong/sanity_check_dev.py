
# coding: utf-8

# In[1]:

import codecs
import os
import re
from Deptree_to_CONLL_U_utils import *


# In[2]:

directory = os.getcwd()+'/wdir/sejong_treebank.txt.v1.'
corpus_list = ['training', 'tuning', 'test']


# In[3]:

def merge_dicts(*dicts):
    d = {}
    for dict in dicts:
        for key in dict:
            try:
                d[key].append(dict[key])
            except KeyError:
                d[key] = [dict[key]]
    return d


def allfiles(path):
    res = []
    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            res.append(filepath)
    return res


# In[10]:

def Dev_search(keyword):
    
    allfilelist = allfiles(os.getcwd()+'/raw_corpus')
    sejonglist = [file for file in allfilelist if "BG" in file]
    # print(sejonglist)
    err_counter = 0
    
    for file_counter, rawfile in enumerate(sejonglist):

        with codecs.open(rawfile, "r", encoding = "utf-16-le") as readfile:
            #OUT_FILENAME = os.getcwd()+"/stripped/"+rawfile[-12:-4]+"_stripped.txt"
            first_line = True
            whitespace_chars = ['(', ')', '<', '>', '{', '}', '[', ']', '-']

            line_counter = 1

            for line in readfile:
                if "; " == line[0:2]:
                    if first_line == False:
                        #writefile.write("\n")
                        pass


                if keyword in line:
                    err_counter += 1
                    print('filename: ', rawfile[-12:-4])
                    print('line_number: ', line_counter)
                    print(line.strip())
                    print('num_error: ', err_counter)

                line_counter += 1


# In[11]:

temp_counter = 0
error_occured = False
total_dict = {}
file_dict = {}
sentence_dict ={}
for corpus_type in corpus_list:
    corpus = directory + corpus_type
    file_dict = {}
    
    with codecs.open(corpus, 'r') as readfile:
            #sentence_dict ={}
            
            original_bucket = []
            eoj_counter = 0
            
            for line in readfile:
                
                if error_occured == True:
                    raise SystemExit
                
                try:
                    if line == '\n':
                        original_bucket = []
                        #sentence_dict = {}
                        eoj_counter = 0

                    elif "; " in line:
                        #temp_line = line.replace('─', ' ─ ')
                        original_sentence = line[2:].strip()
                        original_bucket = original_sentence.split(' ')
                        num_eoj = len(original_bucket)
                        #print("original bucket: ", original_bucket)
                        eoj_counter = 0


                    elif ('(' in line) and (')' in line) and ('\t' in line):
                        #print(eoj_counter))
                        eoj = original_bucket[eoj_counter]
                        #print('eoj: ', eoj)
                        ###matched = re.match('(.*)(\([A-Z_]+ *\t*)+([^\(\)]+)([\)]+)', line).group(3)
                        matched = re.match('(.*)(\([A-Z_]+ *\t*)+(.+[A-Z]+)([\)]+)', line).group(3)
                        #print('matched: ', matched)
                        compressed, num_lemma = compress_eoj(eoj, matched)

                        #print("compressed: ", compressed)


                        sentence_dict.setdefault(eoj, [])
                        sentence_dict[eoj].append(compressed)

                        #print("sentence_dict: ", sentence_dict)

                        eoj_counter += 1

                        temp_counter += 1
                except:
                    print('Error Detected!')
                    print('original_sentence: ', original_sentence)
                    print('original_bucket: ', original_bucket)
                    #print('line: ', line)
                    Dev_search(original_sentence[:-1])
                    error_occured = True

            #file_dict = merge_dicts(file_dict, sentence_dict)
            print('Check: ' + corpus_type + " corpus done!")
            #print("file_dict: ", file_dict)
            
    #total_dict = merge_dicts(total_dict, file_dict)

from collections import Counter

#print("total dict: ", total_dict)
num_total_eoj = len(sentence_dict)
differently_splitted_eoj_counter = 0
weighted_diffrently_splitted_eoj_counter = 0
total_splitted_eoj_counter = 0
for eoj_i, eoj in enumerate(sentence_dict.keys()):
    splitted_eoj = sentence_dict[eoj]
    set_splitted_eoj = set(splitted_eoj)

    count = Counter(splitted_eoj)

    num_differently_splitted = len(set_splitted_eoj)
    weighted_num_differently_splitted = len(splitted_eoj)

    if num_differently_splitted == 1:
        pass
    else:
        differently_splitted_eoj_counter += 1
        weighted_diffrently_splitted_eoj_counter += count.most_common()[0][1]
        total_splitted_eoj_counter += weighted_num_differently_splitted

print('number of different eojs: ', num_total_eoj)
print('number of differently splitted eojs: ', differently_splitted_eoj_counter,
      differently_splitted_eoj_counter/num_total_eoj*100,'%')
print('weighted percentage: ', weighted_diffrently_splitted_eoj_counter/total_splitted_eoj_counter*100, '%')

f = open(os.getcwd()+'/pos_table.txt', 'wb')
import pickle
pickle.dump(sentence_dict, f)
f.close()