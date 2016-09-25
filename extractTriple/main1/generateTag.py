# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 16:03:18 2016

@author: DELL
"""
'''
@Input: txt file
@output: tag information
@function: 获取文件的tag信息
'''
import sys
import codecs
from  multiprocessing import Pool
sys.path.append('../utils')
from spacy.en import English
#from getTaggerOrDepenParser import dependencyParser
#from getTaggerOrDepenParser import PosTagger
from tags2id import PosTag2id
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class generateTag():
    """
    @function: to get word's index in the sentence 
    """
                
    def getPosTags(self,sentence,nlp):
        #Now we utilize the Spacy
        sentence = sentence.strip()
        new_sentence = []
        doc = nlp(sentence)
        tags = []
        for token in doc:
            if 'SP' != token.tag_:
                temp =[]
                temp.append(token)
                temp.append(token.tag_)
                tags.append(temp)
        if len(tags)>0:
            return tags
        else:
            return None
def pro_sen(gen,line,nlp):
    lineNo,sentence = line.split(u'\t')
    retValue = []
    retValue.append(lineNo)
    if sentence!='':
        tags = gen.getPosTags(sentence,nlp)
        if tags!=None:
            retValue.append(tags)
    if len(retValue)==2:
        return retValue
    else:
        return None
    
def completedCallback1(data):
    try:
        if data!=None:
            lineNo = data[0]
            tags = data[1]
            if tags!=None:
                sys.stdout.write(lineNo+'\n')
                for k in tags:
                    sys.stdout.write(str(k[0])+'\t'+k[1]+'\n')
                sys.stdout.write('\n')
    except:
        #print data
        exit(-1)

#sentence =u'''
#But then , he told me , he realized his 6: 20 client's real problem was not the traders themselves;
#'''entrée

if __name__ == '__main__':
    if len(sys.argv) !=3:
        print 'usage: python pyfile dir_path input_name'
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+'/'+sys.argv[2]
    gen = generateTag()
    nlp = English()
    iters = 1
    try:
        with codecs.open(f_input,'r','utf-8') as file:
            for line in file:
                data = pro_sen(gen,line,nlp)
                completedCallback1(data)               
    except KeyboardInterrupt:
        print 'control-c presd butan'
        