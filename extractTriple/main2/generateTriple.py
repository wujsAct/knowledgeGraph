# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 20:52:58 2016

@author: DELL
"""
import time
import codecs
from TripleRecord import TripleRecord
from PhraseRecord import EntRecord
import collections

class generateTriples():
    """
    @function: to get word's index in the sentence 
    """
    def getIndex(self,word,sentence):
        #sentence = sentence.split()
        
        for i in range(len(sentence)):
            if word == sentence[i]:
                return i
    """
    @function: to get stanford dependency parser tree
    """
    def get_dependency_tree(self,sentence,dep_trip,relation_phrase,entity_phrase):
    
        subtriple={}
        for i in range(len(dep_trip)):
            depenR = dep_trip[i][1]
            extent =None
            extrel = None
            if depenR == u'nsubj':
                subj = dep_trip[i][0][0]
               # print 'subj',subj
                rel = dep_trip[i][2][0]
               # print 'rel',rel
                rel_id = dep_trip[i][2][1]
                ent_id = dep_trip[i][0][1]
                tagrel1 = 0
                tagrel2 = 0
                for key in relation_phrase:
                    rel_range1, rel_range2 = key.getIndexes()
                    
                    if rel_id in range(rel_range1, rel_range2):
                        extrel = sentence[rel_range1:rel_range2]
                        tagrel1 = rel_range1
                        tagrel2 = rel_range2
                        tagrel = key
                
                for key in entity_phrase:
                    ent_range1, ent_range2 = key.getIndexes()
                    
                    if ent_id in range(ent_range1,ent_range2):
                        if ent_id not in range(tagrel1,tagrel2):
                            extent = sentence[ent_range1:ent_range2]
                            tagent = key
                            break
                            
            if extent !=None and extrel!=None and ent_id < rel_id:
                subtriple[tagrel] = [tagent,'l',u'nsubj']
                #print extent,extrel
               
            extent =None
            extrel = None
            if depenR == u'dobj':
                obj = dep_trip[i][0][0]
                rel = dep_trip[i][2][0]
                rel_id = dep_trip[i][2][1]
                ent_id = dep_trip[i][0][1]
                tagrel1 = 0
                tagrel2 = 0
                tagrel = 0
                for key in relation_phrase:
                    rel_range1, rel_range2 = key.getIndexes()
                    
                    if rel_id>=rel_range1 and rel_id <=rel_range2:
                        extrel = sentence[rel_range1:rel_range2]
                        tagrel1 = rel_range1
                        tagrel2 = rel_range2
                        tagrel = key
                
                tagent = 0
                for key in entity_phrase:
                    ent_range1, ent_range2 = key.getIndexes()                                                                                                                                                                         
                    if ent_id>=ent_range1 and ent_id <=ent_range2:
                        if ent_id < tagrel1 or ent_id> tagrel2:
                            extent = sentence[ent_range1:ent_range2]
                            tagent = key
           
            if extent !=None and extrel!=None:
                subtriple[tagrel] = [tagent,'r',u'dobj']
        return subtriple

    def getReverbTriple(self,sentence,relation_phrase,entity_phrase):
        '''
        @record in 2016/9/25
        '''
        ent_flag_dict= {}
        for key in entity_phrase:
            ent_flag_dict[key] = 0
        subtriple={}
        for key in relation_phrase:
            rel_range1, rel_range2 = key.getIndexes()
            rel_phr =  sentence[rel_range1:rel_range2]
            #print 'relation key',rel_phr
            #left argument
            mins_left = 100
            mins_right=100
            flagkey1 = None
            value1 = '0'
            flagkey2 = None
            value2 = '0'
            for key1 in entity_phrase:
                #print 'entity',key1
                ent_range1, ent_range2 = key1.getIndexes()  
                mins_temp =  rel_range1 - ent_range2
                if mins_temp >= 0 and mins_temp < mins_left:
                    mins_left = mins_temp
                    flagkey1 = key1
                    value1 = sentence[ent_range1:ent_range2]
                    
                mins_temp = ent_range1 - rel_range2
                
                if mins_temp>=0 and mins_temp < mins_right:
                    mins_right = mins_temp
                    flagkey2 = key1
                    value2 = sentence[ent_range1:ent_range2]
                    
            '''
            @attention the process!
            '''
            if flagkey1 is not None and flagkey2 is not None:
                subtriple[key] = [[flagkey1, flagkey2,u'nearArguments']]
                ent_flag_dict[flagkey1]=1
                ent_flag_dict[flagkey2]=1
    
        #pay attention to some entity has no distributed the relation, so we need to distribute them to the relation
        for key in ent_flag_dict:
            if ent_flag_dict[key]==0:
                ent_range1, ent_range2 = key.getIndexes()
                mins_left = 100
                mins_right=100
                flagkey1 = None
                flagkey2 = None
                value1 = '0'
                value2 = '0'
                for key1 in relation_phrase:
                    rel_range1, rel_range2 = key1.getIndexes()
                    rel_phr =  sentence[rel_range1:rel_range2]
                    mins_temp =  rel_range1 - ent_range2
                    if mins_temp >= 0 and mins_temp < mins_left:
                        mins_left = mins_temp
                        flagkey1 = key1
                        value1 = sentence[rel_range1:rel_range2]
                    
                    mins_temp = ent_range1 - rel_range2
                    if mins_temp>=0 and mins_temp < mins_right:
                        mins_right = mins_temp
                        flagkey2 = key1
                        value2 = sentence[rel_range1:rel_range2]
            
                value_ent = None
                flagkey =None
                '''
                find the right relation(the entity is the left argument)
                '''
                if  flagkey1!=None and flagkey2 == None:
                    if subtriple.get(flagkey1)!=None:
                        temp = subtriple[flagkey1]
                        temp =temp[0]
                        value_ent = [key,temp[1],'nearArguments']
                        flagkey = flagkey1
                '''
                find the left relation(the entity is the right argument)
                '''
                if flagkey2!= None and flagkey1 ==None:
                    if subtriple.get(flagkey2)!=None:
                        temp = subtriple[flagkey2]
                        temp =temp[0]
                        value_ent = [temp[0],key,u'nearArguments']
                        flagkey = flagkey2
                        
                if flagkey1!=None and flagkey2!=None:
                    if mins_left <mins_right:
                        if subtriple.get(flagkey1)!=None:
                            temp = subtriple[flagkey1]
                            temp =temp[0]
                            value_ent = [key,temp[1],u'nearArguments']
                            flagkey = flagkey1
                    else:
                        if subtriple.get(flagkey2)!=None:
                            temp = subtriple[flagkey2]
                            temp =temp[0]
                            value_ent = [temp[0],key,u'nearArguments']
                            flagkey = flagkey2
            
                if value_ent !=None and flagkey!=None:
                   subtriple[flagkey].append(value_ent)
        return subtriple

    def isRelation(self,ids,relation_phrase):
        tag = False
        relkey =None
        for key in relation_phrase:
            rel_range1, rel_range2 = key.getIndexes()
            #print 'isrel','\t',str(rel_range1), '\t',str(rel_range2)
            if ids in range(rel_range1,rel_range2):
                tag=True
                relkey=key
        return tag,relkey
    
    def isEnt(self,ids,entity_phrase):
        tag = False
        entkey =None
        for key in entity_phrase:
            ent_range1, ent_range2 = key.getIndexes()
            #print 'isrel','\t',str(rel_range1), '\t',str(rel_range2)
            if ids in range(ent_range1,ent_range2):
                tag=True
                entkey=key
        return tag,entkey
        
    def getFinalTriple(self,lineNo,sentence,dep_trip,relation_phrase,entity_phrase,tag):
        sentence = sentence.split()
        #print 'get sentence finish!'
        subtriple1 = self.get_dependency_tree(sentence,dep_trip,relation_phrase,entity_phrase)
        #print 'get_dependency_tree is normal'
        subtriple2 = self.getReverbTriple(sentence,relation_phrase,entity_phrase)
        #print 'reverb triple is normal'
#        for rel in subtriple2:
#            sr,er = rel.getIndexes()
#            for key in subtriple2[rel]:
#                s1,e1 = key[0].getIndexes()
#                s2,e2 = key[1].getIndexes()
#                print 'Reverbs: ent1:',' '.join(sentence[s1:e1]),'\t rel:',' '.join(sentence[sr:er]),'\t ent2:',' '.join(sentence[s2:e2]),'\t',key[2]
      
        for key in subtriple1:
            flagr = 0
            if subtriple2.get(key)!=None:
                value1 = subtriple1[key]
                ent = value1[0]
                flag = value1[1]
                strategy = value1[2]
            
                value2 = subtriple2[key][0]
                ent1 = value2[0]
                ent2 = value2[1]
                
                ent1_start, ent1_end = ent1.getIndexes()
                ent2_start, ent2_end = ent2.getIndexes()
                rel_start, rel_end = key.getIndexes()

                if flag == 'r':
                    ent2 = ent
                if flag =='l':
                    ent1 = ent
                #opt to replace the first triples!
                subtriple2[key][0] = [ent1, ent2, strategy]
            else:
                '''
                we may not distribute any arguments for relations!
                '''
                rel_start, rel_end = key.getIndexes()
                subtriple2[key] = [subtriple1[key]]
        
        '''
        we also need to revise the [rel1,conj,rel2] have same left entity, ignore the nsubj and dobj strategy
        this kind of verb need to share the left ents
        '''
        for i in range(len(dep_trip)):
        
            depenR = dep_trip[i][1]
            if depenR ==u'conj':
                #print depenR
                rel1 = dep_trip[i][2][0]
                rel1_id = dep_trip[i][2][1]
                
                rel2 = dep_trip[i][0][0]
                rel2_id = dep_trip[i][0][1]
                tag1,key1 = self.isRelation(rel1_id,relation_phrase)
                #print tag1,key1
                tag2,key2 = self.isRelation(rel2_id,relation_phrase)
                #print rel2_id
                #print tag2,key2
                if tag1 and tag2:
                    #print subtriple2[key1]
                    if key1 in subtriple2 and key2 in subtriple2:
                        value1 = subtriple2[key1]
                        ent1 = value1[0][0]
                        for i in range(len(subtriple2[key2])):
                            value2 = subtriple2[key2][i]
                            if isinstance(value2[1],str) and value2[1]=='r':
                                ent2 = value2[0]
                            else:
                                ent2 = value2[1]
                            subtriple2[key2][i] = [ent1,ent2,u'depenR_conj']
                    
            if depenR ==u'advcl':
                #print depenR
                rel1 = dep_trip[i][2][0]
                rel1_id = dep_trip[i][2][1]
                
                rel2 = dep_trip[i][0][0]
                rel2_id = dep_trip[i][0][1]
                tag1,key1 = self.isRelation(rel1_id,relation_phrase)
                #print tag1,key1
                tag2,key2 = self.isRelation(rel2_id,relation_phrase)
                #print rel2_id
                #print tag2,key2
                if tag1 and tag2:
                    #print subtriple2[key1]
                    if key1 in subtriple2 and key2 in subtriple2:
                        value1 = subtriple2[key1]
                        ent1 = value1[0][0]
                        
                        for i in range(len(subtriple2[key2])):
                            value2 = subtriple2[key2][i]
                            #print 'value2',value2
                            if value2[2] not in [u'depenR_conj',u'nsubj',u'dobj']:
                                if isinstance(value2[1],str):
                                    ent2 = value2[0]
                                else:
                                    ent2 = value2[1]
                                subtriple2[key2][i] = [ent1,ent2,u'advcl']
            if depenR ==u'conj':
                ent1 = dep_trip[i][2][0]
                ent1_id = dep_trip[i][2][1]
                #print 'ent1:',ent1
                ent2 = dep_trip[i][0][0]
                ent2_id = dep_trip[i][0][1]
                #print 'ent2:',ent2
                tag1,key1 = self.isEnt(ent1_id,entity_phrase)
                tag2,key2 = self.isEnt(ent2_id,entity_phrase)
                if tag1 and tag2:
                    s,e = key1.getIndexes()
                    #print 'ent1:',' '.join(sentence[s:e]),'\t',int(s),'\t',int(e)
                    s,e = key2.getIndexes()
                    #print rel2_id
                    #print 'ent2:',' '.join(sentence[s:e]),'\t',int(s),'\t',int(e)
                    for key in subtriple2:
                        for i in range(len(subtriple2[key])):
                            value2 = subtriple2[key][i]
                            if not isinstance(value2[1],str) and value2[1] == key1:
                                ent1_left = value2[0]
                                subtriple2[key].append([ent1_left,key2,u'depenE_conj'])
                            
        triples = collections.defaultdict(set)
        for key in subtriple2:
            rel = key
            value = subtriple2[rel]
            
            for i in range(len(value)):
                if not isinstance(value[i],EntRecord) and not isinstance(value[i],str):
                    ent1 = value[i][0]
                    ent1_start, ent1_end = ent1.getIndexes()
                    ent2 = value[i][1]
                    strategy = value[i][2]
                    #print 'strategy',strategy
                    if not isinstance(value[i][1],str):
                        ent2_start, ent2_end = ent2.getIndexes()
                        rel_start, rel_end = key.getIndexes()
                        tri = lineNo+'\t'+' '.join(sentence[ent1_start:ent1_end])+'\t'+u' '.join(sentence[rel_start:rel_end])+'\t'+u' '.join(sentence[ent2_start:ent2_end])+'\t'+str(1)+'\t'+u' '.join(sentence)
                        triples[tri].add(strategy)
        if len(triples)==0:
            return 'None'
        else:
            return triples