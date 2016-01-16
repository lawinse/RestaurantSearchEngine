#!/usr/bin/env python

import web
from web import form
from lucene import *
import urllib2
import os
import time
import img_sch
import shop2_to_shop_recmd

def readin(s):
    f=open(s, 'r')
    readin=f.read()
    f.close()
    return readin
def writedwn(s, path):
    res=open(path, 'w')
    res.write(s)
    res.close()

web.config.debug = False
TimeMechine = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))

urls = (
    '/', 'index',
    '/index', 'index',
    '/s', 'search',
    '/indexpic', 'indexpic',
    '/pchome', 'pchome'
)
DBStore = eval(readin('data/user_table.dat'))
FavoStore = eval(readin('data/favorite_table.dat'))
HistStore = eval(readin('data/history_table.dat'))

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username':'', 'password':'', 'recommend':[]})
render = web.template.render('templates', globals={'content':session}, cache = False) # your templates


class index:
    def GET(self):
        if (session.username!=''):
            user = session.username
            info = 'Weclome!'
            session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
        else:
            user = ''
            info = 'Welcome!'
            session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
        # print 'Hello fuck you!'
        # print session.recommend
        # print 'Hello fuck you!2'
        return render.index(session, info)
    def POST(self):
        info = 'Welcome!'
        user = ''
        print '/............Process of LogIn & SignUp............../'
        # print DBStore
        try:
            username1 = web.input()['inputUsername1']
            password1 = web.input()['inputPassword1']
        except:
            username1 = ''
            password1 = ''
        try:
            username2 = web.input()['inputUsername2']
            password2 = web.input()['inputPassword2']
            password3 = web.input()['inputPassword3']
        except:
            username2 = ''
            password2 = ''
            password3 = ''
        if ((username1!='' and password1!='')and(username2=='' or password2=='' or password3=='')):
            print 'Log In'
            if ((username1 in DBStore)and(password1==DBStore[username1])):
                user = username1
                info = 'Log In Successfully'
                session.username = username1
                session.password = password1
            else:
                user = ''
                info = 'User Non-existence or Password Error'
        elif ((username1=='' or password1=='')and(username2!='' and password2!='' and password3!='')):
            print 'Sign Up'
            l1 = len(username2)
            l2 = len(password2)
            l3 = len(password3)
            if not(l1>=4 and l1<=20 and l2>=6 and l2<=16 and l3>=6 and l3<=16):#matching rules
                user = ''
                info = 'Username: 4-20 characters; Password: 6-16 characters'
            elif ((username2 not in DBStore)and(password2==password3)):
                DBStore[username2] = password2
                writedwn(str(DBStore).encode('utf8'), 'data/user_table.dat')
                FavoStore[username2] = {}
                writedwn(str(FavoStore).encode('utf8'), 'data/favorite_table.dat')
                HistStore[username2] = {}
                writedwn(str(HistStore).encode('utf8'), 'data/history_table.dat')
                user = username2
                info = 'Sign Up Successfully'
                session.username = username2
                session.password = password2
            elif (username2 in DBStore):
                user = ''
                info = 'This Username has been used, please use another Username.'
            elif (password2!=password3):
                user = ''
                info = 'Twice inputs of password are different'
            else:
                user = ''
                info = 'Unknown Errors'
        else:
            user = ''
            if (session.username==''):
                info = 'Welcome!'
            else:
                info = 'Log Out Successfully'
            session.username = ''
            session.password = ''
        if (session.username!=''):
            session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
            print 'Current User :', session.username
        else:
            session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
        # print HistStore
        return render.index(session, info)

# ['place', 'cmd', 'price', 'distance']
class search:
    def GET(self):
        input_adr = web.input()['adr']
        input_cmd = web.input()['cmd']
        try:
            input_typ = web.input()['typ']
            input_bs = web.input()['bs']
        except:
            input_typ = ''
            input_bs = ''
    	input_adr = input_adr.decode('utf8')
    	input_cmd = input_cmd.decode('utf8')
    	#print 'input_adr: ', input_adr
    	#print 'input_cmd: ', input_cmd
    	#print 'input_typ: ', input_typ
    	#print 'input_bs: ', input_bs
        list_cmd = ['', '', 0, 0]
        list_cmd[0] = input_adr
        list_cmd[1] = input_cmd
        if (input_typ=='price' and input_bs=='lth'):
            list_cmd[2] = 1
        elif (input_typ=='price' and input_bs=='htl'):
            list_cmd[2] = 2
        elif (input_typ=='distance' and input_bs=='lth'):
            list_cmd[3] = 1
        elif (input_typ=='distance' and input_bs=='htl'):
            list_cmd[3] = 2
        print str(list_cmd)
        if ((len(str(input_cmd))+len(str(input_adr))) >= 0):
            writedwn(str(list_cmd), 'data/cmd.dat')
            os.system('python SearchFiles.py')
            # print "The res: ", readin('data/res.dat')
            res = eval(readin('data/res.dat'))
            print 'The input_cmd: ', input_cmd
            if (session.username!=''):
                session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
            else:
                session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
            return render.search(res, input_adr, input_cmd, session)
        else:
            return render.index(session, '')
    def POST(self):
        try:
            favi = web.input()['favorite']
        except:
            favi = ''
        try:
            x = web.input(myfile={})
            filedir = './static/pic' # change this to the directory you want to store the file in.
            if 'myfile' in x: # to check if the file-object is created
                filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                filename=filepath.split('/')[-1].decode('utf-8') # splits the and chooses the last part (the filename with extension)
                fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
                fout.close() # closes the file, upload complete.
                infile = filedir +'/'+filename
                outfile = infile + ".thumbnail"
                img_query = (filedir+'/'+filename).decode('utf8')
                print img_query
                img_cmd = img_sch.img_to_key(img_query).decode('utf8')
                list_cmd = ['', '', 0, 0]
                list_cmd[1] = img_cmd
                writedwn(str(list_cmd), 'data/cmd.dat')
                os.system('python SearchFiles.py')
                # print "The res: ", readin('data/res.dat')
                res = eval(readin('data/res.dat'))
                print 'img_cmd: ', img_cmd
                if (session.username!=''):
                    session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
                else:
                    session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
                return render.search(res, '', img_cmd, session)
        except:
            pass
        print 'Adding to Favorite: ', favi
        # print type(x)
        if (session.username!='' and favi!=''):
            username = session.username
            print 'Current User :', username
            # print FavoStore
            if (favi not in FavoStore[username]):
                FavoStore[username][favi] = favi######### modify to 'url+id':'url'
                writedwn(str(FavoStore).decode('utf8'), 'data/favorite_table.dat')

