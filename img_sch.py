# -*- coding:utf-8 -*-

from cv2 import cv
from math import *
from read_write import *
from operator import itemgetter
CONST_C = 2
kinds = ['烤串 烧烤 肉串', '火锅','烤鸭 烧鸭', '牛排','小笼','鸡排 炸鸡 ']
NUM = 60
v1,v2 = 0.15,0.35
I = [i+1 for i in xrange(12)]

def get_p(img,v1,v2):
    p = []
    p_no_hash = []
    h = img.height
    w = img.width
    for row in xrange(2):
        for col in xrange(2):
            rect = [0,0,0]
            for i in xrange(row*h/2,(row+1)*h/2):
                for j in xrange(col*w/2,(col+1)*w/2):
                        rect[0] += img[i,j][0]
                        rect[1] += img[i,j][1]
                        rect[2] += img[i,j][2]
            summ = rect[0] + rect[1] + rect[2]
            for clr in xrange(3):
                tmp = float(rect[clr])/summ
                p_no_hash.append(tmp)
                if (v1 != 0 and v2 != 0): p.append(int(tmp > v1) + int(tmp > v2))
    #print p_no_hash
    return p, p_no_hash

def get_dist(p1,p2):
    #print p1,p2
    if (len(p1) != len(p2)):
        print "error!"
    else:
        tmp = 0
        for i in xrange(len(p1)):
            tmp += (p1[i] - p2[i])**2
        #print tmp
        return sqrt(tmp)

def is_in(v,low,up):
    return int(v >= low) - 1 + int(v > up)

def get_proj(p):
    #I = [i+1 for i in xrange(13)]
    #I = [1,3,7,8]
    lenI = len(I)
    res = ""
    pos = 0
    i = 0
    cnt = 0
    one_cnt = 0
    while pos <= lenI:
        if (pos < lenI): cmp_ = is_in(I[pos],CONST_C*i+1,CONST_C*(i+1))
        #else : endd = 1
        #print"cmp = ",cmp_
        if  pos == lenI or cmp_ != 0 :
            #print "+++++++"
            i += 1
            #pos -= 1
            res += ('1'*one_cnt+'0'*(cnt-one_cnt))
            #print  ('1'*one_cnt+'0'*(cnt-one_cnt))
            cnt = 0
            one_cnt = 0
            if (pos == lenI): break
            else:continue
        else:
            cnt += 1
            if I[pos]-CONST_C*i <= p[i]:
                one_cnt += 1
                #print '=====',one_cnt
            pos += 1
    return res

def hash_init(v1,v2):
    proj_dic = {}
    p_li = []
    pnh_li = []
    for i in xrange(NUM):
        img = cv.LoadImage("Dataset/"+str(i+1)+".jpg")
        p,pnh = get_p(img,v1,v2)
        p_li.append(p)
        pnh_li.append(pnh)
        proj_ = get_proj(p)
        if proj_ in proj_dic.keys():
            proj_dic[proj_].append(i)
        else:
            proj_dic[proj_] = [i]
    return proj_dic, p_li, pnh_li

def get_bst_mtched(target,v1,v2,proj_dic, p_li, pnh_li):
    t_p,t_p_n = get_p(target,v1,v2)
    t_proj = get_proj(t_p)
    #proj_dic, p_li, pnh_li = hash_init(v1,v2)
    match_1st = []
    if t_proj not in proj_dic.keys():
        #print "not matched!"
        return []
    else:
        match_1st = proj_dic[t_proj]
    li = [0,0,0,0,0,0,0]
    lii = [0,0,0,0,0,0,0]
    cnt = [0,0,0,0,0,0,0]
    if 1:
        min_d = 1000000000
        bst = []
        for i in match_1st:
            #print i,
            tmp_d = get_dist(t_p_n,pnh_li[i])
            #print i,tmp_d
            if 1:
                li[i/10] += tmp_d**2
                lii[i/10] += e**(-tmp_d/2)
                #print e**(-tmp_d/2)
                cnt[i/10] += 1
            #print i, 1/tmp_d
            #print i, tmp_d
            if (tmp_d < min_d):
                min_d = tmp_d
                bst = [i]
            elif abs(tmp_d - min_d) <= 1e-10:
                   bst.append(i)
    res = {}
    for i in xrange(len(li)):
        try:
            res[i] = lii[i]*cnt[i]/li[i]
        except:
            res [i] = 0
    sorted_a = sorted(res.iteritems(), key=itemgetter(1))
    first = sorted_a[-1]
    second = sorted_a[-2]
    #print sorted_a
    #print sorted_a
    return bst ,first,second

def Lsh_Search(target,v1,v2):
    #print "Lsh init..."

    proj_dic = eval(readin('img_data/lsh_proj_dic.txt'))
    p_li = eval(readin('img_data/lsh_p_li.txt'))
    pnh_li = eval(readin('img_data/lsh_pnh_li.txt'))
    tmp_v1,tmp_v2 = eval(readin('img_data/value.txt'))

    #print "Finished.\n===== Lsh Search ======:"
    #start = time.time()
    res,fir,sec = get_bst_mtched(target,v1,v2,proj_dic, p_li, pnh_li)
    if (len(res) != 0):
        return res[0],fir,sec
    else:
        return -1,fir,sec


def NN_Search(target):
    #print "NN init..."

    min_d = 1000000000
    bst = []

    pnh_li = eval(readin("img_data/NN_pnh_li.txt"))

   # print "Finished.\n===== NN Search ======:"
    t_p,t_p_n = get_p(target,0,0)
    for i in xrange(NUM):
        tmp_d = get_dist(t_p_n,pnh_li[i])
            #print i, tmp_d
        if (tmp_d < min_d):
                min_d = tmp_d
                bst = [i]
        elif abs(tmp_d - min_d) <= 1e-10:
                 bst.append(i)
   # print min_d
    #print "Best matched:"
    if len(bst) != 0:
        return bst[0]
    else:
        return -1

def img_to_key(img):

    #print 'The seperate-values used this time are:', v1, v2

    target = cv.LoadImage(img)
    bst_lsh,fir,sec = Lsh_Search(target,v1,v2)
    bst_nn = NN_Search(target)
    lsh_v = (bst_lsh ) /10
    nn_v = (bst_nn ) /10
    #print bst_lsh,bst_nn,fir,sec
    s = set()
    if fir[1] == 0 and sec[1] == 0:
         s.add((bst_nn )/10)
         s.add((bst_lsh )/10)
    #elif fir[1] != 0 and sec[1] == 0:
     #   return kinds[fir[0]]
    else:
        fir_v = fir[1]
        sec_v = sec[1]
        if fir[0] == lsh_v: fir_v *= 1.5
        if fir[0] == nn_v: fir_v *= 1.65
        if sec[0] == lsh_v: sec_v *= 1.5
        if sec[0] == nn_v: sec_v *= 1.65
        if sec_v > fir_v:
            s.add(sec[0])
        else:
            s.add(fir[0])

    if lsh_v == nn_v:
        s.add(lsh_v)
    res = ""
    for item in s:
        res += kinds[item]+' '
    return res
if __name__=="__main__":
    print img_to_key('9421763_215327679000_2.jpg').decode('utf8')

