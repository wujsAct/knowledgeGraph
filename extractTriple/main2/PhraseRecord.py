# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 17:05:38 2016

@author: DELL
"""

import re
class PhraseRecord:
    def __init__(self, start, end, pattern=None):
        self.startIndex = start
        self.endIndex = end
        self.pattern = pattern
        self.content = ''
    
    def getIndexes(self):
        return self.startIndex, self.endIndex
    
    def getPattern(self):
        return self.pattern
    def getContent(self):
        return self.content
        
    def setContent(self,sentence):
        self.content = ' '.join(sentence[self.startIndex:self.endIndex])
        
    def isContainedIn(self, another):
        a_start, a_end = another.getIndexes()
        if self.startIndex >= a_start and self.endIndex <= a_end:
            return True
        else:
            return False     
    def isAdj2(self, latter):
        a_start, a_end = latter.getIndexes()
        if self.endIndex == a_start:
            return True
        else:
            return False
    def absorb(self, latter):
        print "the method will be overwritten by subclass"


class EntRecord(PhraseRecord): 
    def __init__(self, start, end, pattern=None):
        PhraseRecord.__init__(self, start, end, pattern)
    
    def absorb(self, latter):
        a_start, a_end = latter.getIndexes()
        newEnt = EntRecord(self.startIndex, a_end, self.pattern + latter.getPattern())
        return newEnt

    def isNNP(self):
        nnp_pattern = re.compile('[0]+')
        #print 'ent pattern', self.pattern
        if nnp_pattern.match(self.pattern) is not None:
            return True
        else:
            return False

		
class RelRecord(PhraseRecord): 
    def __init__(self, start, end, pattern=None):
        PhraseRecord.__init__(self, start, end, pattern)
    
    def absorb(self, latter):
        a_start, a_end = latter.getIndexes()
        newRel = RelRecord(self.startIndex, a_end, self.pattern + latter.getPattern())
        return newRel

    def isVWP(self):
        W='[015348]*'
        P='[679]+'
        vwp_pattern = re.compile(r'2+'+W+P)
        if vwp_pattern.match(self.pattern) is not None:
            return True
        else:
            return False
            
    def isV(self):
        pattern1 = re.compile(r'2+3?6?')
        #print 'rel pattern', self.pattern
        if pattern1.match(self.pattern) is not None:
            return True
        else:
            return False     