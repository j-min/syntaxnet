
# coding: utf-8

# In[1]:

import codecs
import os
import re


directory = os.getcwd()+'/wdir/deptree.txt.v2.'
corpus_list = ['training', 'tuning', 'test']


# In[2]:

"""
1. ID: Word index, integer starting at 1 for each new sentence; may be a range for tokens with multiple words.
2. FORM: Word form or punctuation symbol.
3. LEMMA: Lemma or stem of word form.
4. UPOSTAG: Universal part-of-speech tag drawn from our revised version of the Google universal POS tags.
5. XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
6. FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
7. HEAD: Head of the current token, which is either a value of ID or zero (0).
8. DEPREL: Universal Stanford dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
9. DEPS: List of secondary dependencies (head-deprel pairs).
10. MISC: Any other annotation.
"""


# In[4]:

for corpus_type in corpus_list:
    corpus = directory + corpus_type
    with codecs.open(corpus, 'r') as readfile:
        OUT_FILENAME = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/models_sejong_conll/sejong_' + corpus_type

        sentence_buffer = ""
        error_sentence = False
        # print_dict = {'ID', 'FORM', 'LEMMA', 'UPOSTAG', 'XPOSTAG', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC'}
        with codecs.open(OUT_FILENAME, 'w') as writefile:
            line_counter = 1
            
            for line in readfile:
                if line == '\n':
                    if error_sentence == False:
                        sentence_buffer += '\n'
                        writefile.write(sentence_buffer)
                    
                    error_sentence = False
                    sentence_buffer = ""

                
                else:
                    bucket = line.split('\t')
                    """
                    0: ID
                    1: FORM
                    2: LEMMA + POS
                    3. DEPREL
                    4. HEAD
                    """
                    print_dict = dict()
                    POS = []
                    Lemma = []
                    #print(bucket)
                    
                    POS_Lemma = re.split('[ +]+', bucket[2])
                    #print("POS_Lemma: "+str(POS_Lemma))
                    # print(line_counter, POS_Lemma)
                    
                    POS_match = []
                    Lemma_match = []
                    for POS_Lemma_x in POS_Lemma:
                        #print("POS_Lemma_x: ", POS_Lemma_x)
                        
                        try:
                            matched_POS = re.findall('(\/[A-Z_]+)', POS_Lemma_x)[0][1:]
                            #print("matched_POS: ", matched_POS)
                        except IndexError as e:
                            print(e, "\n", "Line ", line_counter, " contains errors at")
                            print(POS_Lemma, line)
                            error_sentence = True


                        matched_Lemma = re.sub(matched_POS, '', POS_Lemma_x)[:-1]
                        #print("matched_Lemma:", matched_Lemma)
                        
                        POS_match.append(matched_POS)
                        Lemma_match.append(matched_Lemma)
                    
                    #print("POS_match: "+str(POS_match))
                    #print("Lemma_match: " + str(Lemma_match))
                    

                    POS = '+'.join(POS_match)
                    #print("POS: "+POS)
                    
                    #Lemma = re.findall('(.*)(\/[A-Z_]+)', bucket[2])
                    #print(Lemma.groups())
                    
                    # Lemma_match = re.findall('([]\/)')


                    print_dict['ID'] = bucket[0]
                    print_dict['FORM'] = bucket[1]
                    print_dict['LEMMA'] = Lemma_match[0]
                    print_dict['UPOSTAG'] = POS_match[0]
                    print_dict['XPOSTAG'] = POS
                    print_dict['FEATS'] = '_'
                    print_dict['HEAD'] = bucket[4][:-1]
                    print_dict['DEPREL'] = bucket[3]
                    print_dict['DEPS'] = '_'
                    print_dict['MISC'] = '_'
                    
                    line_to_write = str(print_dict['ID']) + '\t' + str(print_dict['FORM']) +                                     '\t' + str(print_dict['LEMMA']) + '\t' + str(print_dict['UPOSTAG']) +                                     '\t' + str(print_dict['XPOSTAG']) + '\t' + str(print_dict['FEATS']) +                                     '\t' + str(print_dict['HEAD']) + '\t' + str(print_dict['DEPREL']) +                                     '\t' + str(print_dict['DEPS']) + '\t' + str(print_dict['MISC']) + '\n'
                            
                    #print(line_to_write)
                    #break
                    
                    sentence_buffer += line_to_write
                line_counter += 1
            print(str(OUT_FILENAME)+ " converted!")


# In[4]:

print("All Sejong Corpora have been converted!")

