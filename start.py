#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
import mnist_train
import mnist_cnn as mnist_interence
import numpy as np
import os

def preparePng(path):
    lena = mpimg.imread(path)
    lena.astype(np.float32)
    img = np.dot(lena[..., :3], [0.299, 0.587, 0.114])
    return img

def predictInt2(imgdata):
    with tf.Graph().as_default() as g:  # 将默认图设为g
        # 定义输入输出的格式
        x = tf.placeholder(tf.float32, shape=[1,
                                              mnist_interence.IMAGE_SIZE,
                                              mnist_interence.IMAGE_SIZE,
                                              mnist_interence.NUM_CHANNEL], name='x-input')
        regularizer = tf.contrib.layers.l2_regularizer(0.0001)
        y = mnist_interence.interence(x, True, regularizer)
        variable_averages = tf.train.ExponentialMovingAverage(mnist_train.MOVING_AVERAGE_DECAY)
        variable_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variable_to_restore)  # 这些值要从模型中提取
        with tf.Session() as sess:
            if (os.path.exists(os.path.join('model', 'checkpoint'))):
                # Restore variables from disk.
                saver = tf.train.import_meta_graph(os.path.join('model', 'model.meta'))
                saver.restore(sess, tf.train.latest_checkpoint(os.path.join('model')))
                xs = imgdata.reshape(1,28,28,1)
                prediction = tf.argmax(y, 1)
                num = prediction.eval(feed_dict={x: xs}, session=sess)
                num = num[0]
                return num

#服务器与客户端连接实例
class Connect(object):
    users=[]

    #建立客户端的连接
    def newUser(self,newMan):
        self.users.append(newMan)       #加入

    #客户端用户退出，删除该用户的连接
    def exit(self,quitter):
        self.users.remove(quitter)

    #接受用户端的图片
    def receiveMessage(self,sender,message):
        src=message.split(',')[1]
        img = base64.b64decode(src)
        u=str(sender.get_argument('u'))
        path = 'static/img/'+u+'.png'
        file = open(path, 'wb')
        file.write(img)
        file.close()

        data=preparePng(path)
        num = str(predictInt2(data))
        self.sendMessage(sender,num)

    #发送一条消息给user客户端img
    def sendMessage(self,user,message):
        user.write_message(message)

class LoginHandler(tornado.web.RequestHandler):
    '''进行登陆'''
    def get(self):
        self.render('index.html')

class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        u=uuid4()
        image_src=str(self.get_argument('image_src'))
        self.render('show.html',image_src=image_src,u=u)


class UpdatesMssageHandler(tornado.websocket.WebSocketHandler):
    '''
        websocket， 记录客户端连接，删除客户端连接，接收最新消息
    '''
    def open(self):
        self.application.connect.newUser(self)    #记录客户端连接

    def on_close(self):
        self.application.connect.exit(self)  #删除客户端连接

    def on_message(self, message):
        self.application.connect.receiveMessage(self, message)   #处理客户端提交的最新消息


class Application(tornado.web.Application):
    def __init__(self):
        self.connect = Connect()
        handlers=[
            (r'/', LoginHandler),
            (r'/show/update/', UpdatesMssageHandler),
            (r'/show', ShowHandler),
        ]
        settings = {
            'template_path': 'templates',
            'static_path': 'static',
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
