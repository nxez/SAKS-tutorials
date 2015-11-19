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
# tutorials url: http://shumeipai.nxez.com/2015/04/05/saks-diy-tutorials-reboot-button.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

import RPi.GPIO as GPIO
import time
import os,sys
import signal

#定义关机键和关机状态指示灯的GPIO引脚
GPIO.setmode(GPIO.BCM)
pin_btn = 23
pin_led_reboot = 7
pin_led_halt = 8

#初始化SAKS上相应按键和LED的状态，按键内部上拉、LED不亮
GPIO.setup(pin_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin_led_reboot, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(pin_led_halt, GPIO.OUT, initial = GPIO.HIGH)

#初始化按下关机键的次数
press_times = 0
#按下关机键后等待并倒数10次
count_down = 10
led_on_reboot = 0
led_on_halt = 0

def onPress(channel):
    global press_times, count_down
    print('pressed')
    press_times += 1
    if press_times > 3:
        press_times = 1
    #重启模式
    if press_times == 1:
        GPIO.output(pin_led_reboot, 0)
        GPIO.output(pin_led_halt, 1)
        print('system will restart in %s' % (count_down))
    #关机模式
    elif press_times == 2:
        GPIO.output(pin_led_reboot, 1)
        GPIO.output(pin_led_halt, 0)
        print('system will halt in %s' % (count_down))
    #模式取消
    elif press_times == 3:
        GPIO.output(pin_led_reboot, 1)
        GPIO.output(pin_led_halt, 1)
        print 'cancel'
        count_down = 10

#设置按键检测，检测到按下时调用 onPress 函数
GPIO.add_event_detect(pin_btn, GPIO.FALLING, callback = onPress, bouncetime = 500)

try:
    while True:
        #重启模式
        if press_times == 1:
            if count_down == 0:
                print "start restart"
                os.system("shutdown -r -t 5 now")
                sys.exit()
            led_on_reboot = not led_on_reboot
            #黄色 LED 闪烁
            GPIO.output(pin_led_reboot, led_on_reboot)
        #关机模式
        if press_times == 2:
            if count_down == 0:
                print "start shutdown"
                os.system("shutdown  -t 5 now")
                sys.exit()
            led_on_halt = not led_on_halt
            #红色 LED 闪烁
            GPIO.output(pin_led_halt, led_on_halt)

        if press_times == 1 or press_times == 2:
            count_down -= 1
            print "%s second" % (count_down)
        time.sleep(1)
except KeyboardInterrupt:
    print('User press Ctrl+c, exit;')
finally:
    GPIO.cleanup()