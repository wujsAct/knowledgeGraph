# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 09:41:55 2016

@author: DELL
"""
import codecs
import json

f1 = codecs.open('../datapro/yelp_academic_dataset_review.json','r','utf-8')
f2 = codecs.open('../datapro/yelp_full_review.txt','w','utf-8')
no = 0
while True:
    chunk = f1.readlines(1000)
    if not chunk:
        break
    for line in chunk:
        line = line.strip()
        obj = json.loads(line)
        reveiews = obj['text']
        reveiews = reveiews.replace('\n','')
        print no
        f2.write(str(no)+'\t'+reveiews+'\n')
        no = no + 1
f2.close()