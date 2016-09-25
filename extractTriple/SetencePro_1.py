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
import cPickle
import pickle
import collections


def crftag2id(crfTags):
    crftags = crfTags.split(u' ')
    tags={'B-NP':'1','I-NP':'2','B-VP':'3','I-VP':'4','B-ADVP':'5','I-ADVP':'6','B-PP':'7'}
    tag2id = []
    for tagi in crftags:
        if tagi in tags:
            tag2id.append(tags[tagi])
        else:
            tag2id.append('0')
    return ''.join(tag2id)

def pro_sen1(dep_triple,line):
    #print texti
#    dep_triple = texti[0]
#    line = texti[1]
    #print line
    lineNo,sentence,tags,tags_er = line.split(u'\t')
    #print line
    sentence = sentence.strip()
    tag =crftag2id(tags_er)
    
    rel_parameters=[tag,sentence,rel2num,strrels]
    rels = infoextractclass.extractRelation(rel_parameters,'extract')
    #print rels
    ent_parameters =[tag,sentence,rels,ent2num,strents]
    ents = infoextractclass.extractEntity(ent_parameters,'extract')
    
#    for i in ents:
#        s,e = i.getIndexes()
#        print 'ent ',i,'\t',' '.join(sentence.split(u' ')[s:e])
#        
#    for i in rels:
#        s,e = i.getIndexes()
#        print 'rel ',i,'\t',' '.join(sentence.split(u' ')[s:e])
        
    #print ents
    triples ='None'
    if rels is not None and ents is not None:
        triples = genTriple.getFinalTriple(lineNo,sentence,dep_triple,rels,ents,tags)
    #print triples
    return triples
        
    
    
