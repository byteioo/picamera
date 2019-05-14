#!/bin/sh
basedir="/home/pi/software/picamera"
logpath=${basedir}"/log/"
campath=${basedir}"/py/cam/"

#删除当前log
sudo rm -rf ${logpath}"*.log"

#进入cam目录
cd $campath

#后台运行监控脚本
#nohup python -u start_http.py > ${logpath}"http.log"  2>&1 &
nohup python -u start_cam.py > ${logpath}"cam.log"  2>&1 &
