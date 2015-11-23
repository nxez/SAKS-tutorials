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
# tutorials url: http://shumeipai.nxez.com/2015/10/11/saks-diy-tutorials-digital-clock.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

from sakshat import SAKSHAT
import time

#Declare the SAKS Board
SAKS = SAKSHAT()

__dp = True
__alarm_beep_status = False
__alarm_beep_times = 0
# 在这里设定闹钟定时时间
__alarm_time = "18:10:00"

#在检测到轻触开关触发时自动执行此函数
def tact_event_handler(pin, status):
    '''
    called while the status of tacts changed
    :param pin: pin number which stauts of tact is changed
    :param status: current status
    :return: void
    '''
    global __alarm_beep_status
    global __alarm_beep_times
    # 停止闹钟响铃（按下任何轻触开关均可触发）
    __alarm_beep_status = False
    __alarm_beep_times = 0
    SAKS.buzzer.off()
    SAKS.ledrow.items[6].off()

if __name__ == "__main__":
    #设定轻触开关回调函数
    SAKS.tact_event_handler = tact_event_handler
    SAKS.buzzer.off()
    SAKS.ledrow.items[6].off()
    while True:
        # 以下代码获取系统时间、时、分、秒、星期的数值
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        w = time.strftime('%w',t)
        #print h,m,s,w
        print "%02d:%02d:%02d" % (h, m, s)

        if ("%02d:%02d:%02d" % (h, m, s)) == __alarm_time:
            __alarm_beep_status = True
            __alarm_beep_times = 0

        if __dp:
            # 数码管显示小时和分，最后一位的小点每秒闪烁一次
            SAKS.digital_display.show(("%02d%02d." % (h, m)))
            # 判断是否应该响起闹钟
            if __alarm_beep_status:
                SAKS.buzzer.on()
                SAKS.ledrow.items[6].on()
                __alarm_beep_times = __alarm_beep_times + 1
                # 30次没按下停止键则自动停止闹铃
                if __alarm_beep_times > 30:
                    __alarm_beep_status = False
                    __alarm_beep_times = 0
        else:
            SAKS.digital_display.show(("%02d%02d" % (h, m)))
            if __alarm_beep_status:
                SAKS.buzzer.off()
                SAKS.ledrow.items[6].off()
        __dp = not __dp

        time.sleep(0.5)
    input("Enter any keys to exit...")