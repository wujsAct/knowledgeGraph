# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 18:44:54 2016
code from: http://biansutao.iteye.com/blog/326008
@author: DELL
"""
#如何判断新的实体呢？

import gensim,logging
import numpy as np
#model = gensim.models.word2vec.Word2Vec.load_word2vec_format('E:/usersoftware/GoogleNews-vectors-negative300.bin', binary=True)

class detectNovelEnt():
#    #直接用add做compostion，感觉应该靠谱吧！
#    def getVector(self,entity):
#        #组成entity的words都是用空格分隔的呢！
#        words = entity.split(' ')
#        vec = np.zeros((300,),dtype='float32')
#        #此处假设大多数实体的name都可以在Google News中出现了的哈！
#        #此处捕获一个异常，如果有词没在Google News中出现！
#        for word in words:
#            try:
#                temp = model[word]
#                vec = vec + temp
#            except:
#                print 'keyerr!!!'
#        return vec
    
    '''levenshtein distance'''
    def levenshtein(self,first,second):
        if len(first) > len(second):
            first,second = second,first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        max_len = max(first_length,second_length) + 0.0
        #print max_len
        distance_matrix = [range(second_length) for x in range(first_length)] 
        #print distance_matrix
        for i in range(1,first_length):
            for j in range(1,second_length):
                deletion = distance_matrix[i-1][j] + 1
                insertion = distance_matrix[i][j-1] + 1
                substitution = distance_matrix[i-1][j-1]
                if (first[i-1]).lower() != (second[j-1]).lower():
                    substitution += 1
                distance_matrix[i][j] = min(insertion,deletion,substitution)
        #print distance_matrix
        #print distance_matrix[first_length-1][second_length-1]
        return distance_matrix[first_length-1][second_length-1]/max_len
