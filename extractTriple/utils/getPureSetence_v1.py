# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 14:33:47 2016

@author: DELL
"""
import sys
import codecs
from tags2id import PosTag2id

if __name__=='__main__':
    dir_path = '../data/food/'
    if len(sys.argv)!=3:
        print 'usage: python py_file input_name output_name'
        exit(1)
    f_input = dir_path+sys.argv[1]
    f_output = dir_path+sys.argv[2]
   
    print 'start to read the text'
    
    tag2id_class = PosTag2id()
    sentence = ''
    tagids = ''
    ner_tags = ''
    f = codecs.open(f_output,'w','utf-8')
    
    with codecs.open(f_input,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            if line !='':
                ent1,tag,er = line.split(u'\t')
                sentence = sentence + ent1 +' '
                tagids = tagids + tag + ' '
                ner_tags = ner_tags + er + ' '
            else:
                new_line = sentence + '\t'+tagids+'\t'+ner_tags
                f.write(new_line+'\n')
                sentence = ''
                tagids = ''
                ner_tags = ''
    f.close()