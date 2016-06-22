# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 20:52:58 2016

@author: DELL
"""
import time
import codecs

class generateTriples():
    """
    @function: to get word's index in the sentence 
    """
    def getIndex(self,word,sentence):
        #sentence = sentence.split()
        
        for i in range(len(sentence)):
            if word == sentence[i]:
                return i
    """
    @function: to get stanford dependency parser tree
    """
    def get_dependency_tree(self,sentence,dep_trip,relation_phrase,entity_phrase):
        #sentence = sentence.split(' ')
        #print '------------------------'
        """
        @function: å
å©ç¨dependencyçå
³ç³»å»æ½åç´æ¥çä¸å
ç»å¦ï¼å¯è½æ¾å°é¿çä¾èµå
³ç³»å§ï¼åºè¯¥æ¯æ¯è¾ç²¾åçä¸å
ç»ï¼æè
facts
        è¿ä¸ªäº§ççä¸ä¸å®æ¯ä¸å
ç»å§ï¼?        """
        subtriple={}
        for i in range(len(dep_trip)):
            depenR = dep_trip[i][1]
            extent =None
            extrel = None
            if depenR == 'nsubj':
                subj = dep_trip[i][0][0]
               # print 'subj',subj
                rel = dep_trip[i][2][0]
               # print 'rel',rel
                rel_id = dep_trip[i][2][1]
                ent_id = dep_trip[i][0][1]
                tagrel1 = 0
                tagrel2 = 0
                for key in relation_phrase:
                    rel_range1, rel_range2 = key.getIndexes()
                    
                    if rel_id>=rel_range1 and rel_id <=rel_range2:
                        extrel = sentence[rel_range1:rel_range2]
                        tagrel1 = rel_range1
                        tagrel2 = rel_range2
                        tagrel = key
                
                for key in entity_phrase:
                    ent_range1, ent_range2 = key.getIndexes()
                    
                    if ent_id>=ent_range1 and ent_id <=ent_range2:
                        if ent_id <tagrel1 or ent_id> tagrel2:
                            extent = sentence[ent_range1:ent_range2]
                            tagent = key
            if extent !=None and extrel!=None and ent_id < rel_id:
                subtriple[tagrel] = (tagent,'l')
                #print extent,extrel
               
            extent =None
            extrel = None
            if depenR == 'dobj':
                obj = dep_trip[i][0][0]
                rel = dep_trip[i][2][0]
                rel_id = dep_trip[i][2][1]
                ent_id = dep_trip[i][0][1]
                tagrel1 = 0
                tagrel2 = 0
                tagrel = 0
                for key in relation_phrase:
                    rel_range1, rel_range2 = key.getIndexes()
                    
                    if rel_id>=rel_range1 and rel_id <=rel_range2:
                        extrel = sentence[rel_range1:rel_range2]
                        tagrel1 = rel_range1
                        tagrel2 = rel_range2
                        tagrel = key
                
                tagent = 0
                for key in entity_phrase:
                    ent_range1, ent_range2 = key.getIndexes()                                                                                                                                                                         
                    if ent_id>=ent_range1 and ent_id <=ent_range2:
                        if ent_id < tagrel1 or ent_id> tagrel2:
                            extent = sentence[ent_range1:ent_range2]
                            tagent = key
            
            if extent !=None and extrel!=None:
                subtriple[tagrel] = (tagent,'r')
                #print '1',extrel,extent
        #print 'get_dependency_tree',subtriple
        return subtriple
    """
    @function: ç´æ¥æ ¹æ®æè¿ååå»ä»entity phraseårelation phraseå»äº§çä¸å
ç»
    @note: å ä¸ºæ²¡æèèå°dependency treeçæ
