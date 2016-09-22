# coding: utf-8
import re

def compress_eoj(FORM, LEMMA_POS):
    """
    Input:

    FORM: '수영할'
    LEMMA_POS: '수영/NNG + 하/XSV + ㄹ/ETM'

    OUTPUT:
    Compressed_LEMMA_POS: '수영/NNG + 할/XSV+ETM'

    """

    """
    FORM: 도수안경의
    LEMMA_POS:  도수/NNG + 안경/NNG + 의/JKG

    For Debug => compress_eoj('도수안경의', '도수/NNG + 안경/NNG + 의/JKG')
    """

    sniparray = []
    sniparrayOrigin = []
    posarray = []

    if LEMMA_POS == ' + /SW':
        return ' + /SW', 1

    snip_pairs = re.split(' \+ ', LEMMA_POS)  # +sign needs to be escaped in regex #던지/VV + 어/EC
    """
    snip_pairs
    = ['도수/NNG', '안경/NNG', '의/JKG']
    """
    snip_pairs_2d = []

    for snip_pair in snip_pairs:
        # line_counter += 1
        # print ("snip_pair = ", snip_pair) #던지/VV
        m2 = re.match('^(.+)\/([^\/]+)$', snip_pair)
        if m2:
            snip = m2.group(1)
            pos = m2.group(2)
            # print ("line", line_counter)
            # print ("snip", snip)
            # print ("pos", pos)
            # print (line_counter,"\t",snip,"\t",pos)
            snip_pairs_2d.append([snip, pos])

    """
    snip_pairs_2d
    = [['도수', 'NNG'],
        ['안경', 'NNG'],
        ['의', 'JKG']]
    """

    word = FORM
    """
    word = '도수안경의'
    """

    # print (snip_pairs_2d)
    # print (word)

    buffer_start = 0
    bufer_end = len(snip_pairs_2d) - 1
    snipbuffer = []
    posbuffer = []

    # word = list(word)
    # print(word)
    word_counter = 0

    end_of_sequence = False
    buffer = False
    for snip_pair in snip_pairs_2d:
        """
        snip_pairs_2d
        = [['도수', 'NNG'],
            ['안경', 'NNG'],
            ['의', 'JKG']]
        snip_pair = ['도수', 'NNG'], ['안경', 'NNG'], ['의', 'JKG']

        ex) 첫번째 foor loop
        => snip_pair = ['도수', 'NNG'] 일 때
        => snip_pair[0] = '도수'  &   snip_pair[1] = 'NNG'
        """
        if snip_pairs_2d[-1] == snip_pair:
            end_of_sequence = True

            # 4 cases
            # 1) if snippet is inside the word & no buffer
            # 2) if snippet is inside the word & there is buffer
            # 3) if snippet is NOT inside the word & no buffer
            # 4) if snippet is NOT inside the word & there is buffer

            # 1) if snippet is inside the word & no buffer
            # => Print current word
        if (snip_pair[0] in word[word_counter:]) and (buffer == False):
            #print(1)
            sniparray.append([snip_pair[0]])
            sniparrayOrigin.append([snip_pair[0]])
            posarray.append([snip_pair[1]])

            buffer_start += len(snip_pair[0])
            buffer = False

            word_counter += 1

            # 2) if snippet is inside the word & there is buffer
            # => Print Buffer and Print current word
        elif (snip_pair[0] in word[word_counter:]) and (buffer == True):
            #print(2)
            # print("Where is corresponding word:" word.index(snip_pair[0]))
            buffer_end = word.index(snip_pair[0])
            snipbuffer = word[buffer_start:buffer_end]

            if snipbuffer == '':
                # posarray.append(posbuffer)
                sniparray.append([snip_pair[0]])
                posbuffer.extend([snip_pair[1]])
                posarray.append(posbuffer)
            else:
                sniparray.append([snipbuffer])
                posarray.append(posbuffer)
                sniparray.append([snip_pair[0]])
                posarray.append([snip_pair[1]])
            sniparrayOrigin.append([snip_pair[0]])

            buffer_start += len(snip_pair[0])

            # sniparray.append([snip_pair[0]])
            # posarray.append([snip_pair[1]])

            buffer = False

            word_counter += 1

            # 3) if snippet is NOT inside the word & no buffer
            # if End of Sequence => Print current word
            # if not end of sequence => Do Not Print Buffer, Buffer Start
        elif not (snip_pair[0] in word[word_counter:]) and (buffer == False):

            if end_of_sequence == True:
                #print("3-1")
                # Print Current word(=remaining part in the 'word')
                snipbuffer = word[buffer_start:]

                if snipbuffer == '':
                    posarray[-1].extend([snip_pair[1]])
                else:
                    posarray.append([snip_pair[1]])
                    sniparray.append(snipbuffer)
                    sniparrayOrigin.append([snip_pair[0]])

                word_counter += 1

            else:
                #print("3-2")
                # Buffer Start!
                # snip buffer will be formed right before when buffer is eliminated
                # just don't change buffer_start
                posbuffer = []
                posbuffer.append(snip_pair[1])
                # sniparrayOrigin.append(snip_pair[0])
                sniparrayOrigin.append([snip_pair[0]])
                buffer = True

                word_counter += 1

                # 4) if snippet is NOT inside the word & there is buffer
                # if End of Sequence => Print Buffer and print current word
                # if not end of sequence => Add buffer
        else:
            if end_of_sequence == True:
                #print("4-1")
                # Print Buffer and print current word
                # buffer_end = len(word)-1
                snipbuffer = word[buffer_start:]
                sniparray.append([snipbuffer])
                sniparrayOrigin.append(snip_pair[0])

                posbuffer.append(snip_pair[1])
                posarray.append(posbuffer)

                word_counter += 1
            else:
                #print("4-2")
                # Add buffer
                posbuffer.append(snip_pair[1])

                word_counter += 1

        if end_of_sequence == True:
            continue

    #print ("snipbuffer: ", snipbuffer)
    #print ("posbuffer: ", posbuffer)
    #print ("sniparray: ", sniparray)
    #print ("posarray: ", posarray)
    # print ("sniparrayOrigin: ", sniparrayOrigin)
    num_lemma = len(sniparray)
    temp_list = []
    # output_compressed_LEMMA_POS = ""
    for i in range(len(sniparray)):
        temp_list.append(sniparray[i][0] + '/' + '+'.join(posarray[i]))

    #print(temp_list)
    output_compressed_LEMMA_POS = ' + '.join(temp_list)
    return output_compressed_LEMMA_POS, num_lemma


