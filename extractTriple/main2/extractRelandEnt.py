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
        #improved the efficency!!
        relationRange = {x for key in rels for x in xrange(key.startIndex,key.endIndex)}
        
        return relationRange
    
    
    def isInRelRange(self,relRange,ent_start,ent_end):
        flag = False
        t1 = set(range(ent_start,ent_end))
        if len(relRange.intersection(t1)) >0:
            flag = True
        return flag
    #for statistic
    def getLongerEntOrRel(self,sub1,sub2):
        LongerEnt = list(sub1)
        #having some troubles 
        for ent1 in sub1:
            start1,end1 = ent1.getIndexes()
            for ent2 in sub2:
                start2,end2 = ent2.getIndexes()
                if start1 == start2:
                    LongerEnt.remove(ent1)
        LongerEnt += sub2
        return LongerEnt
    
    #attention to different kind of copy!
    def getLongerRelorEnt(self,sub1,sub2,rel2num,sentence,strrels,match_flag):
        #match_flag=1 for entity and match_flag=2 for relation
        LongerEnt = list(sub1)
        sub2c = list(sub2)
        
        #having some troubles
        for rel1 in sub1:
            start1,end1 = rel1.getIndexes()
            for rel2 in sub2:
                start2,end2 = rel2.getIndexes()
                if start1 == start2:
                    strrel = u' '.join(sentence[end1-1:end1+min(match_flag,end2-start2)])
                    rel2str= u' '.join(sentence[start2:end2])
                    temp = strrels.count(strrel)
                    #print 'strrel:',strrel,'times:',temp,'\t','rel2str',rel2str,' nums',rel2num[rel2str]
                    if temp >=2 or rel2num[rel2str]>1:
                        LongerEnt.remove(rel1)
                    else:
                        sub2c.remove(rel2)
            sub2 = list(sub2c)
        LongerEnt += sub2    
        return LongerEnt
        
    def mergeNearEntOrRel(self,sub,flag):
        if flag =='rel':
            record = RelRecord
        else:
            record = EntRecord
        mergeSub = sub
        tag = False
        for i in range(len(sub)):
            subi = sub[i]
            if subi in mergeSub:
                start1,end1 = subi.getIndexes()
                tempmergeSub = list(mergeSub)
                for j in range(len(mergeSub)):
                    subj = mergeSub[j]
                    start2,end2 = subj.getIndexes()
                    
                    if end2 == start1:
                        temprecord = record(start2,end1)
                        if subi in tempmergeSub:
                            tempmergeSub.remove(subi)
                        if subj in tempmergeSub:
                            tempmergeSub.remove(subj)
                        tempmergeSub.append(temprecord)
                        tag = True
                    else:
                        if end1 == start2:
                            temprecord = record(start1,end2)
                            if subi in tempmergeSub:
                                tempmergeSub.remove(subi)
                            if subj in tempmergeSub:
                                tempmergeSub.remove(subj)
                            tempmergeSub.append(temprecord)
                            tag = True
            if tag:
                mergeSub = list(tempmergeSub)
            tag = False
        return mergeSub 
                    
    def extractEntity(self,parameters,flag):
        if flag == 'extract':
            tag = parameters[0]
            sentence = parameters[1]
            rels = parameters[2]
            ent2num = parameters[3]
            strents = parameters[4]
        if flag =='statistic':
            tag = parameters[0]
            sentence = parameters[1]
            rels = parameters[2]
        
        sentence = sentence.split(u' ')
        
        entsub1 =[]
        relRange = self.getRelationPosition(rels)
        pattern1 = re.compile(r'17*')
        iterator  = pattern1.finditer(tag)
        for matchs in iterator:
            if not self.isInRelRange(relRange,matchs.start(),matchs.end()):
                temp = EntRecord(matchs.start(), matchs.end())
                entsub1.append(temp)
                s = matchs.start()
                e = matchs.end()
                #print 'ent 1:',' '.join(sentence[s:e])
        pattern2 = re.compile(r'17*2+7*')
        entsub2 =[]
        iterator  = pattern2.finditer(tag)
        for matchs in iterator:
            if not self.isInRelRange(relRange,matchs.start(),matchs.end()):
                temp = EntRecord(matchs.start(), matchs.end())
                entsub2.append(temp)
                s = matchs.start()
                e = matchs.end() 
                #print 'ent 2:',' '.join(sentence[s:e])
        if flag =='statistic':
            LongerEnt = self.getLongerEntOrRel(entsub1,entsub2)
            mergeEnt = self.mergeNearEntOrRel(LongerEnt,'ent')
            return set(entsub1+entsub2+LongerEnt+mergeEnt)
        if flag == 'extract':
            #LongerEnt = self.getLongerRelorEnt(entsub1,entsub2,ent2num,sentence,strents,1)
            LongerEnt = self.getLongerEntOrRel(entsub1,entsub2)
            mergeEnt = self.mergeNearEntOrRel(LongerEnt,'ent')
            return set(mergeEnt)
            
    def extractRelation(self,parameters,flag):
        #flag: extract or statistic
        if flag == 'extract':
            tag = parameters[0]
            sentence = parameters[1]
            rel2num = parameters[2]
            strrels = parameters[3]
        if flag =='statistic':
            tag = parameters[0]
            sentence = parameters[1]
            
        sentence = sentence.split(u' ')
        pattern1 = re.compile(r'37*')
        pattern2 = re.compile(r'37*[456]+7*')
        #have some conclusion with
        pattern3 = re.compile(r'37*[12456]+7')
        
        
        relsub1 = []
        iterator  = pattern1.finditer(tag)
        for matchs in iterator:
            temp = RelRecord(matchs.start(), matchs.end(), matchs.group(0))
            s = matchs.start()
            e = matchs.end()
            #print 'rel 1:',' '.join(sentence[s:e])
            relsub1.append(temp)
             
        relsub2 = []
        iterator  = pattern2.finditer(tag)
        for matchs in iterator:
            temp = RelRecord(matchs.start(), matchs.end(), matchs.group(0))
            relsub2.append(temp)
            s = matchs.start()
            e = matchs.end()
            #print 'rel 2:',' '.join(sentence[s:e])
        relsub3 = []
        iterator  = pattern3.finditer(tag)
        for matchs in iterator:
            temp = RelRecord(matchs.start(), matchs.end(), matchs.group(0))
            relsub3.append(temp)
            s = matchs.start()
            e = matchs.end()
            #print 'rel 3:',' '.join(sentence[s:e])
        if flag=='statistic':
            LongerRel = self.getLongerEntOrRel(relsub1,relsub2)
            LongerRel = self.getLongerEntOrRel(LongerRel,relsub3)
            mergeRel = self.mergeNearEntOrRel(LongerRel,'rel')
            return set(relsub1+relsub2+relsub3+LongerRel+mergeRel)
        else:
            LongerRel = self.getLongerRelorEnt(relsub1,relsub2,rel2num,sentence,strrels,2)
            LongerRel = self.getLongerRelorEnt(LongerRel,relsub3,rel2num,sentence,strrels,2)
            mergeRel = self.mergeNearEntOrRel(LongerRel,'rel')
            return set(mergeRel)
       
