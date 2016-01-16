# -*- coding:utf-8 -*-

from lucene import *
from thread import*
import vm
def readin(s):
    f=open(s,'r')
    readin=f.read()
    f.close()
    return readin
def writedwn(s,path):
    res=open(path,'w')
    res.write(s)
    res.close()

