# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:18:36 2016

@author: DELL
"""
import codecs
import sys
sys.path.append('../utils')
from getFreebaseType import FreebaseAPI
from deleteEntStopWords import deleteEntStopW
def analyEnt(f_name,ent_name_type):
    ents = {}
    with codecs.open(f_name,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            items = line.split('\t')
            if len(items)==6:
                ent = items[5]
                if ents.get(ent)==None:
                    ents[ent] = ent_name_type[ent]
            else:
                if len(items)==8:
                    ent1 = items[5]
                    ent2 = items[7]
                    if ents.get(ent1)==None:
                        if ent_name_type.get(ent1) != None:
                            ents[ent1] = ent_name_type[ent1]
                        else:
                            ents[ent1] = 'NIL'
                    if ents.get(ent2)==None:
                       if ent_name_type.get(ent2) != None:
                            ents[ent2] = ent_name_type[ent2]
                       else:
                            ents[ent2] = 'NIL'
    return ents

def analyRel(f_name):
    rels = set()
    with codecs.open(f_name,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            items = line.split('\t')
            if len(items)>=4:
                rel = items[1]
                rels.add(rel)
    return rels
            
f_name = 'ftri.txt'
f_entHasName = "../data/food/food_enthasName_type.txt"
ent_name_type = {}
with codecs.open(f_entHasName,'r','utf-8') as file:
    for line in file:
        line = line.strip()
        items = line.split('\t')
        pid = items[0]
        name = items[1]
        types = ''
        for i in range(2,len(items)):
            types = types + items[i] + '\t'
        name = name.lower()
        ent_name_type[name] = types
ents = analyEnt(f_name,ent_name_type)
rels = analyRel(f_name)

f_ent = codecs.open("../data/food/extract_ent_has_type.txt",'w','utf-8')
hastype=0
#fr = FreebaseAPI()
#dels = deleteEntStopW()
type_map = {}
for key in ents:
    types = ents[key]
    if  types!='NIL':
        hastype = hastype + 1
        items = types.split('\t')
        for typei in items:
            if type_map.get(typei) ==None:
                type_map[typei]=1
            else:
                type_map[typei] = type_map[typei] + 1
    f_ent.write(key+'\t'+ents[key]+'\n')

typefile = codecs.open('../data/food/type2Num.txt','w','utf-8')

type_map_sorted = sorted(type_map.items(),key=lambda d:d[1])
for key in type_map_sorted:
    typefile.write(key[0]+'\t'+str(key[1])+'\n')
typefile.close()

#    else:
#        name_types = fr.getTypes(key)
#        if name_types !=None:
#            items = name_types.split('\t')
#            types = '\t'.join(items[1:-1])
#            hastype = hastype + 1
#            f_ent.write(key+'\t'+ents[key]+'\t'+types+'\n')
#        else:
#            items = key.split(' ')
#            newent = dels.delStopW(items)
#            name_types = fr.getTypes(key)
#            if name_types !=None:
#                items = name_types.split('\t')
#                types = '\t'.join(items[1:-1])
#                hastype = hastype + 1
#                f_ent.write(key+'\t'+ents[key]+'\t'+types+'\n')
#            
f_ent.close()
print hastype