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


#spacy is very fast than stanford CORENLP
def generateDT(doc):
    #print doc.text
    t = {token.idx:i for i,token in enumerate(doc)}
    dep_triple = []
    for token in doc:
        temp = []
        temp.append([token.orth_,t[token.idx]])
        temp.append(nlp.vocab.strings[token.dep])
        temp.append([token.head.orth_,t[token.head.idx]])
        dep_triple.append(temp)
    return dep_triple

    
if __name__=='__main__':
    #print 'data'
    
    if len(sys.argv) !=3:
        print 'usage: python pyfile dir_path input_name outputname'
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+sys.argv[2]
   
    nlp= English()
    texts = []
    stime = time.time()
    with codecs.open(f_input,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            lineNo,sentence,tags,tags_er = line.split('\t')
            texts.append(lineNo+sentence)
    etime = time.time()
    print 'load tests time:',etime - stime       
             
    pool = Pool(30)
    try:
        DT_result = [generateDT(doc) for doc in nlp.pipe(texts, n_threads=30, batch_size=100)]
    except:
        print 'read file exception'
    pickle.dump(DT_result,open(dir_path+'DT_result.p','wb'))