def eoj_find_inner_head(DEPREL, POS_List, num_lemma, FORM_List):
    """
    DEPREL(구문 표지) 에 따라,
    어절 내의 lemma 들이 어떤 lemma에 종속되어 있는지 출력
    => 어떤 head lemma를 가지는지 출력

    INPUT
    * DEPREL: 세종 코퍼스 구문 표지 (string)
    * POS_LIST: 각 lemma의 POS
    * num_lemma: lemma가 총 몇 개인지
    * FORM_List:  lemma_list 디버그용
    ex) 'VP', ['MAG','VV','EF', 'SF'], 4, ['안', '나오', '는데', '.']

    OUTPUT
    * HEAD_LIST: 각 lemma가 가리키는 head lemma의 index
                        (1부터 시작; root 이면 0) => 맨 마지막 리턴 직전에 +1 해서 보정

    """
    root_is_specified = False
    head_list = ['not_specified'] * num_lemma
    where_root_is = 99

    if num_lemma == 1:
        where_root_is = 0
        head_list = [0]
        root_is_specified = True

    elif 'NP' in DEPREL:
        """
        체언구 (일반명사 NNG, 고유명사 NNP, 의존명사 NNB, 대명사 NP, 수사 NR)

        원래 체언이 있어야 하는데...
        체언이 없고 어근 XR이 root으로 존재하는 경우가 있음 => 어근을 root로
        어근이 없고 숫자만 존재하는 경우가 있음 => 첫 번째 형태소를 root로
        """
        num_N = 0
        for i, pos in enumerate(POS_List):
            # if any(x in str for x in a):
            if any(x in pos for x in ['NNG', 'NNP', 'NNB', 'NP', 'NR']):
                head_list[i] = 'N'
                num_N += 1

            else:
                # for i, pos in enumerate(POS_List):
                """
                의존형태

                어근(XR)
                => 바로 뒷 lemma가 여기에 종속
                # => 접미사와 항상 같이 쓰이기 때문에 생략

                접두사(XPN)
                => 바로 뒷 lemma에 종속

                어미(EP, EF, EC, ETN, ETM), 접미사(XSN, XSV, XSA), 기호(SF), 보조사(JX)
                => 바로 앞 lemma에 종속
                """
                if not num_lemma == 1:
                    if 'XR' in pos:
                        head_list[i + 1] = i
                    elif 'XPN' in pos:
                        head_list[i] = i + 1
                    elif any(x in pos for x in ['EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA', 'SF', 'JX']):
                        head_list[i] = i - 1

        if num_N == 0:
            # 체언이 1개도 없을 때

            # 어근이 있을 때=> 어근이 root
            # 어근이 없을 때 => 첫 번째가 root
            try:
                where_root_is = POS_List.index('XR')
            except:
                where_root_is = 0
            head_list[where_root_is] = 0

            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

        elif num_N == 1:
            # 체언이 1개일 때 => 그 체언이 root
            where_root_is = head_list.index('N')
            head_list[where_root_is] = 0
            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

        else:
            # 체언이 2개 이상일 때 => 맨 끝에 위치한 체언이 root

            where_Ns_are = [i for i, x in enumerate(head_list) if x == 'N']
            # 체언들의 위치 출력

            for i in where_Ns_are:
                head_list[i] = 'not_specified'
            where_root_is = max(where_Ns_are)
            head_list[where_root_is] = 0
            # 맨 끝에 위치한 체언이 root
            # 나머지는 초기화

            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

    elif 'VP' in DEPREL:
        """
        용언구
        동사 VV, 형용사 VA, 보조용언VX, 부정지정사 VCN

        위의 용언이 없으면 => NP, NR, NN-, XR, MAG, SH, IC이 root
        아니면 맨앞
        """
        num_V = 0
        for i, pos in enumerate(POS_List):
            # if any(x in str for x in a):
            if any(x in pos for x in ['VV', 'VA', 'VX', 'VCN']):
                head_list[i] = 'V'
                num_V += 1

            # print(head_list)
            else:
                #for i, pos in enumerate(POS_List):
                """
                의존형태

                어근(XR)
                => 바로 뒷 lemma가 여기에 종속
                # => 접미사와 항상 같이 쓰이기 때문에 생략

                접두사(XPN)
                => 바로 뒷 lemma에 종속

                어미(EP, EF, EC, ETN, ETM), 접미사(XSN, XSV, XSA), 기호(SF), 보조사(JX)
                => 바로 앞 lemma에 종속
                """
                if not num_lemma == 1:
                    if 'XR' in pos:
                        head_list[i + 1] = i
                    elif 'XPN' in pos:
                        head_list[i] = i + 1
                    elif any(x in pos for x in ['EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA', 'SF', 'JX']):
                        head_list[i] = i - 1

        # print(head_list)

        if num_V == 0:
            # 용언이 1개도 없을 때 => XR, NN-, NR, MAG, SH가 root

            for i, pos in enumerate(POS_List):
                if any(x in pos for x in ['NR', 'NP', 'XR', 'NN', 'MAG', 'SH', 'IC']):
                    where_root_is = i
                    root_is_specified = True

            if where_root_is == 99:
                where_root_is = 0
                root_is_specified = True

            head_list[where_root_is] = 0
            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

        elif num_V == 1:
            # 용언이 1개일 때 => 그 용언이 root

            where_root_is = head_list.index('V')
            head_list[where_root_is] = 0
            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

        else:
            # 용언이 2개 이상일 때 => 첫 용언이 root

            where_Vs_are = [i for i, x in enumerate(head_list) if x == 'V']
            # 용언들의 위치 출력

            for i in where_Vs_are:
                head_list[i] = 'not_specified'
            where_root_is = min(where_Vs_are)
            head_list[where_root_is] = 0
            # 첫 용언이 root
            # 나머지는 초기화

            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

            # print(head_list)

    elif 'VNP' in DEPREL:
        """
        긍정지정사구
        VCP가 들어있는 것
        root는 체언 또는 용언
        """
        num_N_V = 0
        num_N = 0
        num_V = 0
        for i, pos in enumerate(POS_List):
            if any(x in pos for x in ['NNG', 'NNP', 'NNB', 'NP', 'NR', 'VV', 'VA', 'VX', 'VCN']):
                num_N_V += 1
                if any(x in pos for x in ['NNG', 'NNP', 'NNB', 'NP', 'NR']):
                    num_N += 1
                    head_list[i] = 'N'
                elif any(x in pos for x in ['VV', 'VA', 'VX', 'VCN']):
                    num_V += 1
                    head_list[i] = 'V'

                else:
                    # for i, pos in enumerate(POS_List):
                    """
                    의존형태

                    어근(XR)
                    => 바로 뒷 lemma가 여기에 종속
                    # => 접미사와 항상 같이 쓰이기 때문에 생략

                    접두사(XPN)
                    => 바로 뒷 lemma에 종속

                    어미(EP, EF, EC, ETN, ETM), 접미사(XSN, XSV, XSA), 기호(SF), 보조사(JX)
                    => 바로 앞 lemma에 종속
                    """
                    if not num_lemma == 1:
                        if 'XR' in pos:
                            head_list[i + 1] = i
                        elif 'XPN' in pos:
                            head_list[i] = i + 1
                        elif any(x in pos for x in ['EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA', 'SF', 'JX']):
                            head_list[i] = i - 1

        if (num_N_V == 0):
            root_is_specified = False
            print ('root is not specified')
            print (FORM_List)
            print (POS_List)

        elif num_N_V == 1:
            if num_N == 1:
                # 체언이 1개일 때 => 그 체언이 root
                where_root_is = head_list.index('N')
                head_list[where_root_is] = 0
                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True
            else:
                # 용언이 1개일 때 => 그 용언이 root
                where_root_is = head_list.index('V')
                head_list[where_root_is] = 0
                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True

        else:
            if num_N > 1:
                # 체언이 2개 이상일 때 => 맨 끝에 위치한 체언이 root
                # 용언과 섞여있으면 체언이 우선

                where_Ns_are = [i for i, x in enumerate(head_list) if x == 'N']
                # 체언들의 위치 출력
                for i in where_Ns_are:
                    head_list[i] = 'not_specified'
                where_Vs_are = [i for i, x in enumerate(head_list) if x == 'V']
                # 용언들의 위치 출력
                for i in where_Vs_are:
                    head_list[i] = 'not_specified'
                where_root_is = max(where_Ns_are)
                head_list[where_root_is] = 0
                # 맨 끝에 위치한 체언이 root
                # 나머지는 초기화

                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True

            else:
                # 용언이 2개 이상일 때 => 첫 용언이 root

                where_Vs_are = [i for i, x in enumerate(head_list) if x == 'V']
                # 용언들의 위치 출력

                for i in where_Vs_are:
                    head_list[i] = 'not_specified'
                where_root_is = min(where_Vs_are)
                head_list[where_root_is] = 0
                # 첫 용언이 root
                # 나머지는 초기화

                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True


    elif 'AP' in DEPREL:
        """
        부사구

        일반부사 MAG, 접속부사 MAJ
        거의 단일 형태소로 구성

        NNG와 결합
        기운/NNG + 없이/MAG

        용언과 결합
        자/VV + 나/EC + 깨/VV + 나/EC

        복합형태-거의 없음
        AP 애/NA + -/SS + 앵/MAG + -/SS + ./SP
        AP 시/NNG + 도/JX + 때/NNG + 도/JX + 없이/MAG


        AP[A-Z_]* [ㄱ-ㅣ가-힣]+/[^M] 로 검출
        """
        num_N_V = 0
        num_N = 0
        num_V = 0
        for i, pos in enumerate(POS_List):
            if any(x in pos for x in ['NNG', 'NNP', 'NNB', 'NP', 'NR', 'VV', 'VA', 'VX', 'VCN']):
                num_N_V += 1
                if any(x in pos for x in ['NNG', 'NNP', 'NNB', 'NP', 'NR']):
                    num_N += 1
                    head_list[i] = 'N'
                elif any(x in pos for x in ['VV', 'VA', 'VX', 'VCN']):
                    num_V += 1
                    head_list[i] = 'V'

                else:
                    # for i, pos in enumerate(POS_List):
                    """
                    의존형태

                    어근(XR)
                    => 바로 뒷 lemma가 여기에 종속
                    # => 접미사와 항상 같이 쓰이기 때문에 생략

                    접두사(XPN)
                    => 바로 뒷 lemma에 종속

                    어미(EP, EF, EC, ETN, ETM), 접미사(XSN, XSV, XSA), 기호(SF), 보조사(JX)
                    => 바로 앞 lemma에 종속
                    """
                    if not num_lemma == 1:
                        if 'XR' in pos:
                            head_list[i + 1] = i
                        elif 'XPN' in pos:
                            head_list[i] = i + 1
                        elif any(x in pos for x in ['EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA', 'SF', 'JX']):
                            head_list[i] = i - 1

        if num_N_V == 0:
            # MAG 또는 MAJ가 Root
            try:
                where_root_is = POS_List.index('MAG')
            except:
                where_root_is = POS_List.index('MAJ')
            head_list[where_root_is] = 0
            for i, pos in enumerate(head_list):
                if pos == 'not_specified':
                    head_list[i] = where_root_is
            root_is_specified = True

        #elif not (num_N_V == num_N) and not (num_N_V == num_V):
        #    root_is_specified = False
        #    print ('root is not specified')
        #    print (FORM_List)
        #    print (POS_List)


        elif num_N_V == 1:
            if num_N == 1:
                # 체언이 1개일 때 => 그 체언이 root
                where_root_is = head_list.index('N')
                head_list[where_root_is] = 0
                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True
            else:
                # 용언이 1개일 때 => 그 용언이 root
                where_root_is = head_list.index('V')
                head_list[where_root_is] = 0
                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True

        else:
            if num_N > 1:
                # 체언이 2개 이상일 때 => 맨 끝에 위치한 체언이 root
                # 용언과 섞여있으면 체언이 우선

                where_Ns_are = [i for i, x in enumerate(head_list) if x == 'N']
                # 체언들의 위치 출력
                for i in where_Ns_are:
                    head_list[i] = 'not_specified'
                where_Vs_are = [i for i, x in enumerate(head_list) if x == 'V']
                # 용언들의 위치 출력
                for i in where_Vs_are:
                    head_list[i] = 'not_specified'
                where_root_is = max(where_Ns_are)
                head_list[where_root_is] = 0
                # 맨 끝에 위치한 체언이 root
                # 나머지는 초기화

                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True

            else:
                # 용언이 2개 이상일 때 => 첫 용언이 root

                where_Vs_are = [i for i, x in enumerate(head_list) if x == 'V']
                # 용언들의 위치 출력

                for i in where_Vs_are:
                    head_list[i] = 'not_specified'
                where_root_is = min(where_Vs_are)
                head_list[where_root_is] = 0
                # 첫 용언이 root
                # 나머지는 초기화

                for i, pos in enumerate(head_list):
                    if pos == 'not_specified':
                        head_list[i] = where_root_is
                root_is_specified = True
    elif 'DP' in DEPREL:
        """
        관형사구

        대부분이 단일 MM으로 사용됨

        유일한 예외는 숫자
        DP 열/NR + 네/MM

        => 모두 MM을 root로
        """
        where_root_is = POS_List.index('MM')
        head_list[where_root_is] = 0

        for i, pos in enumerate(head_list):
            if pos == 'not_specified':
                head_list[i] = where_root_is
        root_is_specified = True
    elif 'IP' in DEPREL:
        """
        감탄사구

        대부분이 IC 단일 어절

        역시 모두 IC를 root 로
        없으면 MAG가 root
        없으면 중간(내림)
        """
        #print("check_1")
        for i, pos in enumerate(POS_List):
            if any(x in pos for x in ['IC', 'MAG']):
                where_root_is = i
                root_is_specified = True

        if where_root_is == 99:
            #print("check_2")
            where_root_is = int(num_lemma/2)
            root_is_specified = True

        #print("where_root_is: ", where_root_is)
        head_list[where_root_is] = 0

        for i, pos in enumerate(head_list):
            if pos == 'not_specified':
                head_list[i] = where_root_is
        root_is_specified = True
    elif 'X' in DEPREL:
        """
        기타표지

        인용부호와 괄호를 제외한 나머지 부호나, 조사, 어미가 단독으로 어절을 이룰 때
        그 구문표지 위치에 표시
        예: [ X_CMP]
        (X -/SS)

        대부분이 단일표지
        첫번째를 root로
        """
        where_root_is = 0
        head_list[where_root_is] = 0

        for i, pos in enumerate(head_list):
            if pos == 'not_specified':
                head_list[i] = where_root_is
        root_is_specified = True

    elif 'L' in DEPREL:
        """
        왼쪽 인용부호 (, ', "

        대부분이 단일표지
        첫번째를 root로
        """
        where_root_is = 0
        head_list[where_root_is] = 0

        for i, pos in enumerate(head_list):
            if pos == 'not_specified':
                head_list[i] = where_root_is
        root_is_specified = True

    elif 'R' in DEPREL:
        """
        오른쪽 인용부호 (, ', "

        대부분이 단일표지
        마지막을 root로
        """
        where_root_is = len(head_list)-1
        head_list[where_root_is] = 0

        for i, pos in enumerate(head_list):
            if pos == 'not_specified':
                head_list[i] = where_root_is
        root_is_specified = True

    elif 'S' == DEPREL:
        """
        문장
        마지막을 root로
        """
        where_root_is = len(head_list) - 1
        head_list[where_root_is] = 0

        for i, pos in enumerate(head_list):
            if pos == 'not_specified':
                head_list[i] = where_root_is
        root_is_specified = True



    if root_is_specified == False:
        print ('root is not specified')
        print (DEPREL)
        print (FORM_List)
        print (POS_List)
        print (head_list)
        raise SystemExit

    # print(head_list)
    # 파이썬 인덱싱은 0부터 시작인데 head list는 1부터 시작
    for i, value in enumerate(head_list):
        if i == where_root_is:
            pass
        else:
            head_list[i] += 1
            # print("head_list: ", head_list)

    return head_list