if __name__=='__main__':
    #print 'data'
    
    if len(sys.argv) !=4:
        print 'usage: python pyfile dir_path input_name outputname'
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+sys.argv[2]
    f_output = dir_path + sys.argv[3]

    #stop words lists
    f_stopwords = "data/stopwords.txt"
    stopwords= {}
    with codecs.open(f_stopwords,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            line = line.lower()
            stopwords[line] = 1
    stime = time.time()
    print 'start to load rel and ents!'
    rel2num = cPickle.load(open(dir_path+'raw_rel2num.p','rb')) 
    etime1 = time.time()
    print 'load rels',etime1 -stime
    ent2num = cPickle.load(open(dir_path+'raw_ent2num.p','rb')) 
    etime2 = time.time()
    print 'load ents',etime2 -etime1
    print 'finish load rel and ents'
    infoextractclass = InfoExtractClass()
    genTag = generateTag()
    genTriple = generateTriples()
    strents = u'\t'.join(ent2num.keys())
    strrels = u'\t'.join(rel2num.keys())
    fout = codecs.open(f_output,'w','utf-8')
    DTResult = cPickle.load(open(dir_path+'DT_result.p','rb'))
    etime3 = time.time()
    print 'load triples',etime3 - etime2
    print 'finish load datas!!'
    texts = []
    lineno = 0
    with codecs.open(f_input,'r','utf-8') as file:
        for line in file:
            line = line.strip()    
            texts.append([DTResult[lineno],line])
            lineno+=1
    print 'generate texts finished....'  
    
    strategydict={u'depenE_conj':1,u'depenR_conj':2,u'nsubj':3,u'dobj':4,u'nearArguments':5,u'advcl':6}
    
    strategy_dict = collections.defaultdict(int)
    strategyMix_dict = collections.defaultdict(int)
    tempresult=[]
    pool = Pool(30)
    try:
        tempresult = [pool.apply_async(pro_sen1, (texti)).get() for texti in texts]
        pool.close()
        pool.join()
    except:
        print 'control-c presd butan'
        pool.terminate()
        pool.join()
    print 'finished!'
    for result_apply in tempresult:
        #print result_apply
        triples = result_apply
        if triples!='None':
            for ret in triples:
                #print 'wrong with triples'
                #print 'ret:',ret
                strategies = triples[ret]
                #print strategies
                #print 'wrong with strategies'
                for istra in strategies:
#                    print 'istra',istra
                    strategy_dict[istra] +=1
                    ino=strategydict[istra]
                    for jstra in strategies:
                        jno=strategydict[jstra]
                        if ino != jno and ino < jno:
                            strategyMix_dict[str(ino)+'_'+str(jno)] +=1
                        if ino != jno and ino > jno:
                            strategyMix_dict[str(jno)+'_'+str(ino)] +=1
                #print 'finishes'
                fout.write(ret+u'\n')
    fout.close()
    
    pickle.dump(strategy_dict,open(dir_path+'strategy_dict.p','wb'))
    pickle.dump(strategyMix_dict,open(dir_path+'strategyMix_dict.p','wb'))
    
#    lineNo = 0
#    try:
#        with codecs.open(f_input,'r','utf-8') as file:
#            for line in file:
#                lineNo += 1
#                if lineNo %1000==0:
#                    print lineNo
#                triples = pro_sen1(line)
#                for ret in triples:
#                    fout.write(ret+'\n')
#    except:
#        fout.close()
#    fout.close()
    #72037
    #line =u'''2077	The event 's sponsors include the Chamber of Commerce ; FWD.us , a political action group founded by Mark Zuckerberg , the creator of Facebook ; the National Immigration Forum ; and the Partnership for a New American Economy , which is led by Mayor Michael R. Bloomberg of New York , Rupert Murdoch and Bill Marriott Jr.	DT NN NN NNS VBP DT NNP IN NNP : NNP , DT JJ NN NN VBN IN NNP NNP , DT NN IN NNP : DT NNP NNP NNP : CC DT NNP IN DT NNP NNP NNP , WDT VBZ VBN IN NNP NNP NNP NNP IN NNP NNP , NNP NNP CC NNP NNP NNP	B-NP I-NP I-NP I-NP B-VP B-NP I-NP B-PP B-NP O B-NP O B-NP I-NP I-NP I-NP B-VP B-PP B-NP I-NP O B-NP I-NP B-PP B-NP O B-NP I-NP I-NP I-NP O O B-NP I-NP B-PP B-NP I-NP I-NP I-NP O B-NP B-VP I-VP B-PP B-NP I-NP I-NP I-NP B-PP B-NP I-NP O B-NP I-NP O B-NP I-NP I-NP'''
    #data = pro_sen1(DTResult[72037],line)
    #for tt in data:
    #    print tt
#    line =u'''25	carpe diem " ) . 	JJ NN -RRB- -RRB- . 	B-NP I-NP I-NP I-NP O'''
#    data = pro_sen1(DTResult[999],line)
#    for tt in data:
#        print tt
#    line = u'''1	Williams was the only Net to score in the third quarter , on a jumper , a layup and a free throw , going 2 for 6 from the field while his teammates were 0 for 14 . 	NNP VBD DT JJ JJ TO VB IN DT JJ NN , IN DT NN , DT NN CC DT JJ NN , VBG CD IN CD IN DT NN IN PRP$ NNS VBD CD IN CD . 	B-NP B-VP B-NP I-NP I-NP B-VP I-VP B-PP B-NP I-NP I-NP O B-PP B-NP I-NP O B-NP I-NP O B-NP I-NP I-NP O B-VP B-NP B-PP B-NP B-PP B-NP I-NP B-SBAR B-NP I-NP B-VP B-NP B-PP B-NP O '''
#    data = pro_sen1(DTResult[57],line)
#    for tt in data:
#        print tt
    #line = u'''1	Popovich earlier admitted some feelings of awkwardness , having also served as a mentor to Avery Johnson .	NNP RBR VBD DT NNS IN NN , VBG RB VBD IN DT NN IN NNP NNP .	B-NP B-ADVP B-VP B-NP I-NP B-PP B-NP O B-VP B-ADVP B-VP B-PP B-NP I-NP B-PP B-NP I-NP O'''
    #data = pro_sen1(line,stopwords,rel2num,ent2num)
    #line = u'''1	The Nets have not won a game in San Antonio since January 2002 , a span of 11 games , dating to the season before Carlesimo became a Spurs assistant . 	DT NNPS VBP RB VBN DT NN IN NNP NNP IN NNP CD , DT NN IN CD NNS , VBG IN DT NN IN NNP VBD DT NNP NN . 	B-NP I-NP B-VP I-VP I-VP B-NP I-NP B-PP B-NP I-NP B-PP B-NP I-NP O B-NP I-NP B-PP B-NP I-NP O B-VP B-PP B-NP I-NP B-PP B-NP B-VP B-NP I-NP I-NP O '''
    #data = pro_sen1(line,stopwords,rel2num,ent2num)