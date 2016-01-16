#-*- coding:utf-8 -*-

import urllib2,urllib,httplib
import json
import math
from decimal import Decimal

class xBaiduMap:
    def __init__(self,key='your_key'):
        self.host='http://api.map.baidu.com'
        self.path='/geocoder?'
        self.param={'address':None,'output':'json','key':key,'location':None,'city':None}

    def getLocation(self,address,city=None):
        rlt=self.geocoding('address',address,city)
        if rlt!=None:
            l=rlt['result']
            if isinstance(l,list):
                return None
            return l['location']['lat'],l['location']['lng']

    def getAddress(self,lat,lng):
        rlt=self.geocoding('location',"{0},{1}".format(lat,lng))
        if rlt!=None:
            l=rlt['result']
            return l['formatted_address']
            #Here you can get more details about the location with 'addressComponent' key
            #ld=rlt['result']['addressComponent']
            #print(ld['city']+';'+ld['street'])
            #
    def geocoding(self,key,value,city=None):
        if key=='location':
            if 'city' in self.param:
                del self.param['city']
            if 'address' in self.param:
                del self.param['address']

        elif key=='address':
            if 'location' in self.param:
                del self.param['location']
            if city==None and 'city' in self.param:
                del self.param['city']
            else:
                self.param['city']=city
        self.param[key]=value
        r=urllib.urlopen(self.host+self.path+urllib.urlencode(self.param))
        rlt=json.loads(r.read())
        if rlt['status']=='OK':
            return rlt
        else:
            print "Decoding Failed"
            return None

class Point:
    pass

def max(a,b):
    if a>b:
        return a
    return b
def min(a,c):
    if a>c:
        return c
    return a

def lw(a, b, c):
#     b != n && (a = Math.max(a, b));
#     c != n && (a = Math.min(a, c));
    a = max(a,b)
    a = min(a,c)
    return a

def ew(a, b, c):

    while a > c:
        a -= c - b
    while a < b:
        a += c - b
    return a


def oi(a):
    return math.pi * a / 180

def Td(a, b, c, d):
    return 6370996.81 * math.acos(math.sin(c) * math.sin(d) + math.cos(c) * math.cos(d) * math.cos(b - a))

def Wv(a, b):
    if not a or not b:
        return 0;
    a.lng = ew(a.lng, -180, 180);
    a.lat = lw(a.lat, -74, 74);
    b.lng = ew(b.lng, -180, 180);
    b.lat = lw(b.lat, -74, 74);
    return Td(oi(a.lng), oi(b.lng), oi(a.lat), oi(b.lat))

def getDistance(a, b):
    c = Wv(a, b);
    return c

def get_distance(a,b):
    p1 = Point()
    p1.lat = a[0]
    p1.lng = a[1]
    p2 = Point()
    p2.lat = b[0]
    p2.lng = b[1]
    return  getDistance(p1, p2)


def get_cdnt(road,city):
    bm = xBaiduMap()
    return bm.getLocation(road,city)


if __name__ == '__main__':
    #frompoint = [40.0351,116.40863583333334]
    #topoint = [40.0352,116.4086358333333]
    g=GPS()

    bm=xBaiduMap()
    #for i in range(15):
    a =  bm.getLocation("东川路800号",'上海')
    #print bm.getLocation("人民路沙浦路")
    b =  bm.getLocation("东川路永平路",'上海')
    #print bm.getAddress(31.265031, 121.487298)
    frompoint = [a[0],a[1]]
    topoint = [b[0],b[1]]
    print g.spherical_distance(frompoint,topoint)

