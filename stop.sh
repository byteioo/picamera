#!/bin/bash
stopProgress(){
	task=$1
	str=`ps -ef |grep $task | grep -v grep`
	if [ -n "$str" ];then
		ps -ef |grep $task| grep -v grep | awk '{print $2}' | xargs kill -9
		echo "已停止"${task}
	else
		echo "未检测到 "${task}
	fi
}
#stopProgress "start_http.py"
stopProgress "start_cam.py"