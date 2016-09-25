# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 17:02:10 2016

@author: DELL
"""
import sys
sys.path.append('../utils')
from tags2id import PosTag2id
import re
from PhraseRecord import EntRecord
from PhraseRecord import RelRecord


class InfoExtractClass():
    def __init__(self):
        stopW = open('/storage1/wujs/entity/main2/stopwords.txt')
        self.stopW_list = []
        for line in stopW.readlines():
            line = line.strip()
            self.stopW_list.append(line.encode('utf-8'))
    def getRelationPosition(self,rels):
        isRelation = set()
        for key in rels:
            start = key.startIndex 
            end = key.endIndex
            t = range(start,end)
            for itert in t:
                isRelation.add(itert)
        return isRelation
    
    def crftag2id(crfTags):
        crftags = crfTags.split(u' ')
        tags={'B-NP':1,'I-NP':2,'B-VP':3,'I-VP':4,'B-ADVP':5,'I-ADVP','B-PP':6,'B-ADJP':7,'I-ADJP':8}
        tag2id = []
        for tagi in crftags:
            if tagi in tags:
                tag2id.append(tags[tagi])
            else:
                tag2id.append('0')
    def isInRelRange(relRange,ent_start,ent_end):
        flag = False
        for i in range(ent_start,ent_end+1):
            if i in relRange:
                flag=True
        return flag
        
    def is_entity(self,tags,tags_er,sentence,rels):
    
        postag2id = PosTag2id()        
        items = tags_er.split(u' ')
        sentence = sentence.split(u' ')
        tags = tags.split(u' ')
        tags = [postag2id.is_whichPoS(tag_i) for tag_i in tags]
        
        entsub =[]
        relRange = self.getRelationPosition(rels)
        pattern1 = re.compile(r'1')
        iterator  = pattern1.finditer(tag)
        for matchs in iterator:
            if not isInRelRange(relRange,matchs.start(),matchs.end()):
                temp = EntRecord(matchs.start(), matchs.end())
                entsub.append(temp)
            
        pattern2 = re.compile(r'1+')
        iterator  = pattern2.finditer(tag)
        for matchs in iterator:
            if not isInRelRange(relRange,matchs.start(),matchs.end()):
                temp = EntRecord(matchs.start(), matchs.end())
                entsub.append(temp)
        
        for i in range(len(items)):
            item  = items[i]
            if item == 'B-NP' and i not in isRelation:
                ent=[]
                start = i
                end = i + 1
                if i+1 <len(items):
                    tempn = items[i+1]
                    if tempn not in  ['I-NP']:
                        ent.append(tags[i])
                        #print 'ent',ent
                        #print 'ent',sentence[i]
                        temp = EntRecord(start,end,ent)
                        #print ent
                        strsub.append(temp)
                        is_merge.append(False)
                        start = -1
                        end=-1
                else:
                    ent = tags[i]
                    temp = EntRecord(start,end,ent)
                    strsub.append(temp)
                    is_merge.append(False)
                    start = -1
                    end=-1
                        
            if item in ['I-NP'] and i not in isRelation:
                if start ==-1:
                    start = i
                end = i + 1
                if i+1 <len(items):
                    tempn = items[i+1]
                    if tempn not in ['I-NP']:
                        ent = ''.join(tags[start:end])
                        #print ' '.join(sentence[start:end])
                        temp = EntRecord(start,end,ent) 
                        strsub.append(temp)
                        is_merge.append(False)
                        start = -1
                        end=-1       
                else:
                    ent = ''.join(tags[start:end])
                    temp = EntRecord(start,end,ent)
                    strsub.append(temp)
                    #print 'ent',ent
                    is_merge.append(False)
                    start = -1
                    end=-1
        entOrRel = 'ent'
        merge_strsub,flags_1 = self.getLongerEntorRel(sentence,strsub,is_merge,entOrRel)
        new_merge_strsub = self.mergeNearEntOrRel(sentence,merge_strsub,flags_1)      
        return new_merge_strsub
        
    """
    @function: reverbçrelationçsyntactic constraint pattern
    @attention: å
