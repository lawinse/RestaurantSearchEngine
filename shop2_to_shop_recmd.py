# -*- coding:utf-8 -*-

from read_write import *
from copy import *
import random
shop2kinds = eval(readin('./data/shop_to_kinds.dat'))
total_info = eval(readin('./data/total_info.dat'))
pref_wei_dat = './data/pref_wei.dat'
def shop_to_cmd(user_dict):
    pref_wei = {}
    pfrce_li = []
    if len(user_dict) != 0:
        li = []
        shop_li = []
        for item in user_dict.keys():
            li.append(user_dict[item])
            shop_li.append(item)
        pfrce = set()
        pfrce_li = []
        for item in li:
            for i in shop2kinds[item]:
                pfrce.add(i)
                pfrce_li.append(i)
        res = []
        for shops in shop2kinds.keys():
            if len(pfrce & shop2kinds[shops]) != 0 and shops not in shop_li:
                try : res.append(total_info[shops])
                except:pass
                if len(res) == 20 :
                    break
        res = random.sample(res, 5)   #
        max_cnt = 0
        for prf in pfrce_li:
            tmp_cnt = pfrce_li.count(prf)
            pref_wei[prf] = tmp_cnt
            max_cnt = max(max_cnt,tmp_cnt)
        for prf in pref_wei.keys():
            pref_wei[prf] = float(pref_wei[prf]) / max_cnt
        writedwn(str(pref_wei), pref_wei_dat)
        return  res
    else:
        res_ = []
        tmp = list(total_info.values())#
        res_ = random.sample(tmp, 5)#
        writedwn(str({}), pref_wei_dat)
        return res_

def favishow(user_dict):
    #res = []
    for item in user_dict:
        try:
            res.append(total_info[item])
        except:
            continue
    return res

if __name__=="__main__":
    pass
    #for item in total_info:
     #    tmp = total_info[item][7]
      #   tmp = tmp[:min(len(tmp),45)]+"..."
       #  total_info[item][7] = tmp
    #writedwn(str(total_info),'./data/total_info.dat')
    #dic = {1:u'\u5fb7\u6797\u574a\u7d20\u98df\u574a_13550',2:u'\u65b0\u6fb3\u6e2f\u5f0f\u8336\u9910\u5385_2451'}
    #dic  = {}
    #a = ( shop_to_cmd(dic) )
    #Favo = eval(readin('./data/favorite_table.dat'))
    #udict = Favo['Phonic']
    #print_li(a)

