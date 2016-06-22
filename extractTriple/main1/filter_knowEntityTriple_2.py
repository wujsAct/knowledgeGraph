# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 16:21:20 2016

@author: DELL
"""

'''
In this function, we will filter the known triple(left argument or right argument can be
mappped into the knowledge).
'''
import numpy as np
import codecs
#import gensim
from  multiprocessing import Pool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from LeveDist import detectNovelEnt
#from numpy import linalg as LA
#
#def getVecDist(model,et,key):
#    flag1 =1
#    try:
#        et1 = et[0].lower()+et[1:-1]
#        et_vec1 = model[et1]
#    except:
#        try:
#            et2 = et1[0].upper()+et1[1:-1]
#            et_vec1 = model[et2]
#        except:
#            flag1 =0
#            
#    flag2=1
#    try:
#        et1 = key[0].lower()+key[1:-1]
#        et_vec1 = model[et1]
#    except:
#        try:
#            et2 = key[0].upper()+key[1:-1]
#            et_vec1 = model[et2]
#        except:
#            flag2 =0
#    
#    if flag1==1 and flag2==1:
#        vecDist = LA.norm(et_vec1-et_vec1)
#        return vecDist
#    else:
#        return float("inf")
#        
#def getLevDistance(model,dt,ent_name_map,ent):
#    for key in ent_name_map:
#        dist = dt.levenshtein(ent,key)
#        if dist <=0.1:
#            return 1,key
#    return 0,None
    
def pro_sen(dt,ent_name_map,line):
    line = line.strip()
    items= line.split(u'\t')
    flag  = 0
    if len(items)>=4:
        ent1 = items[0]
        ent2 = items[2]
        #ent1_items = ent1.split(' ')
#        for et in ent1_items:
#            tflag, entName = getLevDistance(dt,ent_name_map,et)
#            if tflag ==1:
#                flag = 1
#                line = line + '\t' + 'left '+entName
#                
#        ent2_items = ent2.split(' ')
#        for et in ent2_items:
#            tflag, entName = getLevDistance(dt,ent_name_map,et)
#            if tflag ==1:
#                flag = 1
#                line = line + '\t' + 'right '+entName
        #if getLevDistance(dt,ent_name_map,ent1) == 1 or getLevDistance(dt,ent_name_map,ent2) == 1: 
        temp_str = ''        
        if ent_name_map.get(ent1.lower()) !=None:
            flag = 1
            temp_str = '\t' + 'left '+ent1.lower()
        #�ڴ�ʱdelete��stop words
        else:
        
        if ent_name_map.get(ent2.lower())!=None:
            flag =1
            temp_str = temp_str + '\t' + 'right '+ent2.lower()
            
    if flag ==1:
        return line + temp_str
    else:
        return None

def completedCallback(data):
    if data!=None:
        sys.stdout.write(data+'\n')

f_entHasName = "../data/food/food_enthasName.txt"
f_ent2vec = "../data/food/food_ent2vec.txt"
#model = gensim.models.word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
f_ent2no = {}
ent_name_map = {}
ent_name_vec = np.loadtxt(f_ent2vec)
no = 0
with codecs.open(f_entHasName,'r','utf-8') as file:
    for line in file:
        line = line.strip()
        pid, name = line.split('\t')
        #此处做一些处理，把大写全部改成小写的�?        
        name = name.lower()
        ent_name_map[name] = pid
        f_ent2no[name] =no
        no = no + 1
f_stopword = '../main2/stopwords.txt'
stopwords_list = []
with codecs.open(f_stopword,'r','utf-8') as file:
    for line in file:
        line = line.strip()
        stopwords_list.append(line)
        
print len(ent_name_map)

dt = detectNovelEnt() 
f_triple = "../result.txt"
total = 0
#pool = Pool()
i = 0
relation = {}
with codecs.open(f_triple,'r','utf-8') as file:
    for line in file:
        #print i
        i = i + 1
        result = pro_sen(dt,ent_name_map,line)
        if result !=None:
            items = result.split('\t')
            rel = items[1]
            if relation.get(rel) == None:
                relation[rel]=1
            sys.stdout.write(result+'\n')
#        pool.apply_async(pro_sen,(dt,ent_name_map,line,), callback = completedCallback)
#    pool.close()
#    pool.join()
print '--------------------------'
for key in relation:
    sys.stdout.write(key+'\n')
print len(relation)
