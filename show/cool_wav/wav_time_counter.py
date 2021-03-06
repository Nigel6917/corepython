# -*- coding: utf-8 -*-
# @Time    : 2019/4/8
# @Author  : ErichLee ErichLee@qq.com
# @File    : pic_mv_cut.py
# @Comment : wav时间计算
#

import os
import librosa
import subprocess
import json

def traveseFileFmt2(file_dir, frmStr):
    fileList = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == frmStr:
                fileList.append(os.path.join(root, file))
    fileList.sort()
    return fileList


def getTimeLenSec(file0):
    y, sr = librosa.load(file0, sr=None)
    timeLen = librosa.get_duration(y, sr)

    return timeLen

def getLenTime(filename):
    command = ["ffprobe.exe","-loglevel","quiet","-print_format","json","-show_format","-show_streams","-i",filename]
    result = subprocess.Popen(command,shell=True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out = result.stdout.read()
    # temp = str(out.decode('gbk'))
    data = json.loads(out)["format"]['duration']
    return int(float(data))


def start():
    src_dir = u'E:/clean-fayuan/Batch2-20190610/wav_source'
    format_end = u'.wav'
    file_list = traveseFileFmt2(src_dir, format_end)

    if not file_list:
        print u'请在同级目录创建wav文件夹，并将识别wav文件放入其中'
        return
    # 创建生成文件地址
    time_all = 0
    output_msg = ''
    counter = 0
    for file0 in file_list:
        # newName = strrepWT(file0, src_dir, dst_dir)
        time_len = getLenTime(file0)
        time_all = time_all + time_len
        counter += 1
        output_msg = '{} {} [ {} ]  > {} \n'.format(output_msg, counter, file0, time_len)

    with open('output/rt_times.txt', 'w') as file:
        time_second = round(time_all, 0)
        # time_minute = time_second / 60
        time_hour = round(time_second / (60 * 60), 4)
        print time_all, time_hour, time_second
        file.write('累计时长，[{}]秒 折合[{}]小时，累计文件个数 [{}] 明细如下 ：\n'.
                   format(time_second, time_hour, counter))
        file.write(output_msg)


if __name__ == "__main__":
    start()
