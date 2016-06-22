# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:03:31 2016

@author: DELL
"""
import codecs


class TypeDict():
    def __init__(self):
        fname='../data/food/moretypes.txt'
        f1=codecs.open(fname,'r','utf-8')
        self.type_num = {}
        for line in f1.readlines():
            line = line.strip()
            typer,num = line.split('\t')
            #delete the topic
            if '/common/topic' not in typer:
                num = int(num)
                self.type_num[typer] = num
        
    def getTypeDict(self):
        newcomerge= self.getCooccur()
        newcomerge = self.coverEnt(newcomerge)
        typeDict = newcomerge
        
        typeDict_map = {}
        '''we need also to split the num >=50 from the large class, so that
        we can get more specific type
        '''
        for key in newcomerge:
            if len(key)>=2:
                pop_type = key[-1]
                print pop_type
                for tkey in key:
                    print 'tkey',tkey
                    if tkey[1]>=50:
                       typeDict_map[tkey[0]] = tkey[0]
                    else:
                        typeDict_map[tkey[0]] = pop_type[0]
            else:
                typeDict_map[key[0][0]] = key[0][0]
                
        return typeDict,typeDict_map
    
    def isInList(self,typeItems,comerge):
        typer1=typeItems[0]
        typer2 = typeItems[1]
        flag1 = None
        flag2 =None
        for i in range(len(comerge)):
            dicts = comerge[i]
            if typer1 in dicts:
                flag1 = i
            if typer2 in dicts:
                flag2 = i
            
        if flag1 ==None and flag2 ==None:
            comerge.append(set(typeItems))
        elif flag1 ==None and flag2 !=None:
            comerge[flag2].add(typer1)
            comerge[flag2].add(typer2)
        elif flag1 !=None and flag2 ==None:
            comerge[flag1].add(typer1)
            comerge[flag1].add(typer2)
        else:
            newcomerge = [set(list(comerge[flag1])+list(comerge[flag2]))]
            for i in range(len(comerge)):
                if i !=flag1 and i !=flag2:
                    newcomerge.append(comerge[i])
            comerge = newcomerge
        
        return comerge
    
    def getCooccur(self,fname='../data/food/food_enthasName_type.txt'):
        f1=codecs.open(fname,'r','utf-8')
        comerge = []
        typeNum = self.type_num
        no = 0
        food_appear=set()
        for line in f1.readlines():
            line = line.strip()
            items = line.split('\t')
            typeItems = set(items[2:])        
            typeItems.discard(u'/common/topic')
            typeItems.discard(u'/book/book_subject')
            typeItems.discard(u'/base/ontologies/ontology_instance')
            newtypeItems = set()
            for seti in typeItems:
                if u'/food' in seti or u'/location' in seti or u'region' in seti or u'/wine/' in seti or '/dining/cuisine' in seti:
                    newtypeItems.add(seti)
    #            if not(u'/base' in seti or u'topic' in seti or u'/m' in seti or u'/user' in seti or u'/biology' in seti or u'/internet' in seti or u'/broadcast' in seti or u'/award' in seti or ):
                
            typeItems = list(newtypeItems)        
            
            lent = len(typeItems)
            
           # print 'lent\t',lent,
            if lent >=2:
                if no ==0:
                    comerge.append(set(typeItems))
                    no = no + 1
                else:
                    for k in range(lent-1):
                        typetwo = typeItems[k:k+2]
                        newt = list(typetwo)
                        tagss =-1
                        if u'/food/food' in newt:
                            tagss = newt.index(u'/food/food')
                        if tagss!=-1:
                            food_appear.add(newt[1-tagss])
                        comerge = self.isInList(typetwo,comerge)
                        no = no + 1
        #print len(comerge)
        newcomerge=[]
        for typeset in comerge:
            total =0
            tempdict = {}
            for typer in list(typeset):
                tempdict[typer] = typeNum[typer]
                total = total + typeNum[typer]
            tempdict_sorted = sorted(tempdict.items(),key=lambda d:d[1])
            newcomerge.append(tempdict_sorted)
            #print tempdict_sorted
        return newcomerge
            
    def coverEnt(self,newcomerge,fname='../data/food/food_enthasName_type.txt'):
        f1=codecs.open(fname,'r','utf-8')
        total = 0
        typeNum = self.type_num
       # newmergetype = set()
        newmergetype = {}
        for line in f1.readlines():
            line = line.strip()
            items = line.split('\t')
            flag =-1
            typeItems = set(items[2:])
            typeItems.discard(u'/common/topic')
            typeItems.discard(u'/book/book_subject')
            typeItems.discard(u'/base/ontologies/ontology_instance')
            newtypeItems = set()
            for seti in typeItems:
                if u'/food' in seti or u'/location' in seti or u'region' in seti or u'/wine/' in seti or '/dining/cuisine' in seti:
                    newtypeItems.add(seti)
            typeItems = list(newtypeItems)   
            for seti in typeItems:
                for mergeitem in newcomerge:
                    for newseti in mergeitem:
                        if seti == newseti[0]:
                            flag = 1
            if flag ==-1:
                total = total + 1
                for seti in typeItems:
                    newmergetype[seti] = typeNum[seti]
        for key in newmergetype:
            temp_dict={}
            temp_dict[key] = newmergetype[key]
            newcomerge.append(temp_dict.items())
        #newcomerge_sorted = sorted(newcomerge.items(),key=lambda d:d[1])
#        print total
#        print len(newcomerge)
#        no = 1
#        for key in newcomerge:
#            print no,key
#            no = no + 1
        return newcomerge

    def filterEnthasName(self,newcomerge,fname='../data/food/food_enthasName_type.txt'):
        f1=codecs.open(fname,'r','utf-8')
        f2 = codecs.open(fname+u'_new','w','utf-8')
        total = 0
       # newmergetype = set()
        for line in f1.readlines():
            line = line.strip()
            items = line.split('\t')
            flag =-1
            typeItems = set(items[2:])
            typeItems.discard(u'/common/topic')
            typeItems.discard(u'/book/book_subject')
            typeItems.discard(u'/base/ontologies/ontology_instance')
            newtypeItems = set()
            for seti in typeItems:
                if u'/food' in seti or u'/location' in seti or u'region' in seti or u'/wine/' in seti or '/dining/cuisine' in seti:
                    newtypeItems.add(seti)
            typeItems = list(newtypeItems)   
            for seti in typeItems:
                for mergeitem in newcomerge:
                    for newseti in mergeitem:
                        if seti == newseti[0]:
                            flag = 1
            if flag ==-1:
                total = total + 1
                print line
            else:
                f2.write(line+'\n')
        print 'missing popular type num is',total
                      
typeDictClass = TypeDict()
typeDict,typeDict_map = typeDictClass.getTypeDict()
#no = 1
#for key in typeDict:
#    print no,'\t',key
#    no = no + 1
#typeDictClass.filterEnthasName(typeDict)
print typeDict_map
