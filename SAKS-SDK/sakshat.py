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

__author__ = 'Spoony'
__version__  = 'version 0.0.1'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

import os
import sys
#sys.path.append(sys.path[0] + "/entities/")
#from entities import *
import RPi.GPIO as GPIO
from sakspins import SAKSPins as PINS
import entities

class SAKSHAT(object):
    '''
    SAKS HAT class, some useful function are declared.
    '''
    #appRoot = sys.path[0]
    buzzer = None
    ledrow = None
    ds18b20 = None
    digital_display = None
    dip_switch = None
    tactrow = None

    def saks_gpio_init(self):
        print 'saks_gpio_init'
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PINS.BUZZER, GPIO.OUT)
        GPIO.output(PINS.BUZZER, GPIO.HIGH)

        for p in [PINS.BUZZER, PINS.TACT_RIGHT, PINS.TACT_LEFT, PINS.DIP_SWITCH_1, PINS.DIP_SWITCH_2]:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, GPIO.HIGH)

        for p in PINS.LEDS + PINS.DIGITAL_DISPLAY + PINS.DIGITAL_DISPLAY_SELECT:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, GPIO.HIGH)

        for p in [PINS.TACT_RIGHT, PINS.TACT_LEFT, PINS.DIP_SWITCH_1, PINS.DIP_SWITCH_2]:
            GPIO.setup(p, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            #GPIO.setup(p, GPIO.IN)

        #由于SAKS的蓝色LED和数码管共享引脚，此处将数码管位选关闭，只让信号作用于LED
        #GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)
        #GPIO.setup(27, GPIO.OUT, initial = GPIO.HIGH)
        #GPIO.setup(22, GPIO.OUT, initial = GPIO.HIGH)
        #GPIO.setup(10, GPIO.OUT, initial = GPIO.HIGH)

    def __init__(self):
        self.saks_gpio_init()
        self.buzzer = entities.Buzzer(PINS.BUZZER, GPIO.LOW)
        self.ledrow = entities.LedRow(PINS.LEDS, GPIO.LOW)
        self.ds18b20 = entities.DS18B20(PINS.DS18B20)
        self.digital_display = entities.DigitalDisplay({'seg': PINS.DIGITAL_DISPLAY, 'sel': PINS.DIGITAL_DISPLAY_SELECT}, GPIO.LOW)
        self.dip_switch = entities.DipSwitch2Bit([PINS.DIP_SWITCH_1, PINS.DIP_SWITCH_2], GPIO.LOW)
        self.dip_switch.register(self)
        self.tactrow = entities.TactRow([PINS.TACT_LEFT, PINS.TACT_RIGHT], GPIO.LOW)
        for t in self.tactrow.items:
            t.register(self)

        #print('self.dip_switch.register(self)')

    dip_switch_status_changed_handler = None
    def on_dip_switch_2bit_status_changed(self, status):
        #print('on_dip_switch_2bit_status_changed')
        if self.dip_switch_status_changed_handler is not None:
            self.dip_switch_status_changed_handler(status)

    tact_event_handler = None
    def on_tact_event(self, pin, status):
        #print('on_tact_event')
        if self.tact_event_handler is not None:
            self.tact_event_handler(pin, status)
