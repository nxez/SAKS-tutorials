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
# tutorials url: http://shumeipai.nxez.com/2015/10/11/saks-diy-tutorials-temperature-display-ds18b20.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

from sakshat import SAKSHAT
import time

#Declare the SAKS Board
SAKS = SAKSHAT()

if __name__ == "__main__":
    while True:
        #从 ds18b20 读取温度（摄氏度为单位）
        temp = SAKS.ds18b20.temperature
        #返回值为 -128.0 表示读取失败
        if temp == -128.0 :
            #10秒后再次尝试
            time.sleep(10)
            continue

        print (("%5.1f" % temp).replace(' ','#'))
        #数码管显示温度数值，5位(含小数点)、精确到小数点1后1位
        SAKS.digital_display.show(("%5.1f" % temp).replace(' ','#'))
        time.sleep(5)
    input("Enter any keys to exit...")