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
nlp = English()

#spacy is very fast than stanford CORENLP
def generateTriple(sentence):
    doc = nlp(sentence)
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


def pro_sen1(line,stopwords):
    line = line.strip()
    lineNo,sentence,tags,tags_er = line.split('\t')
    rels = t.relation_pattern(tags,sentence)
    ents = t.is_entity(tags,tags_er,sentence,rels)
    #start = time.time()
    genTripe.getEntRelationEnt(sentence,rels,ents,lineNo,tags,stopwords)
if __name__=='__main__':
    #print 'data'
    if len(sys.argv) !=3:
        print 'usage: python pyfile dir_path input_name'
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+sys.argv[2]
    triple_fea_LR_weight =np.loadtxt('labels/triple_LRweight.txt')
    #stop words lists
    f_stopwords = "data/stopwords.txt"
    stopwords= {}
    with codecs.open(f_stopwords,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            line = line.lower()
            stopwords[line] = 1
    t = InfoExtractClass()
    genTag = generateTag()
    genTripe = generateTriples()
    line_no =0
    pool = Pool(1)
    try:
        with open(f_input,'r') as file:
            for line in file:
                pool.apply_async(pro_sen1,(line,stopwords,))
            pool.close()
            pool.join()
    except:
        print 'control-c presd butan'
        pool.terminate()
#    with codecs.open(f_input,'r','utf-8') as file:
#        for line in file:
#            data = pro_sen1(line,stopwords)
