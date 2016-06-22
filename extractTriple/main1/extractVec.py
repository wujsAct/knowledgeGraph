# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 09:58:54 2016

@author: DELL
"""

'''
@function: to get all the kg's entity vector
'''
import codecs
import gensim
import numpy as np
import string

model = gensim.models.word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
def deleteSymbol(word):
    #t = string.punctuation
    #t.replace('\'',' ')
    t = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    remove_punctuation_map = dict((ord(char), None) for char in t)
    word = ''.join([s.translate(remove_punctuation_map) for s in word])
    word.replace(u'\'s','')
    return word
    
def getVector(entity):
    #组成entity的words都是用空格分隔的呢！
    words = entity.split()
    vec = np.zeros((300,),dtype='float32')
    #此处假设大多数实体的name都可以在Google News中出现了的哈！
    #此处捕获一个异常，如果有词没在Google News中出现！
    flag = 0
    for word in words:
        try:
            word = deleteSymbol(word)
            temp = model[word]
            vec = vec + temp
            flag = 1
        except:
	    print word,' is error key!!'
    return flag,vec
dir_path = 'food/'
file_ent2name=dir_path+'food_ent2name.txt'
file_ent2id=dir_path+'food_enthasName.txt'
file_ent2vec=dir_path+'food_ent2vec.txt'
f1 = codecs.open(file_ent2name,'r','utf-8')
f2 = codecs.open(file_ent2id,'w','utf-8')
f3 = open(file_ent2vec,'w')
for line in f1.readlines():
    line = line.strip()
    items = line.split('\t')
    entid = items[0]
    entName = items[1]
    if entName !=u'None':
        flag,vec = getVector(entName)
        if flag !=0:
            f2.write(entid+u'\t'+entName+u'\n')
            for i in range(300):
                f3.write(vec[i]+'\t')
            f3.write('\n')
f2.close()
f3.close()                
