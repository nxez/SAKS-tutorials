#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 NXEZ.COM.
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

__author__ = 'Spoony'
__version__  = 'version 0.0.1'
__license__  = 'Copyright (c) 2016 NXEZ.COM'

from sakshat import SAKSHAT
import time
import commands
import sys, urllib, urllib2, json
import requests
import re

#Declare the SAKS Board
SAKS = SAKSHAT()

__current_mode = 0
__current_command = 0
__modes = [ 'display', '1' ]
__commands = { 'display': [ '.time', '.cputemp', '.roomtemp', '.citytemp', '.pm25', '.stockmarketindex' ], '1': [ '.0', '.1' ] }

__commands = { 'display': [ '.time', '.cputemp', '.roomtemp', '.stockmarketindex' ], '1': [ '.0', '.1' ] }
__current_command_name = ''
__processing_list = {}

def display_cpu_temp():
    global __current_command_name
    while True:
        if __current_command_name == 'display.cputemp':
            t = get_cpu_temp()
            # Uncomment if need print the temperature to screen
            #print("%.2f" % t)
            SAKS.digital_display.show("%.2f" % t)
            # set any value you want
            if t > 50:
                SAKS.buzzer.beepAction(0.02, 0.02, 20)
            time.sleep(1)
        else:
            __processing_list['display.cputemp'] = False
            break
        time.sleep(0.5)

def display_pm25():
    global __current_command_name
    while True:
        if __current_command_name == 'display.pm25':
            pm25 = get_pm25()
            if pm25 == -1:
                time.sleep(30)
                continue

            #严重污染，红灯亮蜂鸣器Beep
            if pm25 >= 250:
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(7)
                SAKS.buzzer.beepAction(0.05,0.05,3)
            #重度污染，红灯亮
            if pm25 < 250:
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(7)
            #中度污染，红灯亮
            if pm25 < 150:
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(7)
            #轻度污染，黄灯亮
            if pm25 < 115:
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(5)
            #良，1绿灯亮
            if pm25 < 75:
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(3)
            #优，2绿灯亮
            if pm25 < 35:
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(3)
                SAKS.ledrow.on_for_index(2)

            #print (("%4d" % pm25).replace(' ','#'))
            #数码管显示PM2.5数值
            SAKS.digital_display.show(("%4d" % pm25).replace(' ','#'))
            time.sleep(1800)
        else:
            __processing_list['display.pm25'] = False
            break

        time.sleep(0.5)

def display_city_temp():
    global __current_command_name
    while True:
        if __current_command_name == 'display.citytemp':
            temp = get_city_temp()
            #返回值为 -128.0 表示读取失败
            if temp == -128.0 :
                #10秒后再次尝试
                time.sleep(30)
                continue

            print (("%5.1f" % temp).replace(' ','#'))
            #数码管显示温度数值，5位(含小数点)、精确到小数点1后1位
            SAKS.digital_display.show(("%5.1f" % temp).replace(' ','#'))
            time.sleep(1800)
        else:
            __processing_list['display.citytemp'] = False
            break

        time.sleep(0.5)

def display_room_temp():
    global __current_command_name
    while True:
        if __current_command_name == 'display.roomtemp':
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
        else:
            __processing_list['display.roomtemp'] = False
            break

        time.sleep(0.5)

def display_time():
    global __current_command_name
    __dp = True
    __alarm_beep_status = False
    __alarm_beep_times = 0
    # 在这里设定闹钟定时时间
    __alarm_time = "18:10:00"

    while True:
        if __current_command_name == 'display.time':
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
                    #SAKS.ledrow.items[6].on()
                    __alarm_beep_times = __alarm_beep_times + 1
                    # 30次没按下停止键则自动停止闹铃
                    if __alarm_beep_times > 30:
                        __alarm_beep_status = False
                        __alarm_beep_times = 0
            else:
                SAKS.digital_display.show(("%02d%02d" % (h, m)))
                if __alarm_beep_status:
                    SAKS.buzzer.off()
                    #SAKS.ledrow.items[6].off()
            __dp = not __dp

            #time.sleep(0.5)
        else:
            __processing_list['display.time'] = False
            break

        time.sleep(0.5)

def display_stock_market_index():
    global __current_command_name
    while True:
        if __current_command_name == 'display.stockmarketindex':
            pattern = re.compile(r'(\d*\.\d*)')
            r = requests.get('http://hq.sinajs.cn/list=s_sh000001', timeout = 5)
            #print r.text.encode('utf-8')
            #print r.encoding
            match = pattern.findall(r.text)
            if match:
                SAKS.digital_display.show(("%04d" % int(float(match[0]))))
                #return match[0]
            else:
                SAKS.digital_display.show("###0")
                #return 0
        else:
            __processing_list['display.stockmarketindex'] = False
            break

        time.sleep(0.5)