åµï¼æä»¥äº§ççä¸å
ç»æ­£ç¡®çè¯å®å¾ä½çï¼
    """   
    def getReverbTriple(self,sentence,relation_phrase,entity_phrase):
        #sentence = sentence.split()
        ent_flag_dict= {}
        for key in entity_phrase:
            ent_flag_dict[key] = 0
        subtriple={}
        for key in relation_phrase:
            rel_range1, rel_range2 = key.getIndexes()
            rel_phr =  sentence[rel_range1:rel_range2]
            #print 'relation key',rel_phr
            #left argument
            mins_left = 100
            mins_right=100
            flagkey1 = None
            value1 = '0'
            flagkey2 = None
            value2 = '0'
            for key1 in entity_phrase:
                #print 'entity',key1
                ent_range1, ent_range2 = key1.getIndexes()  
                mins_temp =  rel_range1 - ent_range2
                if mins_temp >= 0 and mins_temp < mins_left:
                    mins_left = mins_temp
                    flagkey1 = key1
                    value1 = sentence[ent_range1:ent_range2]
                    ent_flag_dict[key1]=1
                
                mins_temp = ent_range1 - rel_range2
                
                if mins_temp>=0 and mins_temp < mins_right:
                    mins_right = mins_temp
                    flagkey2 = key1
                    value2 = sentence[ent_range1:ent_range2]
                    ent_flag_dict[key1]=1
            #print value1,rel_phr,value2
            #print 'flagkey1',flagkey1
            #print 'flagkey2',flagkey2
            
            if flagkey1 is not None and flagkey2 is not None:
                subtriple[key] = [(flagkey1, flagkey2)]
    
        #pay attention to some entity has no distributed the relation, so we need to distribute them to the relation
        for key in ent_flag_dict:
            if ent_flag_dict[key]==0:
                ent_range1, ent_range2 = key.getIndexes()
                mins_left = 100
                mins_right=100
                flagkey1 = None
                flagkey2 = None
                value1 = '0'
                value2 = '0'
                for key1 in relation_phrase:
                    rel_range1, rel_range2 = key1.getIndexes()
                    rel_phr =  sentence[rel_range1:rel_range2]
                    mins_temp =  rel_range1 - ent_range2
                    if mins_temp >= 0 and mins_temp < mins_left:
                        mins_left = mins_temp
                        flagkey1 = key1
                        value1 = sentence[rel_range1:rel_range2]
                    
                    mins_temp = ent_range1 - rel_range2
                    if mins_temp>=0 and mins_temp < mins_right:
                        mins_right = mins_temp
                        flagkey2 = key1
                        value2 = sentence[rel_range1:rel_range2]
                value_ent = None
                flagkey =None
                if  flagkey1!=None and flagkey2 == None:
                    if subtriple.get(flagkey1)!=None:
                        temp = subtriple[flagkey1]
                        temp =temp[0]
                        value_ent = (key,temp[1])
                        flagkey = flagkey1
                if flagkey2!= None and flagkey1 ==None:
                    if subtriple.get(flagkey2)!=None:
                        temp = subtriple[flagkey2]
                        temp =temp[0]
                        value_ent = (temp[0],key)
                        flagkey = flagkey2
                if flagkey1!=None and flagkey2!=None:
                    if mins_left <mins_right:
                        if subtriple.get(flagkey1)!=None:
                            temp = subtriple[flagkey1]
                            temp =temp[0]
                            value_ent = (key,temp[1])
                            flagkey = flagkey1
                    else:
                        if subtriple.get(flagkey2)!=None:
                            temp = subtriple[flagkey2]
                            temp =temp[0]
                            value_ent = (temp[0],key)
                            flagkey = flagkey2
                if value_ent !=None and flagkey!=None:
                   temp =  subtriple[flagkey]
                   temp.append(value_ent)
                   subtriple[flagkey] = temp
                    
                        
                        
        #print 'getReverbTriple',subtriple
        return subtriple
    ###############################################################
    ##
    ##entity---relation---entity
    ##
    ###############################################################
    def getEntRelationEnt(self,sentence,relation_phrase,entity_phrase,lineNo,tags,stopwords):
#        def getCoreEnt(ent_start,ent_end,tags,sentence):
#            strs = ''
#            tags = tags.split()
#            for i in range(ent_start,ent_end):
#                if tags[i] in ['NN','NNS','PRP','PRP$','NNP','NNPS']:
#                    strs = strs + ' '+sentence[i]
#            strs = strs.strip()
#            return strs
        sentence = sentence.split()
        ent_flag_dict= {}
        for key in entity_phrase:
            ent_flag_dict[key] = 0
        ent_num = len(entity_phrase)
        templist = range(ent_num)
        if ent_num >=2:
            for i in templist[0:ent_num-1:1]:
                key1 = entity_phrase[i]
                ent1_start, ent1_end = key1.getIndexes()
                key2 = entity_phrase[i+1]
                ent2_start, ent2_end = key2.getIndexes()
                #print lineNo,'\t',getCoreEnt(ent1_start,ent1_end,tags,sentence),'\t',' '.join(sentence[ent1_end:ent2_start]),'\t',getCoreEnt(ent2_start,ent2_end,tags,sentence),'\t',1,'\t',' '.join(sentence)
                rel = ''
                if ent2_start != ent1_end:
                    for ir in range(ent1_end,ent2_start):
                        if sentence[ir] not in stopwords:
                            rel = rel + sentence[ir] +' '
                    rel = rel.strip()
                    if len(rel)!=0:
                        print lineNo,'\t',' '.join(sentence[ent1_start:ent1_end]).strip(),'\t',rel.strip(),'\t',' '.join(sentence[ent2_start:ent2_end]).strip(),'\t','1','\t',' '.join(sentence).strip()
                
                
#    def getEntRelationEnt1(self,sentence,relation_phrase,entity_phrase,lineNo,tags):
##        def getCoreEnt(ent_start,ent_end,tags,sentence):
##            strs = ''
##            tags = tags.split()
##            for i in range(ent_start,ent_end):
##                if tags[i] in ['NN','NNS','PRP','PRP$','NNP','NNPS']:
##                    strs = strs + ' '+sentence[i]
##            strs = strs.strip()
##            return strs
#        #read the entity pair in the knowledge graph
#        fentp = codecs.open('/storage1/wujs/entity/main2/entityNamePair.txt','r','utf-8')
#        entPairDict = {}
#        for line in fentp.readlines():
#            line = line.strip()
#            items = line.split('\t')
#            ent1 = items[0];ent2 = items[2]
#            key = ent1+'_'+ent2
#            entPairDict[key] = 1
#        sentence = sentence.split()
#        ent_flag_dict= {}
#        for key in entity_phrase:
#            ent_flag_dict[key] = 0
#        ent_num = len(entity_phrase)
#        templist = range(ent_num)
#        if ent_num >=2:
#            for i in templist:
#                key1 = entity_phrase[i]
#                ent1_start, ent1_end = key1.getIndexes()
#                ent1_name = ' '.join(sentence[ent1_start:ent1_end]).strip().lower()
#                for j in templist:
#                    if i!=j:
#                        key2 = entity_phrase[j]
#                        ent2_start, ent2_end = key2.getIndexes()
#                        ent2_name = ' '.join(sentence[ent2_start:ent2_end]).strip().lower()
#                        key = ent1_name+'_'+ent2_name
#                        if key in entPairDict:
#                        #print lineNo,'\t',getCoreEnt(ent1_start,ent1_end,tags,sentence),'\t',' '.join(sentence[ent1_end:ent2_start]),'\t',getCoreEnt(ent2_start,ent2_end,tags,sentence),'\t',1,'\t',' '.join(sentence)
#                            if ent2_start == ent1_end:
#                                rel = '#'
#                            else:
#                                rel = ' '.join(sentence[ent1_end:ent2_start])
#                            print lineNo,'\t',' '.join(sentence[ent1_start:ent1_end]).strip(),'\t',rel.strip(),'\t',' '.join(sentence[ent2_start:ent2_end]).strip(),'\t','1','\t',' '.join(sentence).strip()
#    
    """
    @function: æ ¹æ®æè¿ååådependency parser treeçç»æï¼ç»¼åæ¥å¾å°ç»æ?    @note: åä¸ä¸ªrelationï¼å½æè¿ååådependency parser treeç»åºçç»æä¸ä¸æ ·çæ¶åï¼æä»¬å°ä½¿ç¨dependencyçç»æ?    """
    def getFinalTriple(self,sentence,dep_trip,relation_phrase,entity_phrase):
        sentence = sentence.split()        
        #start = time.time()
        subtriple1 = self.get_dependency_tree(sentence,dep_trip,relation_phrase,entity_phrase)
        subtriple2 = self.getReverbTriple(sentence,relation_phrase,entity_phrase)
        #end = time.time()
        #print end-start
        
        for key in subtriple1:
            flagr = 0
            if subtriple2.get(key)!=None:
                value1 = subtriple1[key]
                ent = value1[0]
                flag = value1[1]
                
                #print 'flag',flag
                value2 = subtriple2[key]
                value2 =value2[0]
                ent1 = value2[0]
                ent2 = value2[1]
                if flag == 'r':
                    ent2 = ent
                    flagr = 1
                if flag =='l':
                    flagr = 1
                    ent1 = ent
                
                subtriple2[key][0] = (ent1, ent2, flagr)
#        #print '-----------the final triples------------'
#        #print subtriple2
#        triples = []
#        for key in subtriple2:
#            rel = key
#            value = subtriple2[rel]
#            ent1 = value[0]
#            ent2 = value[1]
#            tri = TripleRecord(ent1, rel, ent2, sentence)
#            triples.append(tri)
        return subtriple2
