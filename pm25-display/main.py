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
# tutorials url: http://shumeipai.nxez.com/2015/10/07/saks-diy-tutorials-pm25-display-and-alarm.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

from sakshat import SAKSHAT
import time
import sys, urllib, urllib2, json

#Declare the SAKS Board
SAKS = SAKSHAT()
'''
cityid 和 key 需要根据实际情况替换
参考 http://www.heweather.com/documents/api
http://www.heweather.com/documents/cn-city-list
'''
weather_url = 'https://api.heweather.com/x3/weather?cityid=CN101020100&key=xxx'

def get_pm25():
    global weather_url
    req = urllib2.Request(weather_url)
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        weatherJSON = json.JSONDecoder().decode(content)
        #print(content)
        try:
            if weatherJSON['HeWeather data service 3.0'][0]['status'] == "ok":
                if weatherJSON['HeWeather data service 3.0'][0].has_key('aqi'):
                    print(weatherJSON['HeWeather data service 3.0'][0]['aqi']['city']['pm25'])
                    return int(weatherJSON['HeWeather data service 3.0'][0]['aqi']['city']['pm25'])
                else:
                    return -1
            else:
                return -1
        except:
            return -1

if __name__ == "__main__":
    while True:
        pm25 = get_pm25()
        if pm25 == -1:
            time.sleep(30)
            continue

        #严重污染，红灯亮蜂鸣器Beep
        if pm25 >= 250:
            SAKS.ledrow.off()
            SAKS.ledrow.items[7].on()
            SAKS.buzzer.beepAction(0.05,0.05,3)
        #重度污染，红灯亮
        if pm25 < 250:
            SAKS.ledrow.off()
            SAKS.ledrow.items[7].on()
        #中度污染，红灯亮
        if pm25 < 150:
            SAKS.ledrow.off()
            SAKS.ledrow.items[7].on()
        #轻度污染，黄灯亮
        if pm25 < 115:
            SAKS.ledrow.off()
            SAKS.ledrow.items[6].on()
        #良，1绿灯亮
        if pm25 < 75:
            SAKS.ledrow.off()
            SAKS.ledrow.items[4].on()
        #优，2绿灯亮
        if pm25 < 35:
            SAKS.ledrow.off()
            SAKS.ledrow.items[4].on()
            SAKS.ledrow.items[5].on()

        #print (("%4d" % pm25).replace(' ','#'))
        #数码管显示PM2.5数值
        SAKS.digital_display.show(("%4d" % pm25).replace(' ','#'))
        time.sleep(1800)
    input("Enter any keys to exit...")