def find_head(eoj_head, id_list, eoj_inner_id_list, eoj_inner_head_list, num_lemma):
    """
    Input
    eoj_head = 0
    id_list = [11, 12, 13, 14, 15]
    eoj_inner_id_list = [1, 2, 3, 4, 5]
    eoj_inner_head_list = [2, 3, 4, 0, 4]
    num_lemma = 5


    Output
    head_list = [12, 13, 14, 0, 14]
    """
    head_list = ['_'] * num_lemma
    eoj_head = int(eoj_head)
    # print("eoj_head: ", eoj_head)

    for eoj_inner_id_counter, _ in enumerate(head_list):
        if eoj_head == 0:
            # 현재 어절이 Root 어절일 때

            if eoj_inner_head_list[eoj_inner_id_counter] == 0:
                #print(1)
                # 현재 어절이 Root 어절이고 현재 lemma가 Root 일 때
                head_list[eoj_inner_id_counter] = 0

            else:
                #print(2)
                # 현재 어절이 Root 어절이지만 현재 lemma가 Root는 아닐 때
                # 자신의 내부 Head가 가리키는 내부 ID를 가진 lemma 의 ID
                id_index = eoj_inner_head_list[eoj_inner_id_counter]
                ID_to_append = id_list[eoj_inner_id_list.index(id_index)]
                head_list[eoj_inner_id_counter] = ID_to_append
                # print(head)
        else:
            if eoj_inner_head_list[eoj_inner_id_counter] == 0:
                #print(3)
                # 현재 어절이 Root 어절이고 현재 lemma가 Root 일 때
                pass
            else:
                #print(4)
                # 현재 어절이 Root 어절이 아니고 현재 lemma가 Root가 아닐 때
                # 자신의 내부 Head가 가리키는 내부 ID를 가진 lemma 의 ID
                id_index = eoj_inner_head_list[eoj_inner_id_counter]
                ID_to_append = id_list[eoj_inner_id_list.index(id_index)]
                head_list[eoj_inner_id_counter] = ID_to_append

    return head_list