# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 08:54:57 2016

revised Mar 22
@author: DELL
"""
import sys
sys.path.append('../main1')
import codecs
from analysisEntAndRel import proSeedTriple
import numpy as np
from scipy.sparse import dok_matrix
import re
import string
class RelFeatureGen():
    def __init__(self):
#        dir_path ='../data/nyt/'
#        self.f_entHasName = dir_path+'nyt_enthasName_type.txt_new'
#        self.f_trip = dir_path+'ftri.txt'
#        self.textf = dir_path+'nyt13_sample10k.txt_new_context'
#        self.f_ent = dir_path+'extract_ent_has_type.txt'
#        self.f_type = dir_path+'type2Num.txt'
#        self.f_missingtypeent = '../data/nyt/typePropagation/entity_missingtype1.txt'
#        self.f_entity2id = '../data/nyt/typePropagation/entity2id.txt' 
#        self.proSeedTriple = proSeedTriple(self.f_trip,self.f_entHasName)
########################################################################
        self.f_entHasName = "../data/food/yelp_enthasName_type.txt_new"
        self.f_trip = '../data/food/ftri.txt'
        self.textf = '../data/food/yelp_sample50k.txt_new_context'
        self.f_ent = "../data/food/extract_ent_has_type.txt"
        self.f_type = '../data/food/type2Num.txt'
        self.f_missingtypeent = '../data/food/typePropagation/entity_missingtype1.txt'
        self.f_entity2id = '../data/food/typePropagation/entity2id.txt'
        self.proSeedTriple = proSeedTriple(self.f_trip,self.f_entHasName)
############################################################################
#        self.f_entHasName = "../data/yelp_food_full/food_enthasName_type.txt_new"
#        self.f_trip = '../main1/ftri_yelp_full.txt'
#        self.textf = '../data/yelp_food_full/yelp_full_review.txt_new_context'
#        self.f_ent = "../data/yelp_food_full/extract_ent_has_type.txt"
#        self.f_type = '../data/yelp_food_full/type2Num.txt'
#        self.proSeedTriple = proSeedTriple(self.f_trip,self.f_entHasName)
    
        
    def getEntType(self):
        f1 = codecs.open(self.f_type,'r','utf-8')
        type2id = {}
        id2type = {}
        for line in f1.readlines():
            line = line.strip()
            items = line.split('\t')
            typer = items[0]
            ids = items[2]
            type2id[typer] = ids
            id2type[ids] = typer
        return type2id,id2type
        
    def getAllWords(self):
        wordset = set()
        f1= codecs.open(self.textf, 'r','utf-8')
        
        for line in f1.readlines():
            line = line.strip()
            
            ids,context = line.split('\t')
            
            items = context.split(' ')
            
            for key in items:
                wordset.add(key)
        wordsList = list(wordset)
        word_to_id = { ch:i for i,ch in enumerate(wordsList) }
        id_to_word = { i:ch for i,ch in enumerate(wordsList) }
        return word_to_id,id_to_word
        
    def getEntTypes(self):

        f1 = codecs.open(self.f_ent,'r','utf-8')
        ent_types_dict={}
        for line in f1.readlines():
            line = line.strip()
            items = line.split('\t')
            ent1 = items[0]
            types = ''
            for i in range(1,len(items)):
                if items[i] !='NIL':
                    types = types + items[i]+'\t'
            types =types.strip()
            print types
            if types!='':
                ent_types_dict[ent1] =types
        print len(ent_types_dict)
        
        return ent_types_dict
    
    #get the type signature featue
    def getRelTypeSig(self,rel_list,rel_to_id,id_to_rel):
        #get the entity is test data
        misstype_ents = {}
        misstypeent = codecs.open(self.f_missingtypeent,'r','utf-8')
        entity2id = codecs.open(self.f_entity2id,'r','utf-8')
        id2ent = {}
        for line in entity2id.readlines():
            line = line.strip()
            name,ids = line.split('\t')
            id2ent[ids] = name
        for line in misstypeent.readlines():
            line = line.strip()
            ent = id2ent.get(line)
            misstype_ents[ent] = 1
            
        type2id,id2type = self.getEntType()
               
        rel_num = len(rel_list)
        type_num = len(type2id)
        rel_typeSig = dok_matrix((rel_num,2*type_num),dtype='float')
        sethastypeSig = range(0,rel_num)
        ent_types_dict = self.getEntTypes()
        
        f2 = open(self.f_trip,'r')
        for line in f2.readlines():
            print line
            line = line.strip()
            items = line.split('\t')
            
            rel = items[2].strip()
            ent1 = items[7].strip()
            ent2 = items[9].strip()
            
           # print ent1,ent2
            rel_id = rel_to_id[rel]
            types = ''
            if misstype_ents.get(ent1) ==None:
                temp = ent_types_dict.get(ent1)
                if temp !=None:
                    types = temp
                types = types.strip()
                if types !='':
                    lent = len(types.split('\t'))
                    #print 'type lent',lent
                    for typesi in types.split('\t'):
                        #print 'typesi:',typesi
                        typeid_i = int(typesi)
                        #rel_typeSig[rel_id,typeid_i] =  rel_typeSig[rel_id,typeid_i] + 1.0/float(lent)
                        rel_typeSig[rel_id,typeid_i] =  rel_typeSig[rel_id,typeid_i] + 1.0
            types = ''
            if misstype_ents.get(ent2) ==None:
                temp = ent_types_dict.get(ent2)
                if temp!=None:
                    types = types+'\t'+temp
                types = types.strip()
                if types !='':
                    lent = len(types.split('\t'))
                    #print 'type lent',lent
                    for typesi in types.split('\t'):
                        #print 'typesi:',typesi
                        typeid_i = int(typesi)
                        #rel_typeSig[rel_id,typeid_i] =  rel_typeSig[rel_id,typeid_i] + 1.0/float(lent)
                        rel_typeSig[rel_id,typeid_i+type_num] =  rel_typeSig[rel_id,typeid_i+type_num] + 1.0
            #print 'types:\t',types
            types = types.strip()
            if types !='':
                lent = len(types.split('\t'))
                #print 'type lent',lent
                for typesi in types.split('\t'):
                    #print 'typesi:',typesi
                    typeid_i = int(typesi)
                    #rel_typeSig[rel_id,typeid_i] =  rel_typeSig[rel_id,typeid_i] + 1.0/float(lent)
                    rel_typeSig[rel_id,typeid_i] =  rel_typeSig[rel_id,typeid_i] + 1.0
        set_miss_rel=set()
        for i in range(len(rel_list)):
            if  sum(rel_typeSig[i].toarray()[0]) ==0:
                #print id_to_rel[i]
                sethastypeSig.remove(i)
                set_miss_rel.add(i)
#        print 'set_miss_rel',len(set_miss_rel)
#        print np.shape(rel_typeSig)
        return rel_typeSig,sethastypeSig,set_miss_rel
    def getIterText(self):
        f1 =codecs.open(self.textf,'r','utf-8')
        while(1):
            blocks = f1.readlines(10000)
            if not blocks:
                break
            for line in blocks:
                #yield is a very useful 
                yield line
            #print 'start to get another 10000 data'
    def getContextFeature(self):
        import time
        print 'start to get Context Feature'
        start = time.time()
        
        from sklearn.feature_extraction.text import TfidfTransformer
        from sklearn.feature_extraction.text import CountVectorizer
        #when we meet the large corpus, need to input an iteration!
        corpus = self.getIterText()
        #transfer the text into word frequency matrix
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
        
        print 'get word'
        word=vectorizer.get_feature_names()
        print 'get weight'
        weight=tfidf
        
        print 'weight type:', type(weight)
        #print weight
        end = time.time()
        
        print 'total time: \t', end-start
        return weight,word
    

    def add2FeatrueSet(self,strs,featureSet,word_to_id):
        strs = strs.strip()
        items = strs.split('\t')
        for itr in items:
            #map to the tfidf word dict
            temp = word_to_id.get(itr)
            if temp!=None:
                featureSet.add(temp)
                
        return featureSet
    
    def dealEveryRelContext(self,reli,key,tempr,word_to_id):
        #for key in rel_list.get(reli):
        lent = len(tempr.split(' '))
        symbols = list(string.punctuation)
        lineNo,sentence,ent1,ent2 = key.split('\t')
        items = sentence.split(' ')
        rel_sent =[]
        for ite in items:
            if ite not in symbols:
                rel_sent.append(ite)
        flag =0
        fea1 = ''
        fea2 = ''
        rel_Context_word = set()
        rel_Context_word = self.add2FeatrueSet(ent1,rel_Context_word,word_to_id)
        rel_Context_word = self.add2FeatrueSet(ent2,rel_Context_word,word_to_id)
        for i in range(len(rel_sent)-lent+1):
            if ' '.join(rel_sent[i:i+lent]) == tempr:
                #this is the words feature of left and right two words of the verb
                fea1 = ' '.join(rel_sent[i+lent:i+lent+5])
                fea2 = ' '.join(rel_sent[i-5:i])
                flag =1
        #add ent features
        #print reli,'------',fea1,'---',fea2,'---',ent1,'---',ent2
        rel_Context_word = self.add2FeatrueSet(fea1,rel_Context_word,word_to_id)
        rel_Context_word = self.add2FeatrueSet(fea2,rel_Context_word,word_to_id)
                        
        
        
        if flag ==0 :
            lent = len(reli.split(' '))
            for i in range(len(items)-lent+1):
                if ' '.join(items[i:i+lent]) == reli:
                    #this is the words feature of left and right two words of the verb
                    fea1 = ' '.join(items[i+lent:i+lent+5])
                    fea2 = ' '.join(items[i-5:i])
                    flag =1 
            #add ent features
            print reli,'------',fea1,'---',fea2,'---',ent1,'---',ent2
            rel_Context_word = self.add2FeatrueSet(fea1,rel_Context_word,word_to_id)
            rel_Context_word = self.add2FeatrueSet(fea2,rel_Context_word,word_to_id)
           
        return_para =[]
        return_para.append(lineNo)
        return_para.append(rel_Context_word)
        if flag ==0:
            print 'no !!!!!!!!!!!' ,reli,'------',tempr,'------',rel_sent
            return None
        else:
            return return_para
            
    def getRelContextFeature(self,rel_dict,rel_to_id,id_to_rel):
        symbols = list(string.punctuation)
        tfidf_weight,words = self.getContextFeature()
        word_to_id = { ch:i for i,ch in enumerate(words) }        
        #id_to_word = { i:ch for i,ch in enumerate(words) }
        print 'start to get the feature!'
        rel_num = len(rel_dict)
        word_num = len(word_to_id)
        rel_contFeature = dok_matrix((rel_num,word_num),dtype='float')
        
        for reli in rel_dict:
            temp = reli
            rel_id = rel_to_id[reli]
            
            temp_it = temp.split(' ')
            tempr =[]
            for ite in temp_it:
                if ite not in symbols:
                    tempr.append(ite)
                tempw_r = word_to_id.get(ite)
                #把relation的自己包含的信息也加入进去！
                if tempw_r!=None:
                    rel_contFeature[rel_id,tempw_r] = rel_contFeature[rel_id,tempw_r] + 1
            tempr = ' '.join(tempr)
            
            
            for key in rel_dict.get(reli):
                paras  = self.dealEveryRelContext(reli,key,tempr,word_to_id)
                if paras:
                    print 'rel has no context',
                    lineNo = paras[0]                
                    rel_Context_word = paras[1]
                    #print rel_Context_word
                    if rel_Context_word !=None:                
                        for word in rel_Context_word:
                            rel_contFeature[rel_id,word] = rel_contFeature[rel_id,word] + tfidf_weight[int(lineNo),word]       
        return rel_contFeature
        

if __name__=='__main__':
    relf = RelFeatureGen()
    proSeedTrip = relf.proSeedTriple
    rel_dict,rel2Num = proSeedTrip.analyRel()
    print 'number of rel_dict',len(rel_dict)
    rel_list  = rel_dict.keys()
    rel_to_id = { ch:i for i,ch in enumerate(rel_list) }        
    id_to_rel = { i:ch for i,ch in enumerate(rel_list) }
    rel2Num = sorted(rel2Num.items(),key=lambda d:d[1])
    for item in rel2Num:
        print item[0],'\t',item[1]
    #generation_phrase = "The quick brown fox jumps"
    #word_to_id,id_to_word =relf.getAllWords()
    #relf.getRelTypeSig(rel_list,rel_to_id,id_to_rel)
    #print len(word_to_id)
    #relf.getContextFeature()
    #relf.getRelContextFeature(rel_dict,rel_to_id,id_to_rel)