#!/usr/bin/env py
#coding=UTF-8

import io
import os
from threading import Thread
from time import time
from string import Template
from http.server import HTTPServer, BaseHTTPRequestHandler
import config

###########################################
WIDTH = config.V_WIDTH
HEIGHT = config.V_HEIGHT
HTTP_PORT = config.HTTP_PORT
WS_PORT = config.WS_PORT
WEB_TOKEN = config.WEB_TOKEN
WS_TOKEN = config.WS_TOKEN

##########################################
#  WEB网页路由
WEB_INDEX = config.WEB_INDEX
###########################################

class HttpHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        headers=self.headers #获取请求头的headers
        params = list(self.getParams(self.path).values()) #获取URL中的参数

        if "?" not in self.path or WEB_TOKEN not in params :
            # URL没带参数或者参数错误 返回 404
            if "X-Forwarded-For" in headers.keys():
                self.send_error(404, 'File not found  IP:' + headers["X-Forwarded-For"])
            else:
                self.send_error(404, 'File not found')
            return
        self.path = self.path.split("?")[0]
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location',WEB_INDEX)
            self.end_headers()
            return
        elif self.path == '/index.html':
            content_type = 'text/html; charset=utf-8'
            tpl = Template(self.server.index_template)
            content = tpl.safe_substitute(dict(
                WS_PORT=WS_PORT, WIDTH=WIDTH, HEIGHT=HEIGHT, WEB_TOKEN=WEB_TOKEN,WS_TOKEN=WS_TOKEN))
        else:
            self.send_error(404, 'File not found')
            return
        content = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))
        self.send_header('Last-Modified', self.date_time_string(time()))
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(content)

    def getParams(self,url):
        dict={}
        values = url.split('?')[- 1]
        for key_value in values.split('&'):
            k=key_value.split('=')
            if len(k) >1 :
                dict[k[0]]=k[1] # k0是key(参数名) k1是value(参数值)

        return dict

class PiCameraHttpServer(HTTPServer):
    def __init__(self):
        super(PiCameraHttpServer, self).__init__(
                ('', HTTP_PORT), HttpHandler)
        with open(WEB_INDEX, 'r',encoding="utf-8") as f:
            self.index_template = f.read()

def main():
    print('启动http服务')
    http_server = PiCameraHttpServer()
    http_thread = Thread(target=http_server.serve_forever)
    try:
        print('开启 HTTP server 线程')
        http_thread.start()
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        print('关闭 HTTP server')
        http_server.shutdown()
        print('等待 HTTP server 线程退出')
        http_thread.join()

if __name__ == '__main__':
    main()
