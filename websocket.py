import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
from tornado.options import define,options
import time
import utli.ui_methods
import utli.ui_modules
from ORM.user_module import User
from tornado.web import authenticated
from pycket.session import  SessionMixin
import tornado.websocket
from datetime import datetime


define('port',default=8888,help='run port',type =int)

from ORM.connect import session,Base

class BaseHander(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        #current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('ID')
        if current_user:
            return current_user
        return None

class BaseWebsocketHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('ID')
        if current_user:
            return current_user#当前用户
        return None




class LoginHander(BaseHander):

    def get(self, *args, **kwargs):
        nextname = self.get_argument('next', '')
        #print(nextname)
        self.render('form.html',
                    nextname = nextname)


    def post(self, *args, **kwargs):
        nextname =self.get_argument('next','')
        user = self.get_argument('name','no')
        password = self.get_argument('password','')
        username =User.by_name(user)
        if username and password == username.password:
            #self.set_secure_cookie('ID',user)
            self.session.set('ID',user)
            self.redirect(nextname)
            # self.render('login.html',
            #             username=username
            #            )
        else:
            self.write('用户名 密码错误')


class Indexhandler(BaseHander):
    @authenticated
    def get(self):
        self.render('08websocket.html')

class MessageHandler(BaseWebsocketHandler):
    users = set()#集合


    def open(self, *args, **kwargs):
        MessageHandler.users.add(self)
        print('-'*20+'open'+'-'*20)
        for u in self.users:
            u.write_message(
                ('%s 登陆了' %self.current_user)
            )



    def on_message(self, message):
        #print(dir(self))
        print(self.request.remote_ip)
        print(message)
        for u in self.users:
            u.write_message(
                '%s-%s说:%s' %(
                    self.current_user,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    message
                )
            )

    def on_close(self):
        if self in MessageHandler.users:
            MessageHandler.users.remove(self)
            for u in self.users:
                u.write_message('%s 下线了' %self.current_user)
        print('-'*20+'close'+'-'*20)


class SyncHandler(BaseHander):
    def get(self):
        id = self.get_argument('id',1)
        user1 = User.by_id(id)
        time.sleep(6)
        user2 = {
            'username' : user1.username,
            'id' : user1.id
        }
        self.write(user2)

application = tornado.web.Application(
    handlers=[
        (r'/login',LoginHander),
        (r'/index',Indexhandler),
        (r'/websocket',MessageHandler),
        (r'/sync',SyncHandler)
        #(r'/(.*)',NotHandler)
    ],
    template_path = 'templates',
    static_path= 'static',
    ui_methods= utli.ui_methods ,
    ui_modules= utli.ui_modules,
    cookie_secret = 'ljc',
    login_url = '/login',
    pycket = {
        'engine':'redis',
        'storage':{
            'host':'localhost',
            'port':6379,
            'db_sessions':5,
            'db_notifications':11,
            'max_connections':2**33,
        },
        'cookies':{
          'expires_days':38,
          'max_age':100
        },
    },
    debug = True
   )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()