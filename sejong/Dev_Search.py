# -*- coding: utf-8 -*-
"""
Sejong_Corpus Converter
Jaemin Cho/j-min

- This file works well with dsindex's SyntaxNet fork! (https://github.com/dsindex/syntaxnet)
- Remove every line but raw sentences and parsed sentences
- Remove sentences with errors
  ex)  [Q="12]"
        (Q [/SS + Q="12/Q" + ]/SS)
- Raw files should be inside the same directory with this file.
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

sentence_counter = 0

dirname = "stripped"
if not os.path.isdir("./" + dirname + "/"):
    os.mkdir("./" + dirname + "/")

dirname = "converted"
if not os.path.isdir("./" + dirname + "/"):
    os.mkdir("./" + dirname + "/")

def allfiles(path):
    res = []

    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            res.append(filepath)

    return res

allfilelist = allfiles(os.getcwd()+'/raw_corpus')
sejonglist = [file for file in allfilelist if "BG" in file]
# print(sejonglist)
err_counter = 0



keyword = input("type keyword: ")
print(keyword)

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

                # place whitespaces before and after 'whitespace_chars'
                temp = line.replace('─', '-')
                for x in whitespace_chars:
                    temp = temp.replace(x, ' '+x+' ')
                # Remove multiple whitespaces
                temp = ' '.join(temp.split())

                if '앵, 앵, 앵' in line:
                    # exception
                    #writefile.write('; 앵, 앵, 앵 - . 애-앵-. 밖에서 요란한 소리가 울렸다. ')
                    pass
                else:
                    #writefile.write(temp)
                    pass

                #writefile.write('\n')
                sentence_counter += 1


            elif ("(" in line) and (")" in line[-3:]) and ("/" in line):
                try:
                    temp = re.match('(.*)(\([A-Z_]+ *\t*)+(.+[A-Z]+)([\)]+)', line).groups(3)
                    del(temp)
                    temp = line.replace('─', '-')
                    #writefile.write(temp)
                    first_line = False

                except:
                    #print(rawfile[-12:-4])
                    #print(line)
                    line_groups = re.match('(.*)(\([A-Z_]+ *\t*)+(.+[A-Z]+)[ \+]([\)]+)', line).groups()
                    temp = ''
                    for i, string in enumerate(line_groups):
                        temp += string
                    #writefile.write(print_string)
                    first_line = False
            elif ("<" in line) and not('(' in line) and not (';' in line):
                # 맨 위에 있는 태그들
                pass

            if keyword in line:
                err_counter += 1
                print('filename: ', rawfile[-12:-4])
                print('line_number: ', line_counter)
                print(temp.lstrip())
                print('num_error: ', err_counter)

            line_counter += 1

        #print(file_counter+1, OUT_FILENAME, "from", rawfile)
