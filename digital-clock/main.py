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

dp = True
alarm_beep = False

if __name__ == "__main__":
    while True:
        # 以下代码获取系统时间、时、分、秒、星期的数值
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        w = time.strftime('%w',t)
        #print h,m,s,w

        '''
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
            SAKS.buzzer.beepAction (0.3, 0.5, h)
        '''

        if dp:
            #数码管显示小时和分，最后一位的小点每秒闪烁一次
            SAKS.digital_display.show(("%0d%0d." % (h, m)))
        else:
            SAKS.digital_display.show(("%0d%0d" % (h, m)))
        dp = not dp

        time.sleep(0.5)
    input("Enter any keys to exit...")