class indexpic:
    def GET(self):
        info = 'Welcome!'
        if (session.username!=''):
            session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
        else:
            session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
        return render.indexpic(session, info)
    def POST(self):
        info = 'Welcome!'
        user = ''
        print '/............Process of LogIn & SignUp............../'
        # print DBStore
        try:
            username1 = web.input()['inputUsername1']
            password1 = web.input()['inputPassword1']
        except:
            username1 = ''
            password1 = ''
        try:
            username2 = web.input()['inputUsername2']
            password2 = web.input()['inputPassword2']
            password3 = web.input()['inputPassword3']
        except:
            username2 = ''
            password2 = ''
            password3 = ''
        if ((username1!='' and password1!='')and(username2=='' or password2=='' or password3=='')):
            print 'Log In'
            if ((username1 in DBStore)and(password1==DBStore[username1])):
                user = username1
                info = 'Log In Successfully'
                session.username = username1
                session.password = password1
            else:
                user = ''
                info = 'User Non-existence or Password Error'
        elif ((username1=='' or password1=='')and(username2!='' and password2!='' and password3!='')):
            print 'Sign Up'
            l1 = len(username2)
            l2 = len(password2)
            l3 = len(password3)
            if not(l1>=4 and l1<=20 and l2>=6 and l2<=16 and l3>=6 and l3<=16):#matching rules
                user = ''
                info = 'Username: 4-20 characters; Password: 6-16 characters'
            elif ((username2 not in DBStore)and(password2==password3)):
                DBStore[username2] = password2
                writedwn(str(DBStore).encode('utf8'), 'data/user_table.dat')
                FavoStore[username2] = {}
                writedwn(str(FavoStore).encode('utf8'), 'data/favorite_table.dat')
                HistStore[username2] = {}
                writedwn(str(HistStore).encode('utf8'), 'data/history_table.dat')
                user = username2
                info = 'Sign Up Successfully'
                session.username = username2
                session.password = password2
            elif (username2 in DBStore):
                user = ''
                info = 'This Username has been used, please use another Username.'
            elif (password2!=password3):
                user = ''
                info = 'Twice inputs of password are different'
            else:
                user = ''
                info = 'Unknown Errors'
        else:
            user = ''
            if (session.username==''):
                info = 'Welcome!'
            else:
                info = 'Log Out Successfully'
            session.username = ''
            session.password = ''
        if (session.username!=''):
            session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
            print 'Current User :', session.username
        else:
            session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
        # print HistStore
        return render.indexpic(session, info)

class pchome:
    def GET(self):
        try:
            delete_item = eval(web.input()['deleteFavo'])
            # print delete_item
            key_delete = str(delete_item[1]).decode('utf8')+'_'+str(delete_item[-1])
        except:
            key_delete = 'meiyouooooooo'
            pass
        print key_delete
        if (session.username!=''):
            if (key_delete in FavoStore[session.username]):
                FavoStore[session.username].pop(key_delete)
                writedwn(str(FavoStore).decode('utf8'), 'data/favorite_table.dat')
        else:
            pass
        ##try to delete item##
        src = []
        if (session.username!=''):
            session.recommend = shop2_to_shop_recmd.shop_to_cmd(FavoStore[session.username])
        else:
            session.recommend = shop2_to_shop_recmd.shop_to_cmd({})
        ##Show recommend(above)##
        if (session.username!=''):
            username = session.username
            print 'Current User :', username
            # print type(FavoStore[username])
            src = shop2_to_shop_recmd.favishow(FavoStore[username])
        #print 'SRC', src
        #print '666'
        if (session.username!=''):
            return render.pchome(src, session)
        else:
            return render.index(session, 'Welcome!')


if __name__ == "__main__":
    app.run()
