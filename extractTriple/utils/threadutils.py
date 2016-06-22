# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 09:23:20 2016

@author: DELL
"""

from  multiprocessing import Pool
import os,sys

def add_time(data):
        if data:
            result=[]
            data = data.split()
            result = data[0]
            return result

def completedCallback(data):
    sys.stdout.write(str(data)+"\n")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >>sys.stderr, 'Usage: sys.argv[0] filename'
        sys.exit(1)
    print("processid = %s" % os.getpid())
    pool = Pool()
    filename = sys.argv[1]
    try:
        with open(filename) as file:
            for line in file:
                pool.apply_async(add_time,(line,), callback = completedCallback)
            pool.close()
            pool.join()
    except KeyboardInterrupt:
        print 'control-c presd butan'
        pool.terminate()