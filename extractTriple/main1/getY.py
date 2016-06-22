# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:14:22 2016

@author: DELL
"""
import codecs

dir_path = '../data/yelp_food/'
def getY(dir_path):
    ent2id = getitem2id(dir_path+'typePropagation/entity2id.txt')
    rel2id = getitem2id(dir_path+'typePropagation/rel2id.txt')
    fileName = '../main1/ftri_yelp_full.txt'
    
    f1 = codecs.open(fileName,'r','utf-8')
    
    f2 =codecs.open(dir_path+'typePropagation/Y.txt','w','utf-8')
    f3 = codecs.open(dir_path+'typePropagation/entrel2entset.txt','w','utf-8')
    
    for line in f1.readlines():
        line = line.strip()
        
        items = line.split('\t')
        
        rel= items[2]
        ent1 = items[7]
        ent2 = items[9]
        
        ent1_no = ent2id.get(ent1)
        ent2_no = ent2id.get(ent2)
        
        rel_no = rel2id.get(rel)
        
        if ent1_no!=None:
            temp_no = rel_no*2-1
            print temp_no
            strings = str(ent1_no)+'\t'+str(temp_no)+'\t'+'1'
            f2.write(strings+'\n')
        
        if ent2_no!=None:
            temp_no = rel_no*2
            print temp_no
            strings = str(ent2_no)+'\t'+str(temp_no)+'\t'+'1'
            f2.write(strings+'\n')
        
        if ent1_no!=None and ent2_no!=None:
            strings = str(ent1_no)+'\t'+str(rel_no)+'\t'+str(ent2_no)
            f3.write(strings+'\n')
    f2.close()
    f3.close()