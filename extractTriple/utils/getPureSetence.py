# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 14:33:47 2016

@author: DELL
"""
import sys
import codecs
from tags2id import PosTag2id

def getSentence2ContextId(fname):
    sen2conId = []
    f =  codecs.open(fname,'r','utf-8')
    while(1):
        lines = f.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            if line !='':
                items = line.split(u'\t')
                if len(items)==1:
                    sen2conId.append(items[0])
    return sen2conId

if __name__=='__main__':
    
    if len(sys.argv)!=5:
        print 'usage: python py_file dir_path w2tag.txt input_name output_name'
        exit(1)
    dir_path =sys.argv[1]+'/'
    w2tag = dir_path+sys.argv[2]
    f_input = dir_path+sys.argv[3]
    f_output = dir_path+sys.argv[4]
   
    print 'start to read the text'
    
    tag2id_class = PosTag2id()
    sentence = ''
    tagids = ''
    ner_tags = ''
    f = codecs.open(f_output,'w','utf-8')
    print 'go into the get the id'
    sen2conId = getSentence2ContextId(w2tag)
    line_id = 0
    f1 = codecs.open(f_input,'r','utf-8')
    while(1):
        lines = f1.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            if line !='':
                items = line.split(u'\t')
                if len(items)==3:
                    ent1 = items[0]
                    tag = items[1]
                    er = items[2] 
                    sentence = sentence + ent1 +' '
                    tagids = tagids + tag + ' '
                    ner_tags = ner_tags + er + ' '
            else:
                new_line = sentence + '\t'+tagids+'\t'+ner_tags
                f.write(sen2conId[line_id]+'\t'+new_line+'\n')
                line_id = line_id + 1
                print line_id
                sentence = ''
                tagids = ''
                ner_tags = ''
    f.close()