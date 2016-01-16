# -*- coding:utf-8 -*-

from read_write import *
kind_dic = {"广东菜 粤菜":"广东菜 粤菜","川菜 四川菜":"川菜","湘菜 湖南菜":"湘菜","湖北菜 鄂菜":"湖北菜",\
            "江浙菜 江苏菜 浙江菜 上海菜":"江浙菜","新疆菜 清真菜":"新疆菜","闽南菜 福建菜 台湾菜":"闽南菜 福建菜 台湾菜","小吃 快餐":"小吃 小吃快餐","日本美食 日餐 Japan":"日本美食 日餐",\
            "安徽菜 徽菜":"徽菜","私房菜 家常菜" :"私房菜 家常菜","素菜 素食":"素菜 素食","自助餐 自助":"自助餐","韩国 韩国料理":"韩国料理","山东菜 鲁菜":"鲁菜"}

a = " 北京菜 川菜 湘菜 湖北菜 江浙菜 粤菜 东北菜 新疆菜 西北菜 云南菜 贵州菜 鲁菜 \
素菜 火锅 海鲜 小吃 烧烤 自助餐 甜点 日本美食 韩国料理 东南亚菜 西餐 山西菜 \
台湾菜 江西菜 蒙古菜 徽菜 私房菜 闽南菜 家常菜 烤鸭 官府菜 农家菜 广东菜 四川菜 湖南菜 \
鄂菜 江苏菜 浙江菜 上海菜 清真 清真菜 福建菜 创意菜 快餐 日餐 素食 Japan 安徽菜 自助 ".decode('utf8')

kinds = a.split()

def kind_fliter(str):

    #str = gbk_2_utf8(str)
    #str = str.decode('gbk').decode('utf8')
    #print [str]
    tp = [0,0]
    if str in kinds:
        tp[0] = 1
        for item in kind_dic.keys():
            #print item.decode('utf8')
            if str.encode('gbk') in item.encode('gbk'):
                #print "1111"
                tp[1] = kind_dic[item].decode('utf8')
                return tp

        tp[1] = str.decode('utf8')
        return tp
    else:
        if u'\u505c\u8f66' in str and u'\u6cca\u8f66' not in str:
            str += u' \u6cca\u8f66'
        elif u'\u505c\u8f66' not in str and u'\u6cca\u8f66'  in str:
            str += u' \u505c\u8f66'

        return [0,str]
if __name__ == "__main__":
     print kind_fliter('\xd1\xf2\xc8\xe2\xb4\xae')


