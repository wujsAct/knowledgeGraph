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
    """
    @function: to recognition the entity pharse
    å­å¨å¾å¤§çæ¼æ´ï¼å°±æ¯åºç°äºamod(adjectival modifier: is any adjectival phrase that serves to modify
    the meaning of the NP,å³å½¢å®¹è¯ä¿®é¥°è¯­ï¼ä¸é¨åçå¨è¯è¿å»æ¶ï¼å¯è½ä¼å

å½å½¢å®¹è¯ï¼
    """
    def is_entity(self,tags,tags_er,sentence,rels):
        #ç´æ¥æ ¹æ®CRF-5.8.0ç»åºçç»ææ¥æ½ååºç­æ¡?
        #pay attention to this problem that, entity mention should has not common with the relation
        postag2id = PosTag2id()        
        items = tags_er.split(u' ')
        sentence = sentence.split(u' ')
        tags = tags.split(u' ')
        tags = [postag2id.is_whichPoS(tag_i) for tag_i in tags]
        strsub = []
        is_merge=[]
        ent_ids = 0
        start = -1
        end = -1
        isRelation = self.getRelationPosition(rels)
        for i in range(len(items)):
            item  = items[i]
            if item == 'B-NP' and i not in isRelation:
                start = i
                end = i + 1
                if i+1 <len(items):
                    tempn = items[i+1]
                    if tempn !='I-NP':
                        ent = tags[i]
                        #print 'ent',ent
                        #print 'ent',sentence[i]
                        temp = EntRecord(start,end,ent)
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
                        
            if item == 'I-NP' and i not in isRelation:
                if start ==-1:
                    start = i
                end = i + 1
                if i+1 <len(items):
                    tempn = items[i+1]
                    if tempn !='I-NP':
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
        #new_merge_strsub = self.mergeNearEntOrRel(sentence,merge_strsub,flags_1)      
        return merge_strsub
        
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
        #åå®å¦æä¸¤ä¸ªå¨è¯æ¾å¨ä¸èµ·çè¯ï¼ç´æ¥é»è®¤çæ¯mergeç?        
        #relationç´æ¥ä½¿ç¨reverbçpatternæ¥ä½¿ç?        
        #pattern1 = re.compile(r'3?2+')
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
            #print 'rel3:',sentence[matchs.start():matchs.end()],matchs.start(),matchs.end()
        #print 'is merge:',is_merge
        #print strsub
        #å¦æä¸ä¸ªå¨è¯å¯ä»¥matchå¤ä¸ªpatternï¼ååé£ä¸ªæé¿çphraseä½ä¸ºæä»¬çrelation phraseï¼?       # merge_strsub = {}
        entOrRel = 'rel'
        merge_strsub,flags_1 = self.getLongerEntorRel(sentence,strsub,is_merge,entOrRel)
        new_merge_strsub = self.mergeNearEntOrRel(sentence,merge_strsub,flags_1)
        
        #return new_merge_strsub
        filter_new_merge_strsub = []
        for k in new_merge_strsub:
            start,end = k.getIndexes()
            #rels= ' '.join(sentence[int(start):int(end)])
            
#            if rels not in self.stopW_list:
#                print 'merge rels:',rels
#                filter_new_merge_strsub.append(k)
            filter_new_merge_strsub.append(k)
        return filter_new_merge_strsub
        
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
    '''
    @function:å½åºç°ç¸é»çentity mentionårelation mentionæ¶ï¼éè¦mergeï¼?    '''
    def mergeNearEntOrRel(self,sentence,merge_strsub,flags_1):
        new_merge_strsub=[]
        lent = len(merge_strsub)
        i = 0
        #ç´æ¥ç¸è¿çä¸¤ä¸ªrelation phrase ç´æ¥mergeèµ·æ¥
        for i in range(lent):
            candidate = merge_strsub[i]
            if not flags_1[i]:
                for j in range(i+1,lent):
                    if not flags_1[j]:
                        if candidate.isAdj2(merge_strsub[j]):
                            flags_1[j] = True
                            candidate = candidate.absorb(merge_strsub[j])
                new_merge_strsub.append(candidate)
                #new_merge_strsub[candidate] = True
        return new_merge_strsub