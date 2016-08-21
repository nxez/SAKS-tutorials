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
# tutorials url: http://shumeipai.nxez.com/2015/10/24/saks-diy-tutorials-nightlight.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import time

#Declare the SAKS Board
SAKS = SAKSHAT()
#当前开关状态
__light_status = False

#在检测到拨码开关状态被修改时自动执行此函数
def dip_switch_status_changed_handler(status):
    '''
    called while the status of dip switch changed
    :param status: current status
    :return: void
    '''
    global __light_status
    #在小灯状态开着时执行
    if __light_status:
        #拨码开关第1位状态为ON
        if status[0]:
            #点亮第3个LED
            SAKS.ledrow.items[2].on()
        else:
            SAKS.ledrow.items[2].off()

        #拨码开关第2位状态为ON
        if status[1]:
            #点亮第4个LED
            SAKS.ledrow.items[3].on()
        else:
            SAKS.ledrow.items[3].off()

    #print(status)

#在检测到轻触开关触发时自动执行此函数
def tact_event_handler(pin, status):
    '''
    called while the status of tacts changed
    :param pin: pin number which stauts of tact is changed
    :param status: current status
    :return: void
    '''
    global __light_status
    #判断是否是右边的轻触开关被触发，并且是在被按下
    if pin == PINS.TACT_RIGHT and status == True:
        #在小灯当前状态关着时将它们点亮并修改小灯当前状态为开; 在小灯当前状态开着时将它们灭掉并修改小灯当前状态为关
        if not __light_status:
            SAKS.ledrow.items[0].on()
            SAKS.ledrow.items[1].on()
            #检测第1位拨码开关状态是否为ON
            if SAKS.dip_switch.is_on[0] == True:
                #点亮第3个LED
                SAKS.ledrow.items[2].on()
            #检测第2位拨码开关状态是否为ON
            if SAKS.dip_switch.is_on[1] == True:
                #点亮第4个LED
                SAKS.ledrow.items[3].on()
        else:
            SAKS.ledrow.items[0].off()
            SAKS.ledrow.items[1].off()
            SAKS.ledrow.items[2].off()
            SAKS.ledrow.items[3].off()

        __light_status = not __light_status

    #print("%d - %s" % (pin, status))


if __name__ == "__main__":
    #设定拨码开关回调函数
    SAKS.dip_switch_status_changed_handler = dip_switch_status_changed_handler
    #设定轻触开关回调函数
    SAKS.tact_event_handler = tact_event_handler
    input("Enter any keys to exit...")