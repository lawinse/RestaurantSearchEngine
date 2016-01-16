# -*- coding:utf-8 -*-
#!/usr/bin/env python
from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File, \
    VERSION, initVM, Version, WhitespaceAnalyzer,NumericRangeQuery ,BooleanQuery,BooleanClause
import jieba,re
import mapp
import kind_fliter

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def sort_distnce(num):
    res = ""
    if (num == 0):
        return '-'
    if num > 0 and num <= 50:
        tmp = int(num)
        res = ( str(tmp) + '米内').decode('utf8')
    elif num > 50 and num <= 1000:
        tmp = int(num/10)*10
        res = ('约' + str(tmp) + '米').decode('utf8')
    else:
        tmp = int(num/100)
        tmp = float(tmp) / 10
        res = ('约' + str(tmp) + '公里').decode('utf8')
    return res

def radarsort(shops,like):
    A = 0.5
    for shop in shops:
        dis = 2.718281828**(-(shop[16]/4000))
        match = shop[17]
        star = float(eval(shop[5]))/5
        try:
            weight = like[shop[3]]
            print 123456789,weight
            shop.append(dis*match+match*star+star*dis+A*weight)
        except:
            shop.append(dis*match+match*star+star*dis)


def BM25(string,length):
    tf_mode = re.compile('fieldWeight.*?of:([\s\S]*?)= tf',re.I)
    idf_mode = re.compile('termFreq.*?[\s\S](.*?)= idf',re.I)

    tfd_li = tf_mode.findall(string)

    idf_li = idf_mode.findall(string)
    wei = 0.0
    for i in range(len(tfd_li)):
        tfd = eval(tfd_li[i].strip())
        idf = eval(idf_li[i].strip())
        b = 0.75
        k1 = 1.2
        lave = 119.46
        ld = length
        temp = (k1*(1-b+b*ld/lave)+tfd)
        wei += idf*(k1+1)*tfd/temp
    return wei

def normalize(a):
    maxx = 0
    for s in a:
        maxx = max(maxx,s[17])
    if maxx!=0:
        for s in a:
            s[17] = s[17]/maxx

def analy(a):
    tmp = []
    if (a[0]==''):
        tmp.append('')
    else:
        try:
            gg = mapp.get_cdnt(a[0].decode('utf8'),u'\u4e0a\u6d77')
            haha = gg[0]+gg[1]
            tmp.append(gg)
        except:
            tmp.append('')
    tmp.append(a[1])
    tmp.append(a[2])
    tmp.append(a[3])
    return tmp

def re_order(res,item):
    l = sorted(res,key = lambda x:x[item])
    ll = len(l)
    newl = []
    for i in xrange(ll-1,-1,-1):
        newl.append(l[i])
    return newl

def re_order_for_price(res):
    newl = []
    for item in res:
        if item[18] != -1:
            newl.append(item)
    return re_order(newl,18)


def evaluate(a,b,c,d):
    return 2.718281828**(-(a/6930)) + b + float(c)/5 + d

def sort(scoreDocs,query,searcher,loc,pr,li,come):
    quchong = []
    tmpresult = []
    num = 1
    for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            a = searcher.explain(query,scoreDoc.doc)
            #print str(a).decode('utf8')
            x = float(doc.get('exactx'))
            y = float(doc.get('exacty'))
            #print '<',num,'>',doc.get('name'),doc.get('search')
            #print 'distance is ',mapp.get_distance((x,y),(target[0],target[1]))
            if (doc.get('no') in quchong):
                continue
            quchong.append(doc.get('no'))
            tmp = []
            tmp.append(doc.get('url'))
            tmp.append(doc.get('name'))
            tmp.append(doc.get('picture'))
            tmp.append(doc.get('kind'))
            tmp.append(doc.get('address'))
            tmp.append(doc.get('star'))
            tmp.append(doc.get('map'))
            if (len(doc.get('cmt'))>45):
                cmt = doc.get('cmt')[:45] + '...'
                tmp.append(cmt)
            else:
                tmp.append(doc.get('cmt'))
            tmp.append(doc.get('phone'))
            tmp.append(doc.get('tag'))
            tmp.append(doc.get('recipe'))
            tmp.append(doc.get('merit'))
            tmp.append(doc.get('no'))
            tmp.append(doc.get('shop'))
            if(eval(doc.get('price'))<0):
                tmp.append('-')
            else:
                tmp.append(str(doc.get('price')))
            tmp.append(doc.get('length'))                   #15
            if(loc):
                tmp.append(mapp.get_distance((x,y),(target[0],target[1])))          #16
            else:
                tmp.append(0)                                                    #16
            if(come[1]):
                tmp.append(BM25(unicode(a),eval(tmp[15])))      #17
            else:
                tmp.append(0)
            tmp.append(eval(doc.get('price')))                #18
            tmp.append(sort_distnce(tmp[16]))
            tmpresult.append(tmp)
    normalize(tmpresult)
    '''for r in tmpresult:
            like = 0
            r.append(evaluate(r[16],r[17],eval(r[5]),like))
        #print tmpresult'''
    radarsort(tmpresult,like)
    tmpresult = re_order(tmpresult,-1)
    if len(tmpresult)>100:
        tmpresult = tmpresult[:100]
    if(pr==2):
        result = re_order_for_price(tmpresult)
    elif(pr == 1):
        result = re_order_for_price(tmpresult)
        result.reverse()
    elif(di == 2):
        result = re_order(tmpresult,16)
    elif(di == 1):
        result = re_order(tmpresult,16)
        result.reverse()
    else:
        result = tmpresult

    '''for x in result:
            print x[1].decode('utf8')
            print x[16]'''

    txt = open('data/res.dat','w')
    txt.write(str(result))
    txt.close()

