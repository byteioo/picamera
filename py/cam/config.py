# coding=UTF-8
import os
from struct import Struct

#摄像头设置
V_WIDTH = 640 #视频宽度
V_HEIGHT = 480 #视频高度
HTTP_PORT = 9082 #HTTP服务端口
WS_PORT = 9084 #WEBSOCKET端口
FRAMERATE = 24
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
VFLIP = True #垂直翻转
HFLIP = False
WS_TOKEN = "" #获取监控数据流的TOKEN 必须填写!!!!!!!

#人脸检测
AIP_START = False #是否开启人脸检测
AIP_TIME = 15  #人脸扫描时间间隔
AIP_SCORE = 70 #人脸匹配的最低可信度


#网络令牌设置
WEB_TOKEN = "xxxx"  #GET请求 INDEX.HTML 的 WEB_TOKEN 必须填写


BASE_PATH = os.path.abspath(os.path.join(os.getcwd(), "../..")) #根路径
AVATAR_PATH=BASE_PATH + "/data/avatar/"#用户头像路径

#WEB网页路由
WEB_INDEX = BASE_PATH+"/index.html"