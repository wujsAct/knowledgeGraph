# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 16:21:20 2016

@author: DELL
"""

'''
In this function, we will filter the known triple(left argument or right argument can be
mappped into the knowledge).
'''
import numpy as np
import codecs
#import gensim
from  multiprocessing import Pool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from LeveDist import detectNovelEnt
#from numpy import linalg as LA
#
#def getVecDist(model,et,key):
#    flag1 =1
#    try:
#        et1 = et[0].lower()+et[1:-1]
#        et_vec1 = model[et1]
#    except:
#        try:
#            et2 = et1[0].upper()+et1[1:-1]
#            et_vec1 = model[et2]
#        except:
#            flag1 =0
#            
#    flag2=1
#    try:
#        et1 = key[0].lower()+key[1:-1]
#        et_vec1 = model[et1]
#    except:
#        try:
#            et2 = key[0].upper()+key[1:-1]
#            et_vec1 = model[et2]
#        except:
#            flag2 =0
#    
#    if flag1==1 and flag2==1:
#        vecDist = LA.norm(et_vec1-et_vec1)
#        return vecDist
#    else:
#        return float("inf")
#        
#def getLevDistance(model,dt,ent_name_map,ent):
#    for key in ent_name_map:
#        dist = dt.levenshtein(ent,key)
#        if dist <=0.1:
#            return 1,key
#    return 0,None

def delStopW(ent_name_map,stopwords,ent_items):
    new_ent = ''
    for item in ent_items:
        if stopwords.get(item) ==None:
            new_ent = new_ent + item + ' '
    #delete the final ' '
    return new_ent[0:-1]
             
       
def pro_sen(stopwords,ent_name_map,line):
    line = line.strip()
    items= line.split('\t')
    
    flag  = 0
    lflag = 0
    rflag = 0
    if len(items)>=6:
        ent1 = items[1]
        ent2 = items[3]
        ent1 = ent1.lower()
        ent1_items = ent1.strip().split(' ')
        #if the ent_items can totally match, we will not detelet the stopwords
        temp_str = ''
        if stopwords.get(ent1) ==None:
            if ent_name_map.get(ent1) !=None:
                flag = 1
                lflag = 1
                temp_str = '\t' + 'left\t'+ent1.lower()
            else:
                newent1 = delStopW(ent_name_map,stopwords,ent1_items)
                
                if ent_name_map.get(newent1) !=None:
                    flag = 1
                    lflag = 1
                    temp_str = '\t' + 'left\t'+newent1
            if lflag==0:
                temp_str = '\t'+'left\t'+ent1.lower()
        ent2 = ent2.strip().lower()
        ent2_items = ent2.split(' ')
        if stopwords.get(ent2) ==None:
            if ent_name_map.get(ent2)!=None:
                flag = 1
                rflag = 1
                temp_str = temp_str + '\t' + 'right\t'+ent2
            else:
                newent2= delStopW(ent_name_map,stopwords,ent2_items)
                if ent_name_map.get(newent2) !=None:
                    flag = 1
                    rflag =1
                    temp_str =temp_str+ '\t' + 'right\t'+newent2
            if rflag ==0:
                temp_str = temp_str+'\t'+'right\t'+ent2
            
#    #has one entity in the freebase
#    if flag ==1:
#        return line + temp_str
#    else:
#        return None
        if rflag==1 and lflag==1:
            return line + temp_str
        else:
            return None

def completedCallback(data):
    if data!=None:
        sys.stdout.write(data+'\n')

if __name__=="__main__":
    if len(sys.argv) !=4:
        print 'usage: python pyfile dir_path ent_has_namef extract_triple.txt'
        exit(1)
    dir_path = sys.argv[1]
    input_name = sys.argv[2]
    f_entHasName = dir_path + input_name
    #f_ent2vec = "../data/food/food_ent2vec.txt"
    f_stopwords = "../data/stopwords.txt"
    #model = gensim.models.word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    f_ent2no = {}
    ent_name_map = {}
    #ent_name_vec = np.loadtxt(f_ent2vec)
    no = 0
    with codecs.open(f_entHasName,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            items = line.split('\t')
            pid = items[0]
            name = items[1]
            types = ''
            for i in range(2,len(items)):
                types = types + items[i]+'\t'
            name = name.lower()
            ent_name_map[name] = types
            f_ent2no[name] =no
            no = no + 1
    #print ent_name_map.get('rice')
    
    #stop words lists
    stopwords= {}
    with codecs.open(f_stopwords,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            line = line.lower()
            stopwords[line] = 1
    #print stopwords.get('rice')
    
    #dt = detectNovelEnt() 
    f_triple = dir_path+sys.argv[3]
    total = 0
    with open(f_triple,'r') as file:
        for line in file:
            #print line
            data = pro_sen(stopwords,ent_name_map,line)
            if data!=None:
                sys.stdout.write(data+'\n')
