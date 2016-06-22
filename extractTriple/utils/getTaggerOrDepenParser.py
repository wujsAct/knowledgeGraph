# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 13:55:21 2016

@author: DELL
"""

import os
from nltk.parse import stanford
import nltk

"""
@function: to get the dependecy parser and pos tagger
"""
class dependencyParser():
    #Stanford Dependency Parser
    def __init__(self):   
        os.environ['STANFORD_PARSER'] = '/storage1/wujs/entity/stanford-parser-full-2015-04-20/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = '/storage1/wujs/entity/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'
        
        dependency_parser = stanford.StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        self.dependency_parser = dependency_parser

#没有办法解决戴帽子的英文字符的tag工具，因此不用这个！
#class PosTagger():
#    def __init__(self):
#        #Standord POS-tag
#        stanford_pos_dir="E:/usersoftware/stanford-postagger-full-2015-04-20/"        
#        eng_model_filename=stanford_pos_dir+'models/wsj-0-18-left3words-distsim.tagger'
#        my_path_to_jar = stanford_pos_dir+'stanford-postagger.jar'
#        pos_tagger = StanfordPOSTagger(model_filename=eng_model_filename,path_to_jar=my_path_to_jar,encoding='utf8')
#        self.pos_tagger = pos_tagger
#
#text = nltk.word_tokenize('text')
#nltk.pos_tag(text)
class PosTagger():
    def __init__(self,sentence):
        tokens = nltk.word_tokenize(sentence)
        self.tags_result = nltk.pos_tag(tokens)
        #print self.tags_result
