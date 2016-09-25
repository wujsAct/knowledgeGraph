# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 19:46:56 2016

@author: DELL
"""
import sys
import time
import codecs
sys.path.append('utils')
sys.path.append('main1')
sys.path.append('main2')
from extractRelandEnt import InfoExtractClass
from generateTag import generateTag
from TripleRecord import TripleRecord
from generateTriple import generateTriples
import random
import numpy as np
from  multiprocessing import Pool
import hashlib
from spacy.en import English
import pickle
nlp = English()
import collections

#spacy is very fast than stanford CORENLP
def generateTriple(sentence):
    #print sentence
    doc = nlp(sentence)
    #print doc
    #generate the token.idx to token no
    t = {token.idx:i for i,token in enumerate(doc)}
    dep_triple = []
    for token in doc:
        temp = []
        temp.append([token.orth_,t[token.idx]])
        temp.append(nlp.vocab.strings[token.dep])
        temp.append([token.head.orth_,t[token.head.idx]])
        dep_triple.append(temp)
    return dep_triple

def crftag2id(crfTags):
    crftags = crfTags.split(u' ')
    tags={'B-NP':'1','I-NP':'2','B-VP':'3','I-VP':'4','B-ADVP':'5','I-ADVP':'6','B-PP':'7'}
    tag2id = []
    for tagi in crftags:
        if tagi in tags:
            tag2id.append(tags[tagi])
        else:
            tag2id.append('0')
    return u''.join(tag2id)
    

def pro_sen1(line):
    line = line.strip()
    lineNo,sentence,tags,tags_er = line.split(u'\t')
    if int(lineNo)%200==0:
        print lineNo
    tag =crftag2id(tags_er)
    
    rel_parameters=[tag,sentence,rel2num,strrels]
    rels = t.extractRelation(rel_parameters,'extract')
    
    ent_parameters =[tag,sentence,rels]
    ents = t.extractEntity(ent_parameters,'statistic')
    sentence = sentence.split(u' ')
    strents = []
    for ent in ents:
        start,end = ent.getIndexes()
        strent = u' '.join(sentence[start:end])
        strents.append(strent)
    return strents
 
if __name__=='__main__':
    #print 'data'
    
    if len(sys.argv) !=3:
        print 'usage: python pyfile dir_path input_name'
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+sys.argv[2]
    triple_fea_LR_weight =np.loadtxt('labels/triple_LRweight.txt')
        
    t = InfoExtractClass()
    genTag = generateTag()
    line_no =0
    ent2num= collections.defaultdict(int)
    tempresult={}
    rel2num = pickle.load(open(dir_path+'raw_rel2num.p','rb'))
    strrels = u'\n'.join(rel2num.keys())
    pool = Pool(30)
    try:
        with codecs.open(f_input,'r','utf-8') as file:
            for line in file:
                tempresult[pool.apply_async(pro_sen1, (line,))]=1
        print 'end!'
        pool.close()
        pool.join()
    except:
        print 'control-c presd butan'
        pool.terminate()
        pool.join()
    for key in tempresult:
        entlist = key.get()
        for ent in entlist:
            ent2num[ent]+=1
    pickle.dump(ent2num,open(dir_path+'raw_ent2num.p','wb'))
    
    #line =u'''2077	The event 's sponsors include the Chamber of Commerce ; FWD.us , a political action group founded by Mark Zuckerberg , the creator of Facebook ; the National Immigration Forum ; and the Partnership for a New American Economy , which is led by Mayor Michael R. Bloomberg of New York , Rupert Murdoch and Bill Marriott Jr.	DT NN NN NNS VBP DT NNP IN NNP : NNP , DT JJ NN NN VBN IN NNP NNP , DT NN IN NNP : DT NNP NNP NNP : CC DT NNP IN DT NNP NNP NNP , WDT VBZ VBN IN NNP NNP NNP NNP IN NNP NNP , NNP NNP CC NNP NNP NNP	B-NP I-NP I-NP I-NP B-VP B-NP I-NP B-PP B-NP O B-NP O B-NP I-NP I-NP I-NP B-VP B-PP B-NP I-NP O B-NP I-NP B-PP B-NP O B-NP I-NP I-NP I-NP O O B-NP I-NP B-PP B-NP I-NP I-NP I-NP O B-NP B-VP I-VP B-PP B-NP I-NP I-NP I-NP B-PP B-NP I-NP O B-NP I-NP O B-NP I-NP I-NP'''
    #line = u'''1	Popovich earlier admitted some feelings of awkwardness , having also served as a mentor to Avery Johnson .	NNP RBR VBD DT NNS IN NN , VBG RB VBD IN DT NN IN NNP NNP .	B-NP B-ADVP B-VP B-NP I-NP B-PP B-NP O B-VP B-ADVP B-VP B-PP B-NP I-NP B-PP B-NP I-NP O'''
    #data = pro_sen1(line,stopwords)
