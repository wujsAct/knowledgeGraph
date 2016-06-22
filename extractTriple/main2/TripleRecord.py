# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 17:04:44 2016

@author: DELL
"""
import numpy as np
import re
class TripleRecord:
    def __init__(self, ent1, rel, ent2, sentence,tags):
        self.ent1 = ent1
        self.rel = rel
        self.ent2 = ent2
        self.tags = tags
        self.score = 0
        slist = sentence.strip().split()
        self.ent1.setContent(slist)
        self.ent2.setContent(slist)
        self.rel.setContent(slist)
        #self.setScore(sentence.strip())
    
    def getFeature(self,sentence):
        
        feature = np.zeros((1,19),dtype='int')
        
        if self.rel.isVWP():
            feature[0,0]=1
        if self.ent1.isNNP():
            feature[0,1]=1
        if self.ent2.isNNP():
            feature[0,2]=1
        if sentence.startswith(self.ent1.getContent()):
            feature[0,3]=1
        str1 = self.ent1.getContent()
        t1 = str1.split(' ')
        str2 = self.ent2.getContent()
        t2 = str2.split(' ')
        t3 = sentence.split(' ')
#        if len(t1)+len(t2) == len(t3):
#            feature[0,4]=1
        if len(t3)<=10:
            feature[0,4]=1
        if len(t3)>10 and len(t3)<=20:
            feature[0,5]=1
        if len(t3)>20:
            feature[0,6] =1
        if self.rel.isV():
            feature[0,7]=1
            
        sentence = sentence.strip().split(' ')
        tags = self.tags
        tags = tags.strip()
        tags = tags.split(' ')
        #the right of y exist NP
        temp = self.ent2.endIndex
        for i in range(temp-1,len(tags)):
            t= tags[i]
            if t in ['NNP','NNPS','NN','NNS','PRP','PRP$']:
                feature[0,8] = 1
        
        #relation's feature
        rel = self.rel
        start = rel.startIndex
        end = rel.endIndex
        if tags[end-1] in ['IN','TO']:
            rel_last_pre = sentence[end-1]
            if rel_last_pre == 'for':
                feature[0,9] = 1
            if rel_last_pre =='on':
                feature[0,10] = 1
            if rel_last_pre == 'of':
                feature[0,11] = 1
            if rel_last_pre == 'to':
                feature[0,12] = 1
            if rel_last_pre == 'in':
                feature[0,13] = 1
        pattern = re.compile(r'wh.+')
        for i in range(0,start):
            t = sentence[i]
            ttag = tags[i]
            strs = t.lower()
            match = pattern.match(strs)
            if match!=None:
                feature[0,16] =1
            if ttag in ['CC']:
                feature[0,17] = 1
        temp = self.ent1.startIndex
        for i in range(0,temp):
            t = tags[i]
            if t in ['NNP','NNPS','NN','NNS','PRP','PRP$']:
                feature[0,14] = 1
            if t in ['IN']:
                feature[0,15] = 1
        return feature
        
            
#    def setScore(self, sentence):
#        if self.rel.isVWP():
#            self.score = self.score + 0.34
#        if self.ent1.isNNP():
#            self.score = self.score + 0.12
#        if self.ent2.isNNP():
#            self.score = self.score + 0.12
#        if sentence.startswith(self.ent1.getContent()):
#            self.score = self.score + 0.2
#        str1 = self.ent1.getContent()
#        t1 = str1.split(' ')
#        str2 = self.ent2.getContent()
#        t2 = str2.split(' ')
#        t3 = sentence.split(' ')
#        if len(t1)+len(t2) == len(t3):
#            self.score = self.score + 0.36
#        if len(t3)<=10:
#            self.score = self.score + 0.3
#        if len(t3)>10 and len(t3)<=20:
#            self.score = self.score + 0.16
#        if self.rel.isV():
#            self.score = self.score-0.3
#        
#    def getScore(self):
#        return self.score

    def toString(self):
        if len(self.ent1.getContent()) != 0 and len(self.rel.getContent()) != 0 and len(self.ent2.getContent()) != 0:
          #  return self.ent1.getContent() + '\t' + self.rel.getContent() + '\t' + self.ent2.getContent() + '\t' + str(self.score) + '\n'
            return self.ent1.getContent() + '\t' + self.rel.getContent() + '\t' + self.ent2.getContent() + '\n'
        else:
            return ''