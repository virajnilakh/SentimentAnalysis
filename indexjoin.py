import re
import math
import operator

from autocorrect import spell
from stemming.porter2 import stem
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def getWords(text):
    return re.compile('\w+').findall(text)
def normalize(d):
    norm = 0
    for k, v in d.iteritems():
        norm = norm + v ** 2
    norm = math.sqrt(norm)
    for k, v in d.iteritems():
        d[k] = d[k] / norm
    return d
with open('./train.dat', 'r') as fh:
    lines = fh.readlines()
pos = []
neg = []
pindex = -1
nindex = -1
flag = 1
for l in lines:
    if (l[0:2] != "-1"):
        if (l[0:2] == "+1" or flag):
            pos.append("")
            pindex += 1
            if (l[0:2] == "+1"):
                pos[pindex] = l[2:]
            else:
                pos[pindex] = pos[pindex] + l
            flag = 1
        else:

            neg[nindex] = neg[nindex] + l
            flag = 0
    else:
        if (l[0:2] == "-1"):
            neg.append("")
            nindex += 1
            neg[nindex] = l[2:]
        flag = 0