def alarm_process():
    pass

def power_management_process():
    pass

def dip_switch_status_changed_handler(status):
    '''
    called while the status of dip switch changed
    :param status: current status
    :return: void
    '''
    print('on_dip_switch_status_changed:')
    print(status)
    pass

def tact_event_handler(pin, status):
    '''
    called while the status of tacts changed
    :param pin: pin number which stauts of tact is changed
    :param status: current status
    :return: void
    '''
    print('tact_event_handler')
    print("%d - %s" % (pin, status))
    global  __current_command
    global __current_command_name
    global __processing_list

    if __current_command >= len(__commands['display']):
        __current_command = 0

    __current_command_name = __modes[__current_mode] + __commands[__modes[__current_mode]][__current_command]
    print(__current_command_name)

    if __current_command_name == 'display.cputemp' and not __processing_list['display.cputemp']:
        __processing_list['display.cputemp'] = True
        display_cpu_temp()
    elif __current_command_name == 'display.pm25' and not __processing_list['display.pm25']:
        __processing_list['display.pm25'] = True
        display_pm25()
    elif __current_command_name == 'display.citytemp' and not __processing_list['display.citytemp']:
        __processing_list['display.citytemp'] = True
        display_city_temp()
    elif __current_command_name == 'display.roomtemp' and not __processing_list['display.roomtemp']:
        __processing_list['display.roomtemp'] = True
        display_room_temp()
    elif __current_command_name == 'display.time' and not __processing_list['display.time']:
        __processing_list['display.time'] = True
        display_time()
    elif __current_command_name == 'display.stockmarketindex' and not __processing_list['display.stockmarketindex']:
        __processing_list['display.stockmarketindex'] = True
        display_stock_market_index()
    else:
        print('ELSE:' + __current_command_name)


    __current_command += 1
    time.sleep(0.05)


#def handler(signum, frame):
#    SAKS.digital_display.off()
#    print "receive a signal %d"%(signum)

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000
    # Uncomment the next line if you want the temp in Fahrenheit
    #return float(1.8*cpu_temp)+32

def get_gpu_temp():
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    return float(gpu_temp)
    # Uncomment the next line if you want the temp in Fahrenheit
    # return float(1.8* gpu_temp)+32

'''
cityid 和 key 需要根据实际情况替换
参考 http://www.heweather.com/documents/api
http://www.heweather.com/documents/cn-city-list
'''
weather_url = 'https://api.heweather.com/x3/weather?cityid=CN101020100&key=xxx'
def get_pm25():
    global weather_url
    req = urllib2.Request(weather_url)
    resp = urllib2.urlopen(req, timeout = 5)
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

def get_city_temp():
    global weather_url
    req = urllib2.Request(weather_url)
    resp = urllib2.urlopen(req, timeout = 5)
    content = resp.read()
    if(content):
        weatherJSON = json.JSONDecoder().decode(content)
        #print(content)
        try:
            if weatherJSON['HeWeather data service 3.0'][0]['status'] == "ok":
                if weatherJSON['HeWeather data service 3.0'][0].has_key('now'):
                    print(weatherJSON['HeWeather data service 3.0'][0]['now']['tmp'])
                    return int(weatherJSON['HeWeather data service 3.0'][0]['now']['tmp'])
                else:
                    return -128
            else:
                return -128
        except:
            return -128

if __name__ == "__main__":
    print("main")
    #SAKS = SAKSController()
    #print(PINS.BUZZER)
    #print(SAKS.appRoot)

    __processing_list['display.cputemp'] = False
    __processing_list['display.pm25'] = False
    __processing_list['display.citytemp'] = False
    __processing_list['display.roomtemp'] = False
    __processing_list['display.time'] = False
    __processing_list['display.stockmarketindex'] = False

    SAKS.dip_switch_status_changed_handler = dip_switch_status_changed_handler
    SAKS.tact_event_handler = tact_event_handler

    time.sleep(0.5)
    print(SAKS.ds18b20.temperature)
    #SAKS.digital_display.show('#.1#.234')
    #print(SAKS.dip_switch.is_on)

    # 将显示“1234”4位数字，并且每一位右下角的小点点亮
    SAKS.digital_display.show("1.2.3.4.")
    time.sleep(0.5)
    # 在第4位数码管显示“1”，其他3位数码管不显示
    SAKS.digital_display.show("###1")
    time.sleep(0.5)
    SAKS.digital_display.off()

    input("Enter any keys to exit...")
