# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 19:44:56 2016

@author: DELL
"""
import  codecs
dir_path = '../data/food/'

def getMissingEntid2Name():
    f_missEntId= codecs.open(dir_path+'typePropagation/entity_missingtype.txt','r','utf8')
    f_missEntId_Type = codecs.open(dir_path+'typePropagation/entity_missingtype_c.txt','r','utf8')
    
    f_ent2id = codecs.open(dir_path +'typePropagation/entity2id.txt','r','utf8')
    id2name = {}
    for line in f_ent2id:
        line = line.strip()
        items = line.split('\t')
        
        if len(items)==2:
            name = items[0]
            ids = items[1]
            
            id2name[ids] = name
        else:
            print items
        
        
    f_type2id = codecs.open(dir_path +'typePropagation/type2id.txt','r','utf8')
    id2types = {}
    for line in f_type2id:
        line = line.strip()
        items = line.split('\t')
        
        types = items[0]
        ids = items[1]
        
        id2types[ids] = types
    
    entName2type = {}
    for line in f_missEntId_Type:
        line = line.strip()
        items = line.split('\t')
        
        entid = items[0]
        typeid = items[1]
        
        entName = id2name[entid]
        typeName = id2types[typeid]
        
        if entName2type.get(entName)==None:
            entName2type[entName] = typeName
        else:
            entName2type[entName] = entName2type[entName]+'\t'+typeName
    return entName2type

entName2type = getMissingEntid2Name()
entNameInFiger ={}
for key in entName2type:
    entNameInFiger[key] =0
figer_ent2type={}
f_missEntId_Type = codecs.open(dir_path+'figer/figer_result','r','utf8')
for line in f_missEntId_Type:
    line = line.strip()
    
    items = line.split('\t')
    
    name = items[0].lower()
    types = items[1]
    
    print name
    flag = False
    for key in entName2type:
        if key in name:
            flag = True
            entNameInFiger[key]= 1
            break
        if name in key:
            flag =True
            entNameInFiger[key] = 1
            break
            
    if flag:
        if figer_ent2type.get(name) !=None:
            figer_ent2type[name].append(types)
        else:
            figer_ent2type[name] = [types] 