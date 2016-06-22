# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:20:59 2016

@author: DELL
"""
import codecs

class deleteEntStopW():
    def __int__(self):
        f_stopwords = "../main2/stopwords.txt"
        #stop words lists
        self.stopwords= {}
        with codecs.open(f_stopwords,'r','utf-8') as file:
            for line in file:
                line = line.strip()
                line = line.lower()
                self.stopwords[line] = 1
    
    def delStopW(self,ent_items):
        new_ent = ''
        for item in ent_items:
            if self.stopwords.get(item) ==None:
                new_ent = new_ent + item + ' '
        #delete the final ' '
        return new_ent[0:-1]