#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 NXEZ.COM.
# http://www.nxez.com
#
# Licensed under the GNU General Public License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.gnu.org/licenses/gpl-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# tutorials url: http://shumeipai.nxez.com/2015/11/22/saks-diy-tutorials-chime.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

import RPi.GPIO as GPIO
import time
import sys

PIN_NO_BEEP = 11
PIN_NO_LED = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NO_BEEP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PIN_NO_LED, GPIO.OUT, initial=GPIO.HIGH)

# 单次哔声和LED发光
def beep(seconds):
    GPIO.output(PIN_NO_BEEP, GPIO.LOW)
    GPIO.output(PIN_NO_LED, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(PIN_NO_BEEP, GPIO.HIGH)
    GPIO.output(PIN_NO_LED, GPIO.HIGH)

# 多次哔声和LED发光封装函数，输入参数分别为“占空时间”以及重复次数
def beepAction(secs, sleepsecs, times):
    for i in range(times):
        beep(secs)
        time.sleep(sleepsecs)

while True:
    # 以下代码获取系统时间、时、分、秒、星期的数值
    t = time.localtime()
    h = t.tm_hour
    m = t.tm_min
    s = t.tm_sec
    w = time.strftime('%w',t)
    #print h,m,s,w
    time.sleep(0.3)
    # 判断是否为整点
    if m == 0 and s == 0:
        # 以下注释部分用于让报时的脚本跳过周六和周日（睡个懒觉放松下不容易）
        #if w==0 or w==6:
        #    continue
        # 以下代码判断当时间在晚间22点至早间8点期间不报时以免影响睡眠
        if h > 22 or h < 8:
            continue
        # 小时数N大于12点的情况下，哔N-12次
        if h > 12:
            h = h - 12
        beepAction (0.3, 0.5, h)
        time.sleep(1)
    # 判断是否为30分
    if m == 30 and s == 0:
        if h > 22 or h < 8:
            continue
        # 快节奏哔2声
        beepAction (0.05, 0.05, 2)
        time.sleep(1)