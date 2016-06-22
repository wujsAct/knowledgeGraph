# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 21:26:54 2016

@author: DELL
"""
import string


class Symbols():
    def __init__(self):
        t = string.punctuation
        self.sets = set(t)
        
    def is_chinese(self,uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False
 
    def is_number(self,uchar):
        if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True
        else:
            return False
  
    def is_alphabet(self,uchar):
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False
 
    def is_other(self,uchar):
        if not (self.is_chinese(uchar) or self.is_number(uchar) or self.is_alphabet(uchar)):
            return True
        else:
            return False
    
    def getSymbols(self,uchar):
        if uchar in self.sets:
            return True
        else:
            if self.is_other(uchar) and uchar > u'\u024F':
                return True
            else:
                return False
    def getStrangeWords(self,uchar):
        if self.is_other(uchar) and uchar < u'\u024F':
            return True
        else:
            return False
            