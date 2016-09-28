# -*- coding: utf-8 -*-
"""
Sejong_Corpus Converter
Jaemin Cho/j-min

- This file works well with dsindex's SyntaxNet fork! (https://github.com/dsindex/syntaxnet)
- Remove every line but raw sentences and parsed sentences
- Remove sentences with errors
  ex)  [Q="12]"
        (Q [/SS + Q="12/Q" + ]/SS)
- Inputs: Raw Sejong Corpora files ex) BGHO0411.txt (UTF-16)

<!DOCTYPE tei.2 SYSTEM "c:\sgml\dtd\tei2.dtd" [
	<!ENTITY % TEI.corpus "INCLUDE">
	<!ENTITY % TEI.extensions.ent SYSTEM "sejong1.ent">
	<!ENTITY % TEI.extensions.dtd SYSTEM "sejong1.dtd">
]>

<tei.2>
<teiHeader>
	<fileDesc>
		<titleStmt>
			<title>하늘에 뜬 돌도끼, 형태소 분석 전자파일</title>
			<author>손동인</author>
			<sponsor>대한민국 문화관광부</sponsor>
			<respStmt>
				<resp>문헌입력, 표준화, 형태소 정보 부착</resp>
				<name>고려대학교 민족문화연구원</name>
			</respStmt>
		</titleStmt>
		<extent>22,790어절, 3,346문장</extent>
		<publicationStmt>
			<distributor>국립국어연구원</distributor>
			<idno>BGGO0098.txt, 형태분석: BTGO0098.txt, 원본:BRGO0098.txt</idno>
			<availability>배포 불가</availability>
		</publicationStmt>
		<notesStmt>
			<note>균형말뭉치에서 선정</note>
		</notesStmt>
		<sourceDesc>
			<bibl>
....

- Output: Unified Text file without irrelevant tags (UTF-8)
; 새 생명.
(NP 	(DP 새/MM)
	(NP 생명/NNG + ./SF))

; 나는 돈이다.
(S 	(NP_SBJ 나/NP + 는/JX)
	(VNP 돈/NNG + 이/VCP + 다/EF + ./SF))

; 만 원이라는 이름을 붙인 채, 이제 막 태어났다.
(VP 	(NP_AJT 	(VP_MOD 	(NP_OBJ 	(VNP_MOD 	(NP 만/NR)
					(VNP_MOD 원/NNB + 이/VCP + 라는/ETM))
				(NP_OBJ 이름/NNG + 을/JKO))
			(VP_MOD 붙이/VV + ᆫ/ETM))
		(NP_AJT 채/NNB + ,/SP))
	(VP 	(AP 이제/MAG)
		(VP 	(AP 막/MAG)
			(VP 태어나/VV + 았/EP + 다/EF + ./SF))))

; 스슥, 슥-. 이게 마지막 과정이었다.
(S 	(AP 	(AP 	(AP 	(AP 스슥/MAG + ,/SP)
				(AP 슥/MAG))
			(X -/SS))
		(X ./SF))
	(S 	(NP_SBJ 이것/NP + 이/JKS)
		(VNP 	(NP 마지막/NNG)
			(VNP 과정/NNG + 이/VCP + 었/EP + 다/EF + ./SF))))
....
"""

import codecs
import os
import re
import shutil

try:
    os.remove("sejong_treebank.txt.v1")
except:
    print ('No such file to remove!')
    pass

sentence_counter = 0

dirname = "stripped"
if not os.path.isdir("./raw_corpus/" + dirname + "/"):
    os.mkdir("./raw_corpus/" + dirname + "/")

dirname = "converted"
if not os.path.isdir("./raw_corpus/" + dirname + "/"):
    os.mkdir("./raw_corpus/" + dirname + "/")

def allfiles(path):
    res = []

    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            res.append(filepath)

    return res

allfilelist = allfiles(os.getcwd() + '/raw_corpus')
sejonglist = [file for file in allfilelist if "BG" in file]
# print(sejonglist)

