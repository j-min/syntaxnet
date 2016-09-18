#-*- coding: utf8 -*-
from c2d import *
import os
from optparse import OptionParser

print(tokenize(["; 프랑스의 세계적인 의상 디자이너 엠마누엘 웅가로가 실내 장식용 직물 디자이너로 나섰다.",
                "(S 	(NP_SBJ (NP	    (NP_MOD 프랑스/NNP + 의/JKG)",
                "                       (NP	    (VNP_MOD 세계/NNG + 적/XSN + 이/VCP + ᆫ/ETM)",
                "                               (NP	    (NP 의상/NNG)",
                "                                       (NP 디자이너/NNG))))",
                "               (NP_SBJ (NP 엠마누엘/NNP)",
                "                       (NP_SBJ 웅가로/NNP + 가/JKS)))",
                "       (VP	    (NP_AJT	(NP	    (NP	    (NP 실내/NNG)",
                "                                       (NP 장식/NNG + 용/XSN))",
                "                               (NP 직물/NNG))",
                "                       (NP_AJT 디자이너/NNG + 로/JKB))",
                "               (VP 나서/VV + 었/EP + 다/EF + ./SF)))"]))

bucket = ["; 프랑스의 세계적인 의상 디자이너 엠마누엘 웅가로가 실내 장식용 직물 디자이너로 나섰다.",
                "(S 	(NP_SBJ (NP	    (NP_MOD 프랑스/NNP + 의/JKG)",
                "                       (NP	    (VNP_MOD 세계/NNG + 적/XSN + 이/VCP + ᆫ/ETM)",
                "                               (NP	    (NP 의상/NNG)",
                "                                       (NP 디자이너/NNG))))",
                "               (NP_SBJ (NP 엠마누엘/NNP)",
                "                       (NP_SBJ 웅가로/NNP + 가/JKS)))",
                "       (VP	    (NP_AJT	(NP	    (NP	    (NP 실내/NNG)",
                "                                       (NP 장식/NNG + 용/XSN))",
                "                               (NP 직물/NNG))",
                "                       (NP_AJT 디자이너/NNG + 로/JKB))",
                "               (VP 나서/VV + 었/EP + 다/EF + ./SF)))"]

