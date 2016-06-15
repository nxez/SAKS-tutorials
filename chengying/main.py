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

#Declare the SAKS Board
SAKS = SAKSHAT()

__current_mode = 0
__current_command = 0
#__mode = [ '0', '1' ]
__command = { '0': [ '.0', '.1' ], '1': [ '.0', '.1' ] }

def display_cpu_temp():
    while True:
        if __current_mode + __current_command == '':
            t = get_cpu_temp()
            # Uncomment if need print the temperature to screen
            #print("%.2f" % t)
            SAKS.digital_display.show("%.2f" % t)
            # set any value you want
            if t > 50:
                SAKS.buzzer.beepAction(0.02, 0.02, 20)
            time.sleep(1)
        else:
            break

def display_pm25():
    while True:
        if __current_mode + __current_command == '':
            pm25 = get_pm25()
            if pm25 == -1:
                time.sleep(30)
                continue

            #严重污染，红灯亮蜂鸣器Beep
            if pm25 >= 250:
                SAKS.ledrow.off()
                #SAKS.ledrow.items[7].on()
                SAKS.buzzer.beepAction(0.05,0.05,3)
            #重度污染，红灯亮
            if pm25 < 250:
                SAKS.ledrow.off()
                #SAKS.ledrow.items[7].on()
            #中度污染，红灯亮
            if pm25 < 150:
                SAKS.ledrow.off()
                #SAKS.ledrow.items[7].on()
            #轻度污染，黄灯亮
            if pm25 < 115:
                SAKS.ledrow.off()
                #SAKS.ledrow.items[6].on()
            #良，1绿灯亮
            if pm25 < 75:
                SAKS.ledrow.off()
                #SAKS.ledrow.items[4].on()
            #优，2绿灯亮
            if pm25 < 35:
                SAKS.ledrow.off()
                #SAKS.ledrow.items[4].on()
                #SAKS.ledrow.items[5].on()

            #print (("%4d" % pm25).replace(' ','#'))
            #数码管显示PM2.5数值
            SAKS.digital_display.show(("%4d" % pm25).replace(' ','#'))
            time.sleep(1800)
        else:
            break

def display_city_temp():
    while True:
        if __current_mode + __current_command == '':
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
            break

def display_room_temp():
    while True:
        if __current_mode + __current_command == '':
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
            break

def display_time():
    __dp = True
    __alarm_beep_status = False
    __alarm_beep_times = 0
    # 在这里设定闹钟定时时间
    __alarm_time = "18:10:00"

    while True:
        if __current_mode + __current_command == '':
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

            time.sleep(0.5)
        else:
            break

def display_stock_market_index():
    if __current_mode + __current_command == '':
        pass
    pass

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

def get_city_temp():
    global weather_url
    req = urllib2.Request(weather_url)
    resp = urllib2.urlopen(req)
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
    SAKS.dip_switch_status_changed_handler = dip_switch_status_changed_handler
    SAKS.tact_event_handler = tact_event_handler
    b = SAKS.buzzer
    b.beep(1)
    #SAKS.ledrow.ic.set_data(0x08)
    SAKS.ledrow.on()
    time.sleep(3)
    SAKS.ledrow.off()
    time.sleep(3)
    SAKS.ledrow.set_row([True, False, True, False, True, False, True, False])
    time.sleep(2)
    SAKS.ledrow.set_row([None, True, False, None, None, None, None, True])
    print( SAKS.ledrow.row_status)
    print( SAKS.ledrow.is_on(1))
    print( SAKS.ledrow.is_on(2))

    print( SAKS.ledrow.is_on(3))
    print( SAKS.ledrow.is_on(4))

    #SAKS.ledrow.items[7].flashAction(0.02,0.02,30)
    #SAKS.ledrow.on()
    print(SAKS.ds18b20.temperature)
    #SAKS.digital_display.show('#.1#.234')
    #print(SAKS.dip_switch.is_on)

    # 将显示“1234”4位数字，并且每一位右下角的小点点亮
    SAKS.digital_display.show("1.2.3.4.")
    time.sleep(1)
    # 将显示“1234”4位数字，并且数字2后面的小点点亮
    SAKS.digital_display.show("12.34")
    time.sleep(1)
    # 在第4位数码管显示“1”，其他3位数码管不显示
    SAKS.digital_display.show("###1")
    time.sleep(1)
    SAKS.digital_display.off()
    time.sleep(2)
    SAKS.digital_display.on()

    '''
    while True:
        SAKS.digital_display.show("%d%d%d%d" % (time.gmtime().tm_min / 10, time.gmtime().tm_min % 10, time.gmtime().tm_sec / 10, time.gmtime().tm_sec % 10))
        time.sleep(0.5)
    '''

    '''
    while True:
        t = get_cpu_temp()
        print("%3.1f" % t)
        #SAKS.digital_display.show("%3.2f" % t)
        if t > 38:
            b.beepAction(0.02,0.02,30)
        time.sleep(1)
    '''

    input("Enter any keys to exit...")
