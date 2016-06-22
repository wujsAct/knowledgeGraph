# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 15:44:56 2016

@author: DELL
"""

__author__ = 'wujs'
#!/usr/bin/python
import json
import urllib
import codecs

class FreebaseAPI():
    def __init__(self):
        print 'go into....'
        self.api_key = 'AIzaSyBUmPsISQrS8C0jUzFoS1NGFmTl9AW0E70'
        self.service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    '''
    how to get the description:
    freebase topic api:
    https://www.googleapis.com/freebase/v1/topic/m/07q37w?filter=/common/topic/description
    '''
    def getTypes(self,nodes):
        query = [{
            'id': None,
            'name':nodes,
            'type':[]
        }]
        
        params = {
                'query': json.dumps(query),
                'key': self.api_key
            }
        url = self.service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
        try:
            result = response['result']
            
            jsonres =  result[0]
            names = 'None'
            types ='None'
            if jsonres.get('name') !=None:
                names = jsonres['name']
            if jsonres.get('type') !=None:
                types = jsonres['type']
            strs = names+'\t'+'\t'.join(types)
            print strs
            return strs
        except:
            print 'error get the result'
            return 'None'+'\t'+'None'