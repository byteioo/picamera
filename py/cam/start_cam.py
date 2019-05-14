#!/usr/bin/env py
# coding=UTF-8

import io
import os
from subprocess import Popen, PIPE
from threading import Thread
from time import sleep
import datetime as dt
import picamera
import logging
from websocket_server import WebsocketServer
import config

class Websocket_Server:
    def new_client(self,client,server):
        if self.verify_connect(client,server):
            server.send_message(client,config.JSMPEG_HEADER.pack(config.JSMPEG_MAGIC, config.V_WIDTH, config.V_HEIGHT))
        else:
            if client in server.clients:
                server.clients.remove(client)
            server.send_message(client, "认证失败")

    def verify_connect(self,client, server):
        text = client['query']
        print("params："+text+","+dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if "?" not in text or len(text) < 1:
            return False
        if text[0] != "?":
            return False
        if config.WS_TOKEN in text:
            return True
        return False

    def message_received(self,client, server, message):
        if self.verify_connect(client,server):
            server.send_message(client, "接收到：" + str(message))
        else:
            if client in server.clients:
                server.clients.remove(client)
            server.send_message(client, "认证失败")

class WebsocketThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.websocket = Websocket_Server()
        self.server = WebsocketServer(config.WS_PORT,loglevel=logging.INFO)
        self.client = self.websocket.new_client
        self.server.set_fn_new_client(self.client)
        self.server.set_fn_message_received(self.websocket.message_received)

    def run(self):
        self.server.run_forever()

    def shutdown(self):
        self.server.shutdown()

class BroadcastOutput(object):
    def __init__(self, camera):
        self.camera=camera
        self.converter = Popen([
            'ffmpeg',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', '%dx%d' % camera.resolution,
            '-r', str(float(camera.framerate)),
            '-i', '-',
            '-f', 'mpeg1video',
            '-b', '800k',
            '-r', str(float(camera.framerate)),
            '-'],
            stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
            shell=False, close_fds=True)

    def write(self, b):
        self.converter.stdin.write(b)

    def flush(self):
        self.converter.stdin.close()
        self.converter.wait()


class BroadcastThread(Thread):
    def __init__(self, output,websocket_server):
        Thread.__init__(self)
        self.converter = output.converter
        self.server = websocket_server
        self.camera=output.camera

    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read1(32768)
                if buf:
                    self.server.send_message_to_all(buf)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()

def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (config.V_WIDTH, config.V_HEIGHT)
        camera.framerate = config.FRAMERATE
        camera.vflip = config.VFLIP
        camera.hflip = config.HFLIP
        sleep(2)  # 摄像头预热时间
        output = BroadcastOutput(camera)
        websocket_thread=WebsocketThread()
        broadcast_thread = BroadcastThread(output, websocket_thread.server)
        camera.start_recording(output, 'yuv')
        img_file=img_verify.ImgFile()
        try:
            websocket_thread.start()
            broadcast_thread.start()
            print("监控服务已启动")
            while True:
                # 不断地获取摄像头的输入并添加时间戳
                camera.annotate_text = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                camera.wait_recording(1)

        except KeyboardInterrupt :
            pass
        finally:
            camera.stop_recording()
            broadcast_thread.join()
            websocket_thread.shutdown()
            websocket_thread.join()
            print('监控服务已退出')


if __name__ == '__main__':
    main()
