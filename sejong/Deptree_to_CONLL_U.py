
# coding: utf-8

# In[1]:

import codecs
import os
import re
from Deptree_to_CONLL_U_utils import *


directory = os.getcwd()+'/wdir/deptree.txt.v2.'
corpus_list = ['training', 'tuning', 'test']


# In[2]:

for corpus_type in corpus_list:
    corpus = directory + corpus_type
    with codecs.open(corpus, 'r') as readfile:
        OUT_FILENAME = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) +                                     '/models_sejong_conll/sejong_' + corpus_type+'.conllu'

        sentence = []
        error_sentence = False

        with codecs.open(OUT_FILENAME, 'w') as writefile:
            line_counter = 1
            id_counter = 1

            """
            writefile.write('ID' +'\t' + 'FORM' +'\t' + 'LEMMA' +'\t' + 'UPOSTAG' +'\t' + \
                            'XPOSTAG'  +'\t' +  'FEATS'  +'\t' +  'HEAD' +'\t' + 'DEPREL' +'\t' +\
                            'DEPS' +'\t' + 'MISC')
            """
            for line in readfile:
                if line == '\n':
                    if error_sentence == False:

                        sentence_to_write = ""
                        
                        for eoj_counter, eoj in enumerate(sentence):
                            for lemma_counter, lemma_dict in enumerate(eoj):

                                #UPOS
                                try:
                                    plusindex = lemma_dict['POS'].index('+')
                                    firstPOS = lemma_dict['POS'][:plusindex]
                                except:
                                    firstPOS = lemma_dict['POS']
                                    pass

                                #"""
                                if lemma_dict['HEAD'] == '_':
                                    eoj_head = lemma_dict['EOJ_HEAD']
                                    # print("eoj_head: ", eoj_head)
                                    for l_counter, l_dict in enumerate(sentence[int(eoj_head) - 1]):
                                        if l_dict['EOJ_INNER_HEAD'] == 0:
                                            lemma_dict['HEAD'] = l_dict['ID']
                                #"""    
                                
                                sentence_to_write += str(lemma_dict['ID']) + '\t' + str(lemma_dict['FORM']) + \
                                                            '\t' + str(lemma_dict['LEMMA']) + '\t' + str(firstPOS) + \
                                                            '\t' + str(lemma_dict['POS']) + \
                                                            '\t' + str('_') + \
                                                            '\t' + str(lemma_dict['HEAD']) + '\t' + str(lemma_dict['DEPREL']) + \
                                                            '\t' + str('_') + \
                                                            '\t' + str('_') + '\n'
                                                            
                        writefile.write(sentence_to_write)
                        writefile.write('\n')
                    
                    error_sentence = False
                    sentence = []
                    id_counter = 1

                
                else:
                    bucket = line.split('\t')
                    """
                    deptree v.2 는 어절별로 줄이 나누어져 있다.
                    bucket 은 한 줄을 읽어들인 것
                    
                    INPUT
                    ex)
                    0    1                   2                                                   3              4
                    ID   FORM            LEMMA + POS                                DEPREL     HEAD
                    1    도수안경의    도수/NNG + 안경/NNG + 의/JKG    NP_MOD    2 
                    
                    0: ID
                    1: FORM
                    2: LEMMA + POS
                    3. DEPREL
                    4. HEAD
                    
                    
                    OUTPUT
                    0    1         2           3        4               5                  6           7                8                   9                     10
                    ID   FORM  LEMMA  POS    DEPREL      EOJ              EOJ_ID    EOJ_HEAD  EOJ_LENGTH  EOJ_INNER_ID  EOJ_INNER_HEAD
                    1    도수    도수      NNG    NP_MOD    도수안경의   1            2               3                    1                    2
                    2    안경    안경      NNG    NP_MOD    도수안경의   1            2               3                    2                    0
                    3    의       의          JKG     NP_MOD    도수안경의   1            2               3                    3                    2
                            
                    
                    0: ID
                    1: FORM
                    2: LEMMA = FORM
                    3. POS
                    4. DEPREL
                    5. EOJ = 어절
                    6. EOJ_ID = 어절 ID (몇 번째 어절인지; 1부터 시작)
                    7. EOJ_HEAD  = 어절 HEAD (몇 번째 어절에게 dependent한지)
                    8. EOJ_LENGTH = 어절 크기 (어절 안에 형태소가 몇개인지)
                    9. EOJ_INNER_ID = 어절 내부 ID (어절 안에서 몇 번째인지; 1부터 시작)
                    10. EOJ_INNER_HEAD = 어절 내부에서의 HEAD 형태소가 어디인지 (1부터 시작)
                    
                    """
                    

                    #print(bucket)
                    
                    """
                    compress_eoj 사용
                    bucket[2] => compress_eoj(bucket[1], bucket[2])
                    """
                    compressed_bucket, num_lemma = compress_eoj(bucket[1], bucket[2])
                    #print("compressed_bucket: ", compressed_bucket)

                    """
                    if compressed_bucket == ' + /SW':
                        POS_math = ['SW']
                        Lemma_match = [' + ']

                    else:
                    """
                    Lemma_POS = re.split(' \+ ', compressed_bucket)
                    #POS_Lemma = re.split('[ +]+', bucket[2])
                    #print("Lemma_POS: "+str(Lemma_POS))
                    #print("Line: ", line_counter, Lemma_POS)

                    POS_match = []
                    Lemma_match = []
                    for Lemma_POS_x in Lemma_POS:
                        #print("Lemma_POS_x: ", Lemma_POS_x)

                        #"""
                        try:
                            temp_POS = re.findall('(\/[A-Z_+]+)', Lemma_POS_x)[0]
                            matched_POS = temp_POS[1:]
                            # findall은 리스트로 리턴하기 때문에 [0]
                            # 맨 앞의 / 는 제외하려고 [1:]
                            #print("matched_POS: ", matched_POS)
                        except IndexError as e:
                            print(e, "\n", "Line", line_counter, "contains errors at")
                            print(Lemma_POS, line[:-1])
                            print(bucket)
                            print(bucket[1], bucket[2])
                            print('compressed_bucket:', compressed_bucket)
                            error_sentence = True

                        matched_Lemma = Lemma_POS_x.replace(temp_POS, '')
                        #print("matched_Lemma: ", matched_Lemma)

                        POS_match.append(matched_POS)
                        Lemma_match.append(matched_Lemma)

                    """
                    INPUT
                    ex)
                    0    1                   2                                                   3              4
                    ID   FORM            LEMMA + POS                                DEPREL     HEAD
                    1    도수안경의    도수/NNG + 안경/NNG + 의/JKG    NP_MOD    2 
                    
                    0: ID
                    1: FORM
                    2: LEMMA + POS
                    3. DEPREL
                    4. HEAD
                    
                    
                    Intermediate_OUTPUT
                    0    1         2           3        4               5                  6           7                8                   9                     10
                    ID   FORM  LEMMA  POS    DEPREL      EOJ              EOJ_ID    EOJ_HEAD  EOJ_LENGTH  EOJ_INNER_ID  EOJ_INNER_HEAD
                    1    도수    도수      NNG    NP_MOD    도수안경의   1            2               3                    1                    2
                    2    안경    안경      NNG    NP_MOD    도수안경의   1            2               3                    2                    0
                    3    의       의          JKG     NP_MOD    도수안경의   1            2               3                    3                    2
                            
                    
                    0: ID
                    1: FORM
                    2: LEMMA = FORM
                    3. POS
                    4. DEPREL
                    5. EOJ = 어절
                    6. EOJ_ID = 어절 ID (몇 번째 어절인지; 1부터 시작)
                    7. EOJ_HEAD  = 어절 HEAD (몇 번째 어절에게 dependent한지)
                    8. EOJ_LENGTH = 어절 크기 (어절 안에 형태소가 몇개인지)
                    9. EOJ_INNER_ID = 어절 내부 ID (어절 안에서 몇 번째인지; 1부터 시작)
                    10. EOJ_INNER_HEAD = 어절 내부에서의 HEAD 형태소가 어디인지 (1부터 시작)
                    11. HEAD
                    """
                    line_list = []
                    for eoj_inner_id_counter in range(num_lemma):
                         line_list.append({})
                    
                    
                    eojs_to_write = []
                    eoj_deprel = ''
                    eoj_pos_list = []
                    eoj_form_list = []

                    for eoj_inner_id_counter, lemma_dict in enumerate(line_list):
                        #print('eoj_inner_id_counter: ', eoj_inner_id_counter)
                        #print('id_counter: ', id_counter)
                        #print(Lemma_match)
                        lemma_dict['ID'] = id_counter
                        lemma_dict['FORM'] = Lemma_match[eoj_inner_id_counter]
                        lemma_dict['LEMMA'] = lemma_dict['FORM']
                        lemma_dict['POS'] = POS_match[eoj_inner_id_counter]
                        lemma_dict['DEPREL'] = bucket[3]
                        lemma_dict['EOJ'] = bucket[1]
                        lemma_dict['EOJ_ID'] = bucket[0]
                        lemma_dict['EOJ_HEAD'] = bucket[4][:-1]
                        lemma_dict['EOJ_LENGTH'] = num_lemma
                        lemma_dict['EOJ_INNER_ID'] = eoj_inner_id_counter + 1
                        
                        id_counter +=1
                        
                        eoj_deprel = lemma_dict['DEPREL']
                        eoj_pos_list.append(lemma_dict['POS'])
                        eoj_form_list.append(lemma_dict['FORM'])
                        
                    #for eoj_inner_id_counter, lemma_dict in enumerate(line_list):
                    #    print(eoj_inner_id_counter, lemma_dict)
                        
                    #print("원래 어절: ", bucket[1]) # 어절
                    #print('eoj_deprel: ', eoj_deprel)
                    #print('eoj_pos_list: ', eoj_pos_list)
                    #print('eoj_form_list: ', eoj_form_list)
                   
                    for eoj_inner_id_counter, lemma_dict in enumerate(line_list):
                        # INNER_HEAD 추가!
                        #def eoj_find_inner_head(DEPREL, POS_List, num_lemma, FORM_List):
                        lemma_dict['EOJ_INNER_HEAD'] = eoj_find_inner_head(eoj_deprel, eoj_pos_list, num_lemma, eoj_form_list)[eoj_inner_id_counter]
        
                    eoj_head = 0
                    id_list = []
                    eoj_inner_id_list = []
                    eoj_inner_head_list = []
                    for eoj_inner_id_counter, lemma_dict in enumerate(line_list):
                        eoj_head = int(lemma_dict['EOJ_HEAD'])
                        id_list.append(lemma_dict['ID'])
                        eoj_inner_id_list.append(lemma_dict['EOJ_INNER_ID'])
                        eoj_inner_head_list.append(lemma_dict['EOJ_INNER_HEAD'])
                        
                    
                    #print('eoj_head: ', eoj_head)
                    #print('id_list: ', id_list)
                    #print('eoj_inner_id_list: ', eoj_inner_id_list)
                    #print('eoj_inner_head_list: ', eoj_inner_head_list)
                    #print('num_lemma: ', num_lemma)
                    
                    head_list = find_head(eoj_head, id_list, eoj_inner_id_list, eoj_inner_head_list, num_lemma)
                    
                    #print('head_list: ', head_list)
                    
                    
                    for eoj_inner_id_counter, lemma_dict in enumerate(line_list):
                        lemma_dict['HEAD'] = head_list[eoj_inner_id_counter]
                    
                    for eoj_inner_id_counter, lemma_dict in enumerate(line_list):
                        # 출력
                        eojs_to_write.append(lemma_dict)

                    #print(lines_to_write)
                    #break
                    
                    sentence.append(eojs_to_write)
                
                line_counter += 1
                
            print(str(OUT_FILENAME)+ " converted!")

