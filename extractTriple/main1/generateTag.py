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
#    def getIndex(self,word,sentence):
#        sentence = sentence.split(u' ')  
#        for i in range(len(sentence)):
#            if word == sentence[i]:
#                return i
                
    def getPosTags(self,sentence,nlp):
        #abandon the standford NLP
#        tagger = PosTagger(sentence)
#        tags = tagger.tags_result
#        if tags !=None:
#            return tags
#        else:
#            return None
        #Now we utilize the Spacy
        sentence = sentence.strip()
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
            
#    def getDependency(self,sentence):
#        try:
#            dep_parser = dependencyParser()
#            dependency_parser = dep_parser.dependency_parser
#            depresult = dependency_parser.raw_parse(sentence)
#            dep = depresult.next()
#        except:
#            dep =None
#                        
#        if dep !=None:
#            if dep.triples() !=None:
#                return dep.triples()
#            else:
#                return None
#        else:
#            return None
#    
#    def getMergeTags(self,tags,dep_triples,sentence):
#        #pOS Tag不能够完全准确吧！需要用依赖树在一次精确一下relation_phrase
#        tags_dep = {}
#        dep_trip = []
#        newtags =[]
#        #时并不能给出编号呢！
#        if dep_triples !=None:
#            for i in list(dep_triples):
#                dep_trip.append(i)
#                word1 = i[0][0]
#                ids1 = self.getIndex(word1,sentence)
#                wtag1 = i[0][1]
#                tags_dep[ids1]= wtag1
#                    
#                word2 = i[2][0]
#                ids2 = self.getIndex(word2,sentence)
#                wtag2 = i[2][1]
#                tags_dep[ids2]= wtag2
#                
#        posTag2id = PosTag2id()
#        for ient in tags:
#            print ient
#            ent_id = self.getIndex(ient[0],sentence)
#            if tags_dep.get(ent_id) !=None:
#                if ient[1] != tags_dep.get(ent_id) and (posTag2id.is_noun(ient[1]) or posTag2id.is_verb(ient[1])):
#                    strtags = strtags + posTag2id.is_whichPoS(tags_dep.get(ent_id))                    
#                    newient=()
#                    newient=(ient[0],tags_dep.get(ent_id))
#                    newtags.append(newient)
#                else:
#                    strtags = strtags+posTag2id.is_whichPoS(ient[1])
#                    newtags.append(ient)
#            else:
#                newtags.append(ient)
#                strtags = strtags+posTag2id.is_whichPoS(ient[1])
#        print newtags       
#        print out result
#        if len(newtags)!=0:
#            return newtags,strtags
#            return newtags
#        else:
#            return 'None'
    
def pro_sen(gen,line,nlp):
    #print line
    lineNo,sentence = line.split(u'\t')
    #lent = len(sentence.split(u' '))
 #   if sentence !='' and lent<50:
    retValue = []
    retValue.append(lineNo)
    if sentence!='':
        tags = gen.getPosTags(sentence,nlp)
   #     print 'tags',tags
        if tags!=None:
            retValue.append(tags)
   # print 'len retValue',len(retValue)
    if len(retValue)==2:
        return retValue
    else:
        return None
    
#    if sentence!='':
#        if tag==u'0':
#            tags = gen.getPosTags(sentence)
#            dep_triples = gen.getDependency(sentence)
#            newtags = gen.getMergeTags(tags,dep_triples,sentence)
#            
#            if newtags!=None:
#                retValue.append(newtags)
#                return retValue
#            else:
#                return None
#        if tag==u'1':
#            tags = gen.getPosTags(sentence)
#            if tags!=None:
#                retValue.append(tags)
#                return retValue
#            else:
#                return None
#        return None
#    else:
#        return None
def completedCallback1(data):
   # print 'data',data
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
    #f_output = dir_path+'/'+sys.argv[3]
    gen = generateTag()
    #pool = Pool(3)
    nlp = English()
    iters = 1
    try:
        with codecs.open(f_input,'r','utf-8') as file:
            for line in file:
              #  print line
                data = pro_sen(gen,line,nlp)
                completedCallback1(data)
#                pool.apply_async(pro_sen,(gen,line,nlp,), callback = completedCallback)
#            pool.close()
#            pool.join()
    except KeyboardInterrupt:
        print 'control-c presd butan'
        #pool.terminate()

        