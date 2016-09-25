# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:18:36 2016

@author: DELL
"""
import codecs
import sys
sys.path.append('../utils')
#from getFreebaseType import FreebaseAPI
#from deleteEntStopWords import deleteEntStopW
from filterFreebaseFoodType import TypeDict

class proSeedTriple():
    def __init__(self,f_name,f_entHasName):
        self.f_name = f_name
        self.f_entHasName = f_entHasName
        
    def analyEnt(self,ent_name_type):
        ents = {}
        f_name = self.f_name
        with open(f_name,'r') as file:
            for line in file:
                line = line.strip()
                items = line.split('\t')
                if len(items)==6:
                    ent = items[6]
                    if ents.get(ent)==None:
                        ents[ent] = ent_name_type[ent]
                        print ent
                else:
                    if len(items)==10:
                        ent1 = items[7]
                        ent2 = items[9]
                        print ent1
                        print ent2
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
    
    def analyRel(self):
        f_name = self.f_name
        #key is the relation, the value is the context which the relation is merged
        rels = {}
        rel2Num= {}
        with open(f_name,'r') as file:
            for line in file:
                #print 'line',line
                line = line.strip()
                items = line.split('\t')
                if len(items)==10:
                    ContextNo = items[0]
                    ent1 = items[7]
                    ent2 = items[9]
                    if int(ContextNo)==None:
                        print int(ContextNo)
                    rel = items[2].strip()
                    if rel =='staring':
                        print rel
                    sentence = items[5]
                    strs =ContextNo+'\t'+sentence+'\t'+ent1+'\t'+ent2
                    if rels.get(rel) ==None:
                        rel2Num[rel] = 1
                        rels[rel] = {strs}
                    else:
                        temps = rels[rel]
                        temps.add(strs) 
                        rels[rel] = temps
                        rel2Num[rel] +=1                      
        return rels,rel2Num
        
    def getentNameType(self):
        f_entHasName = self.f_entHasName
        ent_name_type = {}
        with open(f_entHasName,'r') as file:
            for line in file:
                line = line.strip()
                items = line.split('\t')
                #pid = items[0]
                name = items[1]
                types = ''
                for i in range(2,len(items)):
                    types = types + items[i] + '\t'
                name = name.lower()
                types = types.strip()
                ent_name_type[name] = types
        return ent_name_type
        
if __name__=="__main__":
    dir_path = '../data/nyt/'
    domain = 'nyt'
#    dir_path ='../data/food/'
#    domain = 'yelp'
    #filetag='_entRent'
    filetag=''
    f_name =dir_path+'ftri'+filetag+'.txt'
    f_entHasName = dir_path+domain+'_enthasName_type.txt_new'
    
    pro = proSeedTriple(f_name,f_entHasName)
    ent_name_type = pro.getentNameType()
    
    ents = pro.analyEnt(ent_name_type)
    rels = pro.analyRel()

    
    
    
#    typeDictClass = TypeDict()
#    typeDict,typeDict_map = typeDictClass.getTypeDict()
#    print 'get type dict finish'
    typeDict_map = {}
    f_typeDictMap = codecs.open(dir_path+domain+'_mintype2populortype.txt','r','utf-8')
    for line in f_typeDictMap.readlines():
        line = line.strip()
        items = line.split('\t')
        mintype = items[0]
        poptype = items[1]
        typeDict_map[mintype] = poptype
    #print len(typeDict_map)
    
    all_typeDict_map = {}
    f_typeDictMap_all = codecs.open(dir_path+domain+'_alltype2populortype.txt','r','utf-8')
    for line in f_typeDictMap_all.readlines():
        line = line.strip()
        items = line.split('\t')
        alltype = items[0]
        poptype = items[1]
        all_typeDict_map[alltype] = poptype
    #print len(all_typeDict_map)    
    
    hastype=0
    type_map = {}
    for key in ents:
        types = ents[key]
        if  types!='NIL':
            hastype = hastype + 1
            items = types.split('\t')
            typenolist = set()
            for typei in items:
                newtypei = typeDict_map.get(typei)
                if newtypei == None:
                    print 'merge new type\t',key,typei
                if type_map.get(newtypei) ==None:
                    type_map[newtypei]=1
                else:
                    type_map[newtypei] = type_map[newtypei] + 1
    
    #print 'type_map',type_map
    type_map_sorted = sorted(type_map.items(),key=lambda d:d[1])
    #print 'type_map_sorted',type_map_sorted
    rel_type2num = {}
    type2poptype = {}
    for key in type_map_sorted:
        temp_key0 = key[0]
        if key[1]<=300:
            temp_key0 = all_typeDict_map.get(key[0])
            type2poptype[key[0]] = temp_key0
        else:
            type2poptype[key[0]] = key[0]
            
        if rel_type2num.get(temp_key0) ==None:
            rel_type2num[temp_key0] = key[1]
        else:
            rel_type2num[temp_key0] = rel_type2num[temp_key0] + key[1]
    i = 0
    type_map_sorted = sorted(rel_type2num.items(),key=lambda d:d[1])
    
    reltype2id = {}
    typefile = codecs.open(dir_path+'type2Num'+filetag+'.txt','w','utf-8')
    for key in type_map_sorted:
        reltype2id[key[0]] = i
        typefile.write(key[0]+'\t'+str(key[1])+'\t'+str(i)+'\n')
        i = i + 1
    typefile.close()
    
    
    f_ent = codecs.open(dir_path+'extract_ent_has_type'+filetag+'.txt','w','utf-8')
    
    for key in ents:
        types = ents[key]
        if  types!='NIL':
            hastype = hastype + 1
            items = types.split('\t')
            typenolist = set()
            for typei in items:
                newtypei = typeDict_map.get(typei)
                relnewtypei = type2poptype.get(newtypei)
                typeids = reltype2id.get(relnewtypei)
                typenolist.add(str(typeids))
            typenolist = '\t'.join(list(typenolist))
            f_ent.write(key+'\t'+typenolist.strip()+'\n')
        else:
            f_ent.write(key+'\t'+types+'\n')
    f_ent.close()