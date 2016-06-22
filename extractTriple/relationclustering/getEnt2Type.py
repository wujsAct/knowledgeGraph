# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 19:54:57 2016

@author: DELL
"""

import codecs
import numpy as np
from sklearn.neighbors import NearestNeighbors
import gensim,logging
"""
@use file: ../data/food/extract_ent_has_type.txt
@function: we first extract all the known entity type, 
           then split the data into train and test subset
"""
#tag_doc='_entRent'
tag_doc=''
def getRelNeighbors(dir_path,num_neighbors):
    X = np.loadtxt(dir_path+'latent_relation.txt')
    nbrs = NearestNeighbors(n_neighbors=num_neighbors, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    return indices
    
def getAllKnownTypeEnt(dir_path):
    f1 = codecs.open(dir_path+'extract_ent_has_type'+tag_doc+'.txt','r','utf-8')
    
    f2 = codecs.open(dir_path+'typePropagation/entity2id.txt','w','utf-8')
    f3 = codecs.open(dir_path+'typePropagation/entityid2typeid.txt','w','utf-8')
    entid = 1
    ent2id_dict={}
    id2ent_dict={}
    for line in f1.readlines():
        line = line.strip()
        
        items = line.split('\t')
        
        entName = items[0]
        type1 = items[1]
        
        if type1!='NIL':
            if ent2id_dict.get(entName)==None:
                ent2id_dict[entName] = entid
                id2ent_dict[entid] = entName
                entid = entid + 1
            entNo = ent2id_dict.get(entName)
            for itr in items[1:]:
                itr = int(itr)+1
                f3.write(str(entNo)+'\t'+str(itr)+'\n')
    f3.close()
    for key in id2ent_dict:
        f2.write(id2ent_dict[key]+'\t'+str(key)+'\n')
    f2.close()

def getitem2id(fileName):
    f1 = codecs.open(fileName,'r','utf-8')
    
    item2id ={}
    for line in f1.readlines():
        line = line.strip()
        
        items = line.split('\t')
        itemName = items[0]
        ids = int(items[1])
        
        item2id[itemName] = ids
    
    return item2id
        

'''
@use file: '../data/food/rel2id', '../data/food/rel2cluster.txt'
@function: merge to get mapping: relation_name clusterid
'''
def getRel2id(dir_path):
    fileName1 = dir_path +'rel2clusterid_r500_max_0.txt'
    cluster_info = np.loadtxt(fileName1)
    
    f1 = codecs.open(dir_path+'rel2id.txt','r','utf-8')    
    f2 = codecs.open(dir_path+'typePropagation/rel2id.txt','w','utf-8')
    no = 0
    for line in f1.readlines():
        line = line.strip()
        
        items = line.split('\t')
        
        relName = items[1]
        relNo = int(cluster_info[no])+1
        no = no + 1
       
        #utilize the clustering information
        f2.write(relName+'\t'+str(relNo)+'\n')
        
        #don't use the clustering information
        #relNo =int(items[0])+ 1
        #f2.write(relName+'\t'+str(relNo)+'\n')
    f2.close()

def loadWord2VectFeature():
    model = gensim.models.word2vec.Word2Vec.load_word2vec_format('../data/food/features/GoogleNews-vectors-negative300.bin', binary=True)
    return model

def getY(dir_path):
    ent2id = getitem2id(dir_path+'typePropagation/entity2id.txt')
    rel2id = getitem2id(dir_path+'typePropagation/rel2id.txt')
    #fileName = '../main1/ftri_yelp_full.txt'
    fileName = dir_path+'ftri'+tag_doc+'.txt'
    f1 = codecs.open(fileName,'r','utf-8')
    model = loadWord2VectFeature()
    #relNeighbors = getRelNeighbors(dir_path,100)
    relNum = 500
    f2 =codecs.open(dir_path+'typePropagation/Y.txt','w','utf-8')
    f4 =codecs.open(dir_path+'typePropagation/Y_onlyw2v.txt','w','utf-8')
    f3 = codecs.open(dir_path+'typePropagation/entrel2entset.txt','w','utf-8')
#    ent_Num = len(ent2id)
#    rel_Num = len(rel2id)
   # Y = dok_matrix((ent_Num,rel_Num*2))
    for line in f1.readlines():
        line = line.strip()
        
        items = line.split('\t')
        #print 'line',line
        #这个地方容易出错！
        rel= items[2].strip()
        ent1 = items[7].strip()
        ent2 = items[9].strip()
        
        ent1_no = ent2id.get(ent1)
        ent2_no = ent2id.get(ent2)
        rel_no = rel2id.get(rel)
        if rel_no*2 >1000:
            print '出错了。。。',rel_no
#        #获取该relation的Neighbor
#        neighbors = relNeighbors[int(rel_no)-1]
#        s
#        if ent1_no!=None:
#            for key in neighbors:
#                temp_no = (key+1)*2-1
#                print temp_no
#               # Y[ent1_no,temp_no] = 1
#                strings = str(ent1_no)+'\t'+str(temp_no)+'\t'+'1'
#                f2.write(strings+'\n')
#        
#        if ent2_no!=None:
#            for key in neighbors:
#                 temp_no = (key+1)*2
#                 print temp_no
#                # Y[ent2_no,temp_no] = 1
#                 strings = str(ent2_no)+'\t'+str(temp_no)+'\t'+'1'
#                 f2.write(strings+'\n')
#        
#        if ent1_no!=None and ent2_no!=None:
#            for key in neighbors:
#                strings = str(ent1_no)+'\t'+str(key+1)+'\t'+str(ent2_no)
#                f3.write(strings+'\n')
                
        if ent1_no!=None:
            temp_no = rel_no*2-1
            #print temp_no
            strings = str(ent1_no)+'\t'+str(temp_no)+'\t'+'1'

            f2.write(strings+'\n')
            
            
            try:
                try:
                    ent1vector = model[ent1.replace(' ','_')]
                except:
                    items = ent1.split(' ')
                    #print 'items',items
                    ent1vector = model[items[0]]
                    for i in range(1,len(items)):
                        ent1vector = ent1vector + model[items[i]]
                for i in range(len(ent1vector)):
                    strings = str(ent1_no)+'\t'+str(i+1+relNum*2)+'\t'+str(ent1vector[i])
                    f2.write(strings+'\n')
                    strings = str(ent1_no)+'\t'+str(i+1)+'\t'+str(ent1vector[i])
                    f4.write(strings+'\n')
            except:
                print ent1
            
        try:    
            if ent2_no!=None:
                temp_no = rel_no*2
                #print temp_no
                strings = str(ent2_no)+'\t'+str(temp_no)+'\t'+'1'
                f2.write(strings+'\n')
                
               
                try:
                    ent2vector = model[ent2.replace(' ','_')]
                except:
                    items = ent2.split(' ')
                    #print 'items',items
                    ent2vector = model[items[0]]
                    for i in range(1,len(items)):
                        ent2vector = ent2vector + model[items[i]]
                for i in range(len(ent2vector)):
                        strings = str(ent2_no)+'\t'+str(i+1+relNum*2)+'\t'+str(ent2vector[i])
                        f2.write(strings+'\n')
                        strings = str(ent2_no)+'\t'+str(i+1)+'\t'+str(ent2vector[i])
                        f4.write(strings+'\n')
        except:
            print ent2
                    
            
        if ent1_no!=None and ent2_no!=None:
            strings = str(ent1_no)+'\t'+str(rel_no)+'\t'+str(ent2_no)
            f3.write(strings+'\n')
        
    f2.close()   
    f3.close()
    f4.close()

def getType2Num(dir_path):
    f1 = codecs.open(dir_path+'type2Num'+tag_doc+'.txt','r','utf-8')
    id2type = {}       
    for line in f1.readlines():
        line =line.strip()
        
        entName,num,ids = line.split('\t')
        id2type[int(ids)]=entName
    
    f2 = codecs.open(dir_path+'typePropagation/type2id.txt','w','utf-8')
    for key in id2type:
        f2.write(id2type[key]+'\t'+str(key)+'\n')
    
    f2.close()
    
if __name__=='__main__':
    #dir_path = '../data/nyt/' 
    #dir_path = '../data/yelp_entRent/'
    dir_path = '../data/food/'
    #getAllKnownTypeEnt(dir_path)
    getRel2id(dir_path)
    getY(dir_path)
    getType2Num(dir_path)
                
        