def run1(searcher, analyzer,target,distance,comein):
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print target
        print [comein[1]]

        flit = kind_fliter.kind_fliter(comein[1].decode('utf8'))
        if (not flit[0]):
            segment = jieba.cut(flit[1])
            command = " ".join(segment).replace("\n","").decode('utf-8')
            #print "Searching for:", command
            query_s = QueryParser(Version.LUCENE_CURRENT, "search",
                            analyzer).parse(command)
        else:
            query_s = QueryParser(Version.LUCENE_CURRENT, "kind",
                            analyzer).parse(flit[1])
        #scoreDocs = searcher.search(query_s, 50).scoreDocs
        #print target
        cal_tar_x = int(target[0]*100000)
        cal_tar_y = int(target[1]*100000)
        #print cal_tar_x
        radius = distance*A*100000
        #print radius
        cal_radius = int(radius)
        query1 = NumericRangeQuery.newFloatRange("calx",cal_tar_x-cal_radius,cal_tar_x+cal_radius,True,True)
        query2 = NumericRangeQuery.newFloatRange("caly",cal_tar_y-cal_radius,cal_tar_y+cal_radius,True,True)

        query = BooleanQuery()
        query.add(query1, BooleanClause.Occur.MUST)
        query.add(query2, BooleanClause.Occur.MUST)
        query.add(query_s, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(query, 500).scoreDocs
        return scoreDocs,query


def run2(searcher, analyzer,target,distance,comein):
        print [comein[1]]
        flit = kind_fliter.kind_fliter(comein[1])
        #print flit[1].decode('utf8')
        query_s = []
        if (not flit[0]):
            #print 11111111111
            segment = jieba.cut(flit[1])
            command = " ".join(segment).replace("\n","")
            #print "Searching for:", command
            query_s = QueryParser(Version.LUCENE_CURRENT, "search",
                            analyzer).parse(command)

        else:
            query_s = QueryParser(Version.LUCENE_CURRENT, "kind",
                            analyzer).parse(flit[1])
        query = BooleanQuery()
        query.add(query_s, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(query, 500).scoreDocs
        return scoreDocs,query

def run3(searcher, analyzer,target,distance,comein):
        #print '&&&&&&&&&&&&&&&&&&&&&&&&&&'
        #print target
        print [comein[1]]
        distance = 5000
        cal_tar_x = int(target[0]*100000)
        cal_tar_y = int(target[1]*100000)
        #print cal_tar_x
        radius = distance*A*100000
        #print radius
        cal_radius = int(radius)
        query1 = NumericRangeQuery.newFloatRange("calx",cal_tar_x-cal_radius,cal_tar_x+cal_radius,True,True)
        query2 = NumericRangeQuery.newFloatRange("caly",cal_tar_y-cal_radius,cal_tar_y+cal_radius,True,True)

        query = BooleanQuery()
        query.add(query1, BooleanClause.Occur.MUST)
        query.add(query2, BooleanClause.Occur.MUST)
        #query.add(query_s, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(query, 500).scoreDocs
        return scoreDocs,query

if __name__ == '__main__':
    come_in = eval(open('./data/cmd.dat','r').read())
    like = eval(open('./data/pref_wei.dat','r').read())
    come = analy(come_in)
    STORE_DIR = "index_folder"
    initVM()
    A = 8.99322056215e-06
    distance = 20000
    target = come[0]
    pr = come[2]
    di = come[3]
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    Doc = []
    loc = -1
    if (come[0]):
        if(come[1]):
            Doc,Que = run1(searcher, analyzer,target,distance,come)
            loc = 1
        else:
            Doc,Que = run3(searcher, analyzer,target,distance,come)
            loc = 1
    else:
        Doc,Que = run2(searcher, analyzer,target,distance,come)
        loc = 0
    sort(Doc,Que,searcher,loc,pr,di,come)

    searcher.close()
