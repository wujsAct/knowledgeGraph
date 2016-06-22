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
    t = {token.idx:i for i,token in enumerate(doc) }
    dep_triple = []
    for token in doc:
        temp = []
        temp.append([token.orth_,t[token.idx]])
        temp.append(nlp.vocab.strings[token.dep])
        temp.append([token.head.orth_,t[token.head.idx]])
        dep_triple.append(temp)
    return dep_triple


def pro_sen(line,stopwords):
    line = line.strip()
    lineNo,sentence,tags,tags_er = line.split('\t')
    rels = t.relation_pattern(tags,sentence)
    ents = t.is_entity(tags,tags_er,sentence,rels)
    #start = time.time()
    dep_triples = generateTriple(sentence)
    #end = time.time()
    #print end-start
    #print sentence
    dep_trip = []
    triples = ''
    #dep_triples =None
    if dep_triples !=None:
        #print 'go into getFinalTriple'
#        for i in list(dep_triples):
#            dep_trip.append(i)
        dep_trip = list(dep_triples)
        triples = genTripe.getFinalTriple(sentence,dep_trip,rels,ents)      
    else:
        triples = genTripe.getReverbTriple(sentence,rels,ents)
    strs = {}
    strs['1'] = lineNo
    strs['2'] = triples
    strs['3'] = sentence
    strs['4'] =tags
    strs['5'] = line
    strs['6'] =stopwords
    return strs
def toString(self):
        if len(self.ent1.getContent()) != 0 and len(self.rel.getContent()) != 0 and len(self.ent2.getContent()) != 0:
          #  return self.ent1.getContent() + '\t' + self.rel.getContent() + '\t' + self.ent2.getContent() + '\t' + str(self.score) + '\n'
            return self.ent1.getContent() + '\t' + self.rel.getContent() + '\t' + self.ent2.getContent() + '\n'
        else:
            return ''

#result_list = {}    
def completedCallback(data):
#    lineNo = data['1']
#    print lineNo
#    result_list.append(data)
    lineNo = data['1']
    if 'SP' == lineNo:
        print 'lineno',lineNo
    triples = data['2']
    sentence = data['3']
    tags = data['4']
    line =data['5']
    stopwords = data['6']
    #result_list=[]
    for key in triples:
        for key_multi in triples[key]:
            dep_tag = 0
            rel = key
            value = key_multi
            if len(value)==2:
                ent1 = value[0]
                ent2 = value[1]
            if len(value)==3:
                ent1 = value[0]
                ent2 = value[1]
                dep_tag = value[2]
            tri = TripleRecord(ent1, rel, ent2, sentence,tags)
            feature =  tri.getFeature(sentence)
            feature[0,18] = dep_tag
            #to score the triple, using the LR weights
            result = feature*triple_fea_LR_weight
            score = sum(result[0])
            #print score
            #stri = (tri.toString()).strip()
            relstr = rel.getContent()
            rel = ''
            for relitem in relstr.split(' '):
                if relitem not in stopwords:
                    rel = rel + relitem+' '
            rel = rel.strip()
            if len(rel)!=0 and score >0:
                print lineNo,'\t',ent1.getContent(),'\t',rel,'\t',ent2.getContent(),'\t',str(score),'\t',sentence
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
    genTripe = generateTriples()
    line_no =0
    f_stopwords = "data/stopwords.txt"
    stopwords= {}
    with codecs.open(f_stopwords,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            line = line.lower()
            stopwords[line] = 1
    pool = Pool(10)
#    extract_triple = codecs.open(dir_path+'extract_triple.txt','w','utf-8')
    try:
        with codecs.open(f_input,'r','utf-8') as file:
            for line in file:
#                data = pro_sen(line)
#                result_list = completedCallback(data)
                pool.apply_async(pro_sen,(line,stopwords,), callback = completedCallback)
            pool.close()
            pool.join()
#                if result_list!=None:
#                    for key in result_list:
#                        extract_triple.write(key+'\n')
#        extract_triple.close()
    except:
        print 'control-c presd butan'
        pool.terminate()
#    line = u'''0	The local government plans to open a visitor center in February that could eventually include a life - size hologram of the singer , whose real name is Park Jae - sang , performing his buf foonish dance .	DT JJ NN VBZ TO VB DT NN NN IN NNP WDT MD RB VB DT NN HYPH NN NN IN DT NN , WP$ JJ NN VBZ NNP NNP HYPH NNP , VBG PRP$ NN NN .	B-NP I-NP I-NP B-VP I-VP I-VP B-NP I-NP I-NP B-PP B-NP B-NP B-VP I-VP I-VP B-NP I-NP I-NP I-NP I-NP B-PP B-NP I-NP O B-NP I-NP I-NP B-VP B-NP I-NP I-NP I-NP O B-VP B-NP I-NP I-NP O '''
#    data = pro_sen(line)
#    completedCallback(data)      
