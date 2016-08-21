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
# tutorials url: http://shumeipai.nxez.com/2015/11/18/saks-diy-tutorials-breathing-light.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(0, GPIO.OUT)
# 默认点亮LED表示正在检测进程
GPIO.output(0, GPIO.LOW)
pwm = GPIO.PWM(0, 50)
pwm.start(0)
pause_time = 0.01

def process_exist():
    proc = subprocess.Popen("ps aux | grep wget", stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    stdout = proc.communicate()
    for line in stdout:
        if line.count('http') > 0:
            #print(line)
            return True

    return False

try:
    while True:
        if process_exist():
            for i in xrange(0, 101, 1):
                pwm.ChangeDutyCycle(i)
                # off
                time.sleep(pause_time)

            time.sleep(1)

            for i in xrange(100, -1, -1):
                pwm.ChangeDutyCycle(i)
                # on
                time.sleep(pause_time)
        else:
            time.sleep(pause_time * 10)

except KeyboardInterrupt:
    # stop the white PWM output
    pwm.stop()
    # clean up GPIO on CTRL+C exit
    GPIO.cleanup()