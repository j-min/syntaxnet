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
			<title>하늘여 돌도끼, 형태소 분석 전�민국 문화관광부</sponsor>
			<respStmt>
				<resp>문헌입력, 표준화, 형태소 정보 부착</resp>
				<name>고려대학교 민족문화연구원</name>
			</respStmt>
		</titleStmt>
		<extent>22,790어절, 3,346문장</extent>
		<publicationStmt>
			<distributor>국립국어연구�분석: BTGO0098.txt, 원본:BRGO0098.txt</idno>
			<availability>배포 불가</availability>
		</publicationStmt>
		<notesStmt>
			<note>균형� 선정</note>
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

; 만 � 막 태어났다.
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

allfilelist = allfiles(os.getcwd())
sejonglist = [file for file in allfilelist if "BG" in file]
# print(sejonglist)

for file_counter, rawfile in enumerate(sejonglist):

    with codecs.open(rawfile, "r", encoding = "utf-16") as readfile:
        OUT_FILENAME = os.getcwd()+"/stripped/"+rawfile[-12:-4]+"_stripped.txt"
        first_line = True

        with codecs.open(OUT_FILENAME, "w", "utf-8") as writefile:
            for line in readfile:
                if "<" in line:
                    pass
                elif "; " in line:
                    if first_line == False:
                        writefile.write("\n")
                    writefile.write(line)
                elif ("("in line) and (")"in line) and ("/"in line):
                    writefile.write(line)
                    first_line = False

        print(file_counter+1, OUT_FILENAME, "from", rawfile)

stripped_sejonglist = allfiles(os.getcwd()+"/stripped")
# stripped_sejonglist = [file for file in strippedfilelist if "stripped" in file]
print(stripped_sejonglist)

error_string = ["Q1", "Q2", "Q3", 'Q4', 'Q5', 'Q6', 'Q=', '(Q', '; Q', '/Q', '/U', '/W', '/Y', '/Z']

for file_counter, strippedfile in enumerate(stripped_sejonglist):
    with codecs.open(strippedfile, 'r') as readfile:
        OUT_FILENAME = os.getcwd()+"/converted/"+strippedfile[-21:-13]+"_converted.txt"
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

converted_sejonglist = allfiles(os.getcwd()+"/converted")
print(converted_sejonglist)

for file_counter, convertedfile in enumerate(converted_sejonglist):
    print(file_counter+1, convertedfile)

    with codecs.open(convertedfile, 'r', encoding = 'utf-8') as readfile:
        OUT_FILENAME = "../sejong_treebank.txt.v1"
        with codecs.open(OUT_FILENAME, "a", "utf-8") as writefile:
            data = readfile.read()
            writefile.write(data)

import shutil

for temp_directory in ["/stripped","/converted"]:
    try:
        shutil.rmtree(os.getcwd()+temp_directory)
    except OSError as e:
        if e.errno == 2:
            # 파일이나 디렉토리가 없음!
            print ('No such file or directory to remove')
            pass
        else:
            raise

print("Converting Sejong Corpus Complete!")