for file_counter, rawfile in enumerate(sejonglist):

    with codecs.open(rawfile, "r", encoding = "utf-16-le") as readfile:
        OUT_FILENAME = os.getcwd()+"/raw_corpus/stripped/"+rawfile[-12:-4]+"_stripped.txt"
        first_line = True
        whitespace_chars = ['(', ')', '<', '>', '{', '}', '[', ']', '-', '─', '·', '/', '~']

        with codecs.open(OUT_FILENAME, "w", "utf-8") as writefile:
            for line in readfile:
                if "; " == line[0:2]:
                    if first_line == False:
                        writefile.write("\n")

                    # place whitespaces before and after 'whitespace_chars'
                    temp = line.replace('─', '-')
                    temp = line.replace('―', '-')
                    temp = line.replace("`", "'")
                    for x in whitespace_chars:
                        temp = temp.replace(x, ' '+x+' ')
                    # Remove multiple whitespaces
                    temp = ' '.join(temp.split())
                    # temp = temp.replace('는지', '는 지')
                    temp = temp.replace('하는데', '하는 데')
                    temp = temp.replace('한데', '한 데')
                    temp = temp.replace('온후', '온 후')

                    if '앵, 앵, 앵' in line:
                        # exception
                        writefile.write('; 앵, 앵, 앵 - . 애-앵-. 밖에서 요란한 소리가 울렸다. ')
                    else:
                        writefile.write(temp)
                    writefile.write('\n')
                    sentence_counter += 1


                elif ("(" in line) and (")" in line[-3:]) and ("/" in line):
                    try:
                        temp = re.match('(.*)(\([A-Z_]+ *\t*)+(.+[A-Z]+)([\)]+)', line).groups(3)
                        del(temp)

                        #temp = temp.replace('NP + 데/NN', 'NP 데/NN')
                        #temp = temp.replace('NP_AJT + 데/NN', 'NP_AJT 데/NN')
                        #temp = temp.replace('NP_AJT + 대로/NN', 'NP_AJT 대로/NN')
                        #temp = temp.replace('(X + ∼/SO', '(X ∼/SO')
                        #temp = temp.replace('(X + -/SS', '(X -/SS')
                        temp = line

                    except:
                        #print(rawfile[-12:-4])
                        #print(line)
                        line_groups = re.match('(.*)(\([A-Z_]+ *\t*)+(.+[A-Z]+)[ \+]([\)]+)', line).groups()
                        temp = line_groups[2].rstrip()

                        # (VP + 내 / VV + 아 / EC)) 같이 처음에 + 나오는  오류 제거
                        if '+ ' in line_groups[2][:3]:
                            temp = temp[2:]
                        temp = line_groups[0]+line_groups[1]+temp+line_groups[3]
                        #print(temp)


                    temp = temp.replace('─', '-')
                    temp = temp.replace('―', '-')
                    temp = temp.replace("`", "'")
                    writefile.write(temp)
                    first_line = False
                elif ("<" in line) and not('(' in line) and not (';' in line):
                    # 맨 위에 있는 태그들
                    pass

        print(file_counter+1, OUT_FILENAME, "from", rawfile)

stripped_sejonglist = allfiles(os.getcwd()+"/raw_corpus/stripped")
# stripped_sejonglist = [file for file in strippedfilelist if "stripped" in file]
print(stripped_sejonglist)

errors = 0
error_string = ["Q1", "Q2", "Q3", 'Q4', 'Q5', 'Q6', 'Q=', '(Q', '; Q', '/Q', '/U', '/W', '/Y', '/Z', '(L', '(R']

for file_counter, strippedfile in enumerate(stripped_sejonglist):
    with codecs.open(strippedfile, 'r') as readfile:
        OUT_FILENAME = os.getcwd()+"/raw_corpus/converted/"+strippedfile[-21:-13]+"_converted.txt"
        error_sentence = False
        buffer = ""

        with codecs.open(OUT_FILENAME, "w") as writefile:
            error_counter = 0
            line_counter = 1

            for line in readfile:
                for x in error_string:
                    if x in line:
                        error_sentence = True
                        buffer = ""
                        # print(line_counter, line)

                if "\n" == line:
                    if error_sentence == False:
                        writefile.write(buffer)
                    else:
                        error_counter +=1
                    buffer = ""
                    error_sentence = False

                if error_sentence == False:
                    buffer += line

                line_counter += 1

        print(file_counter+1, OUT_FILENAME, "from", strippedfile, "| error counts: ", error_counter)
    errors += error_counter

converted_sejonglist = allfiles(os.getcwd()+"/raw_corpus/converted")
print(converted_sejonglist)

for file_counter, convertedfile in enumerate(converted_sejonglist):
    print(file_counter+1, convertedfile)

    with codecs.open(convertedfile, 'r', encoding = 'utf-8') as readfile:
        OUT_FILENAME = "sejong_treebank.txt.v1"
        with codecs.open(OUT_FILENAME, "a", "utf-8") as writefile:
            data = readfile.read()
            writefile.write(data)


for temp_directory in ["stripped","converted"]:
    try:
        shutil.rmtree(os.getcwd()+'/raw_corpus/'+temp_directory)
    except OSError as e:
        if e.errno == 2:
            # 파일이나 디렉토리가 없음!
            print ('No such file or directory to remove')
            pass
try:
    shutil.rmtree(os.getcwd()+'/wdir')
except OSError as e:
    if e.errno == 2:
        # 파일이나 디렉토리가 없음!
        print ('No such file or directory to remove')
        pass

print("Converting Sejong Corpus Complete!")
print("Raw corpus 총 문장: ", sentence_counter)
print("# of error sentences: ", errors)
print("남은 총 문장: ", sentence_counter - errors)
