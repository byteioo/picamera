# picamera
### 灵感源于 [pistreaming][1]，但是进行了大改
------

个人需求：

> * 使用树莓派自带的摄像头监控书桌
> * 需求在外网可以访问
> * 安全，ws连接(获取视频流)时需要token认证

#### token认证思路很简单：
在配置文件里面预置一个长字符串，每次websocket连接都会检测url中是否含有这个字符串，如果没有则踢出 client list(视频流不会对其转发)

在原作中改来改去一路debug都没找到ws连接时带的参数，原作使用的是ws4py，整了半天我索性换成了websocket_server 只有一个.py文件,给其增加了转发request url中的参数的功能。

使用本项目之前你需要完成如下操作：
> *  安装ffmpeg (sudo apt-get install ffmpeg -y)
> * 编辑 py/cam目录下的config.py文件，设置WS_TOKEN 和 WEB_TOKEN
> * 在树莓派设置中打开摄像头

如果你成功完成了上面的操作，那么在项目目录下，执行
```
nohup python -u start_http.py > log/http.log  2>&1 &
nohup python -u start_cam.py > log/cam.log  2>&1 &
```
即可启动项目，日志保存在log目录下
访问 http://树莓派IP:9082?xxxx 即可看到摄像头内容
xxxxx 为自己设置的WEB_TOKEN
配合 frp 可外网访问
