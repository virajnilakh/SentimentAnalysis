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
'''print "relearning"
#relearning
with open('./test.dat', 'r') as fh:
    lines = fh.readlines()

test=[""]
ind=0
for l in lines:
    test[ind]=test[ind]+l
    if "\n" in l:
        ind+=1
        test.append("")
test=test[:-1]
with open('./ans26.dat', 'r') as fh:
    lines = fh.readlines()
rind=0
for l in test:
    if lines[rind]=="+1\n":
        pos.append(l)
    else:
        neg.append(l)
    rind+=1'''
pindex=0
nindex=0
#pos=pos[:50]
#neg=neg[:50]
print "creating document of words"
#creates documents of words
for l in pos:
    pos[pindex]=getWords(l)
    pindex+=1
for l in neg:
    neg[nindex]=getWords(l)
    nindex+=1
print "indexing"
#indexing
index={}
c=0
for l in pos+neg:
    for w in l:
        w = w.lower()
        #w = stem(w)
        if w in stop_words:
            continue
        if w not in index:
            index[w]=c
            c+=1
'''pos_str=""
neg_str=''
for l in pos:
    for w in l:
        pos_str+=(w+" ")
for l in neg:
    for w in l:
        neg_str+=(w+" ")
'''
print "word-freq format"
print "pos word freq"
#converts document in word-freq format
pos_dict=[]
for d in pos:
    p={}
    pd={}
    for w in d:

        w = w.lower()
        #w=stem(w)
        if w in stop_words:
            continue
        if index[w] not in p:
            pd[w]=1
            p[index[w]] = 1
        else:
            pd[w]+=1
            p[index[w]] += 1
    pos_dict.append(p)
    #print pd

neg_dict=[]
for d in neg:
    n={}
    nd={}
    for w in d:
        w = w.lower()
        #w = stem(w)
        if w in stop_words:
            continue
        if index[w] not in n:
            n[index[w]] = 1
            nd[w]=1
        else:
            n[index[w]] += 1
            nd[w]+=1
    neg_dict.append(n)
    #print nd
print "normalizing"
for l in pos_dict+neg_dict:
    l=normalize(l)


'''print "tf-idf"
#tfidf
for w in index:
    c1=0
    c2=0
    for l in pos_dict:
        if index[w] in l:
            c1+=1
    for l in neg_dict:
        if index[w] in l:
            c2+=1
    for l in pos_dict:
        if index[w] in l:
            l[index[w]]*=len(neg_dict)/c1
    for l in neg_dict:
        if index[w] in l:
            l[index[w]]*=len(pos_dict)/c2'''
print "contructinng feature matrix"
#contructinng feature matrix
index = sorted(index.items(), key=operator.itemgetter(1))
print "sorting done"
feature=[]
for v in index:
    f={}
    for j in range(len(pos_dict)):
        if v[1] in pos_dict[j]:
            f[j]=pos_dict[j][v[1]]
    for j in range(len(neg_dict)):
        if v[1] in neg_dict[j]:
            f[-j]=neg_dict[j][v[1]]
    feature.append(f)
other={}
for v in index:
    other[v[0]]=v[1]
index=other

print "test input"
#test
with open('./test.dat', 'r') as fh:
    lines = fh.readlines()

test=[""]
ind=0
for l in lines:
    test[ind]=test[ind]+l
    if "\n" in l:
        ind+=1
        test.append("")
test=test[:-1]

ind=0
ans_a=[]
f = open("ans25.dat", "w+")
for t in test:
    ans=0
    pos_ans = {}
    neg_ans = {}
    pindex = 0
    nindex = 0
    test_dict = {}
    t=getWords(t)
    for w in t:
        w = w.lower()
        #w = stem(w)
        if w in stop_words:
            continue
        if w not in test_dict:
            test_dict[w] = 1
        else:
            test_dict[w] = test_dict[w] + 1


    test_dict=normalize(test_dict)
    for k,v in test_dict.iteritems():
        if k in index:
            for j,u in feature[index[k]].iteritems():
                if j>0:
                    if j in pos_ans:
                        pos_ans[j]+=v*u
                    else:
                        pos_ans[j]=0
                else:
                    if j in neg_ans:
                        neg_ans[j]+=v*u
                    else:
                        neg_ans[j]=0
    pos_ans = sorted(pos_ans.items(), key=operator.itemgetter(1))
    pos_ans = pos_ans[-25:]
    neg_ans = sorted(neg_ans.items(), key=operator.itemgetter(1))
    neg_ans = neg_ans[-25:]
    for v in pos_ans:
        ans += v[1]
    for v in neg_ans:
        ans -= v[1]
    if ans >= 0:
        ans_a.append("+1")
        f.write("+1\n")
    else:
        ans_a.append("-1")
        f.write("-1\n")

    '''for p in pos_dict:
        pos_ans.append(0)
        for k,v in test_dict.iteritems():
            #print k,v
            if k not in index:
                continue
            if index[k] in p:
                pos_ans[pindex]+=p[index[k]]*v
        pindex+=1
    for n in neg_dict:
        neg_ans.append(0)
        for k,v in test_dict.iteritems():
            if k not in index:
                continue
            if index[k] in n:
                neg_ans[nindex]+=n[index[k]]*v
        nindex+=1
    pos_ans.sort(reverse=True)
    neg_ans.sort(reverse=True)
    for v in pos_ans[:10]:
        ans+=v
    for v in neg_ans[:10]:
        ans-=v
    if v>0:
        ans_a.append("+1")
        f.write("+1\n")
    else:
        ans_a.append("-1")
        f.write("-1\n")'''