¶ä¸­tagè¡¨ç¤ºçæ¯å¥å­çpos tagçå½¢å¼?    @attention:å©ç¨çä¸¤ä¸ªå½æ°è·entityé½æ¯ä¸æ ·çï¼å¯ä»¥å°è£
èµ·æ¥äºåï¼
    """
    def relation_pattern(self,tag_str,sentence):
        #print sentence
        pos2tag = PosTag2id()
        tags =tag_str.split(u' ')
        tag = ''
        for k in tags:
            tag = tag + pos2tag.is_whichPoS(k)
       # print tag
        sentence  = sentence.split()
        pattern1 = re.compile(r'2+3?6?')
        
        
        #pattern2 = re.compile(r'3?2+7+')
        #pattern2 = re.compile(r'2+7+')
        
        W='[015348]*'
        
        P='[679]+'
        
        pattern2 = re.compile(r'2+'+W+P)
        
        pattern3 = re.compile(r'2+'+W+P+'2+')
        
        #key is substrs, value is the startnode_endnode
        strsub = []
        is_merge=[]
        iterator  = pattern1.finditer(tag)
        for matchs in iterator:
            temp = RelRecord(matchs.start(), matchs.end(), matchs.group(0))
            strsub.append(temp)
            is_merge.append(False)
            #print 'rel1:',sentence[matchs.start():matchs.end()],matchs.start(),matchs.end()
        iterator  = pattern2.finditer(tag)
        for matchs in iterator:
            temp = RelRecord(matchs.start(), matchs.end(), matchs.group(0))
            strsub.append(temp)
            is_merge.append(False)
            #print 'rel2:',sentence[matchs.start():matchs.end()],matchs.start(),matchs.end()
            
        iterator  = pattern3.finditer(tag)
        for matchs in iterator:
            temp = RelRecord(matchs.start(), matchs.end(), matchs.group(0))
            strsub.append(temp)
            is_merge.append(False)
            
        entOrRel = 'rel'
        merge_strsub,flags_1 = self.getLongerEntorRel(sentence,strsub,is_merge,entOrRel)
#        new_merge_strsub = self.mergeNearEntOrRel(sentence,merge_strsub,flags_1)
#        
#        if new_merge_strsub!=None:
#            return new_merge_strsub
#        else:
#            return merge_strsub
        return merge_strsub
       
        
        '''
    @function: å½entity mentionåprhase menstion æ»¡è¶³å¤ä¸ªpatternæ¶ï¼åæé¿ç
    '''
    def getLongerEntorRel(self,sentence,entORrelList,taglsit,entOrRel):
        #sentence = sentence.split()
        strsub = entORrelList
        is_merge = taglsit
        
        merge_strsub=[]
        flags_1=[]
        for i in range(len(strsub)):
            #print 'merge rel',i,'\t',strsub[i],'\t',is_merge[i]
            if not is_merge[i]:
                candidate = strsub[i]
                for j in range(i+1,len(strsub)):
                    if not is_merge[j]:
                        if candidate.isContainedIn(strsub[j]):
                            candidate = strsub[j]
                            is_merge[i] = True
                            is_merge[j] = True
                        elif strsub[j].isContainedIn(candidate):                             
                            is_merge[j] = True
                        else:
                            pass
                start, end = candidate.getIndexes()
                #print 'merged ',entOrRel,':',sentence[int(start):int(end)]
                merge_strsub.append(candidate)
                flags_1.append(False)
        return merge_strsub,flags_1
    """
    @function: to get word's index in the sentence 
    """
    def getIndex(self,word,sentence):
        sentence = sentence.split()
        
        for i in range(len(sentence)):
            if word == sentence[i]:
                return i
    
    def mergeNearEntOrRel(self,sentence,merge_strsub,flags_1):
        new_merge_strsub=[]
        #print 'merge_strsub',merge_strsub
        lent = len(merge_strsub)
        #print 'lent',lent
        if lent>=1:
            new_merge_strsub=[]
            candidate = merge_strsub[0]
            start,end = candidate.getIndexes()
            #print start,end
            if lent>1:
                for i in range(1,lent):
                    temps = merge_strsub[i]
                    t_start,t_end = temps.getIndexes()
                    #print 't_start:',t_start,'\t','t_end:','\t',t_end
                    if end != t_start:
                        if i+1 >= lent:
                            new_merge_strsub.append(temps)
                        new_merge_strsub.append(EntRecord(start,end))
                        start = t_start
                    else:
                        end = t_end
                        if i+1==lent:
                            new_merge_strsub.append(EntRecord(start,end))
                    end = t_end
                    #print 'start:',start,'\t','end:',end
            else:
                new_merge_strsub.append(candidate)
                #new_merge_strsub[candidate] = True
    
        return new_merge_strsub