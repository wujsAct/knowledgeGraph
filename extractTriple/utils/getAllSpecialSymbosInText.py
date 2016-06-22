# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 10:21:06 2016

@author: DELL
"""
import sys
import codecs
from isSymbol import Symbols
import nltk
from spacy.en import English

def getAllSpecialData(symSets,deleteset,symHander,f_input,f_output1,f_output2):
    iters = 0
    for line in codecs.open(f_input,'r','utf-8'):
        iters = iters + 1
        if iters % 1000 == 0:
            print iters
        items = line.split(u'\t')
        ids=items[0]
        context = ' '.join(items[1:])
        context = context.strip()
        for uchar in context:
            if symHander.getSymbols(uchar):
                symSets.add(uchar)
            #this logic has something wrong£¡
            else:
                if symHander.getStrangeWords(uchar) and uchar not in symSets:
                    deleteset.add(uchar)
    print 'start to generate the special data!'
    symSets= ''.join(symSets)
    symSets = symSets.replace(u'\'',u'')
    symSets = symSets.replace(u'.',u'')
    symSets = symSets.replace(u':',u'')
    symSets= set(symSets)
    print symSets
    f = codecs.open(f_output1,'w','utf-8')
    for item in symSets:
        f.write(item+u'\n')
    f.close()
    
    print 'deleteset',deleteset
    f = codecs.open(f_output2,'w','utf-8')
    for item in deleteset:
        f.write(item+u'\n')
    f.close()

#def sentence_split(raw):
#    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')  
#    sents = sent_tokenizer.tokenize(raw)  
#    return  sents
    
def HandlerText_2_sentence(f_name,f_specialTag,f_deltag):
    nlp = English()
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
    
    f_output1 = f_name+'_new_context'
    f1 = codecs.open(f_output1,'w','utf-8')     
    
    iters = 0
    rel_ids = 0
    f_rel_name = f_name + '_new_context_1'
    for line in codecs.open(f_rel_name,'r','utf-8'):
        iters = iters + 1
        if iters % 1000 == 0:
            print iters
        items = line.split(u'\t')
        ids=items[0]
        context = ' '.join(items[1:])
        context = context.strip()
        doc = nlp(context)
        temp_context =''
        for sentence in doc.sents:
            sentence = sentence.text
            if sentence !='':
                lent = len(sentence.split(u' '))
                if lent <=50: #if the lent>50, then dependecy parser tree may have problem
                    temp_context = temp_context + sentence+' '
                    f.write(str(rel_ids)+'\t'+sentence+u'\n')
        temp_context = temp_context.strip()
        if temp_context!='':
            f1.write(str(rel_ids)+'\t'+temp_context+'\n')
            rel_ids = rel_ids+1
    f.close()
    f1.close()
    
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
    print 'stop the non ascii word!'
    f_output = f_name+'_new_context_1'
    f = codecs.open(f_output,'w','utf-8')
    iters = 0
    for line in codecs.open(f_name,'r','utf-8'):
        iters = iters + 1
        if iters % 1000 == 0:
            print iters
        items = line.split(u'\t')
        ids=items[0]
        context = ' '.join(items[1:])
        strs = u''
        context= list(context)
        for i in range(len(context)):
            uchar = context[i]
            if uchar not in delword:
                strs = strs  + uchar
        f.write(ids+'\t'+strs.strip()+'\n')
    f.close()
    

if __name__ == '__main__':
    if len(sys.argv) !=5:
        print 'usage: python pyfile dir_path input_name output_name '
        exit(1)
    dir_path = sys.argv[1]
    f_input = dir_path+'/'+sys.argv[2]
    f_output1 = dir_path + '/intermediate/'+sys.argv[3]
    f_output2 = dir_path + '/intermediate/'+sys.argv[4]
    deleteset = set()
    symHander = Symbols()
    symSets = symHander.sets
    #getAllSpecialData(symSets,deleteset,symHander,f_input,f_output1,f_output2)
    #HandlerText(f_input,f_output1,f_output2)    
    HandlerText_2_sentence(f_input,f_output1,f_output2)
    
    
    