# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 13:52:01 2016
@author: DELL
"""
class PosTag2id():
    #专有名词
    def is_pnoun(self,tag):
        return tag in ['NNP','NNPS']

    #普通名词
    def is_nnoun(self,tag):
        return tag in ['NN','NNS','PRP','PRP$']
    
    #动词 	
    def is_verb(self,tag):
        return tag in ['VB','VBD','VBG','VBN','VBP','VBZ']
    
    #副词
    def is_adverb(self,tag):
        return tag in ['RB','RBR','RBS']
        
    #形容词
    def is_adjective(self,tag):
        return tag in ['JJ','JJR','JJS']
    
    #限定词
    def is_determiner(self,tag):
        return tag in ['DT']
    
    #particle小品词
    def is_particle(self,tag):
        return tag in ['RP']
    
    #介词、从属连词
    def is_prepostion(self,tag):
        return tag in ['IN']
    
    #代词
    def is_pron(self,tag):
        return tag in ['PRP','PRP$']
    
    def is_to(self,tag):
        return tag in ['TO']
    
    def is_toOrpreposition(self,tag):
        return tag in ['IN','TO']
        
    def is_whichPoS(self,tag):
        if self.is_pnoun(tag):
            return '0'
        if self.is_nnoun(tag):
            return '1'
        if self.is_verb(tag):
            return '2'
        if self.is_adverb(tag):
            return '3'
        if self.is_adjective(tag):
            return '4'
        if self.is_determiner(tag):
            return '5'
        if self.is_particle(tag):
            return '6'
        if self.is_prepostion(tag):
            return '7'
        if self.is_pron(tag):
            return '8'
        if self.is_to(tag):
            return '9'
        
        return '-'  