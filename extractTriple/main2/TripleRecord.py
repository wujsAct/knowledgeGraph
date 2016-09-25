# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 17:04:44 2016

@author: DELL
"""
import numpy as np
import re
class TripleRecord:
    def __init__(self, ent1, rel, ent2, sentence):
        self.ent1 = ent1
        self.rel = rel
        self.ent2 = ent2
        self.score = 0
        slist= sentence
        self.ent1.setContent(slist)
        self.ent2.setContent(slist)
        self.rel.setContent(slist)
        #self.setScore(sentence.strip())
        self.strategy = 'nearArguments'
    '''
    @2016/9/25 to encode extract triples strategy!
    @nearArguments, depenE_conj,depenR_conj,depenR_advcl,depenSubjorObjc_conj
    '''
    def setStrategy(self,strategy):
        self.strategy = strategy
    
    def getStrategy(self):
        return self.strategy
        
    def toString(self):
        if len(self.ent1.getContent()) != 0 and len(self.rel.getContent()) != 0 and len(self.ent2.getContent()) != 0:
          #  return self.ent1.getContent() + '\t' + self.rel.getContent() + '\t' + self.ent2.getContent() + '\t' + str(self.score) + '\n'
            return self.ent1.getContent() + '\t' + self.rel.getContent() + '\t' + self.ent2.getContent() + '\n'
        else:
            return ''