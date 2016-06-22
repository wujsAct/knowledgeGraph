# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 10:21:06 2016

@author: DELL
"""
import sys
import codecs
from isSymbol import Symbols
import nltk
"""
获取文档中所有的特殊符号
"""
def getAllSpecialData(symSets,deleteset,symHander,f_input,f_output1,f_output2):
    iters = 0
    for line in codecs.open(f_input,'r','utf-8'):
        iters = iters + 1
        print iters
        ids,context = line.split(u'\t')
        context = context.strip()
        for uchar in context:
            if symHander.getSymbols(uchar):
                symSets.add(uchar)
            if symHander.getStrangeWords(uchar) and uchar!=u"'" and uchar not in symSets:
                deleteset.add(uchar)
    f = codecs.open(f_output1,'w','utf-8')
    for item in symSets:
        f.write(item+u'\n')
    f.close()
    
    f = codecs.open(f_output2,'w','utf-8')
    for item in deleteset:
        f.write(item+u'\n')
    f.close()

#直接用库来切割效率更加高一些，不要什么代码都自己写，不然会累死
def sentence_split(raw):#分割成句子  
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')  
    sents = sent_tokenizer.tokenize(raw)  
    return  sents
"""
将特殊符号的左右两边都加上空格符
"""
def HandlerText(f_name,f_specialTag,f_deltag):
    symbolset = []
    spe_f = codecs.open(f_specialTag,'r','utf-8')
    for line in spe_f.readlines():
        line = line.strip()
        symbolset.append(line)
    
    delf = codecs.open(f_deltag,'r','utf-8')
    delword = set()
    for line in delf.readlines():
        line = line.strip()
        delword.add(line)
    

    
    f_output = f_name+'_new'
    f = codecs.open(f_output,'w','utf-8')
    iters = 0
    for line in codecs.open(f_name,'r','utf-8'):
        iters = iters + 1
        print iters
        ids,context = line.split(u'\t')
        context = context.strip()
        sentences = sentence_split(context)
        for sentence in sentences:
                #由于句子可能存在很多的不确定性，因此我们需要去捕获很多异常吧！
                if sentence !='':
                    sentence = sentence[0:-1]
                    strs = u''
                    tag =u'0'
                    for uchar in sentence:
                        if uchar in symbolset:
                            strs = strs + u' '+uchar+u' '
                        else:
                            if uchar in delword:
                                tag = u'1'
                            strs = strs + uchar
                    f.write(tag+'\t'+strs+u'\n')
    f.close()   
        
    

if __name__ == '__main__':
    if len(sys.argv) !=5:
        print 'usage: python input_name output_name'
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+"/"+sys.argv[2]
    f_output1 = dir_path + '/intermediate/'+sys.argv[3]
    f_output2 = dir_path + '/intermediate/'+sys.argv[4]
    deleteset = set()
    symHander = Symbols()
    symSets = symHander.sets
    #getAllSpecialData(symSets,deleteset,symHander,f_input,f_output1,f_output2)
    HandlerText(f_input,f_output1,f_output2)
    
    
    