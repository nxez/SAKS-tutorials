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

import RPi.GPIO as GPIO
import time
import re
from threading import Thread

class DigitalDisplay(object):
    '''
    Digital display class
    '''
    __pins = {'seg':[], 'sel':[]}
    __real_true = GPIO.HIGH
    __numbers = []
    __is_flushing = False
    __number_code = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x00]
    __pin_stat = {}

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the digital display
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pins = pins
        self.__real_true = real_true
        try:
            t1 = Thread(target = self.flush_4bit)
            t1.setDaemon(True)
            t1.start()
        except:
            print "Error: Unable to start thread by DigitalDisplay"

    #Stauts.
    @property
    def numbers(self):
        '''
        Get the current numbers array showing
        :return: numbers array
        '''
        return self.__numbers

    #@numbers.setter
    def set_numbers(self, value):
        '''
        Set the numbers array to show
        :return: void
        '''
        pattern = re.compile(r'[#|\d]\.?')
        matches = pattern.findall(value)
        #del self.__numbers
        self.__numbers = []
        for i in range(len(matches)):
            self.__numbers.append(matches[i])
        #print(self.__numbers)

    #@numbers.deleter
    #def numbers(self):
    #    del self.__numbers

    #Verbs.
    def on(self):
        '''
        Set display on
        :return: void
        '''
        self.__is_flushing = True

    def off(self):
        '''
        Set display off
        :return: void
        '''
        self.__is_flushing = False
        for p in self.__pins['sel'] + self.__pins['seg']:
            self.set_pin(p, False)

    def show(self, str):
        '''
        Set the numbers array to show and enable the display
        :return: void
        '''
        self.__is_flushing = False
        self.set_numbers(str)
        self.__is_flushing = True
        #print(self.__numbers)

    def set_pin(self, pin, v):
        ' More stable digital display, fixed by wyb. '
        if v or not pin in self.__pin_stat or v != self.__pin_stat[pin]:
            self.__pin_stat[pin] = v
            if v:
                GPIO.output(pin, GPIO.LOW)
            else:
                GPIO.output(pin, GPIO.HIGH)
    
    def flush_bit(self, sel, num, dp):
        if num == '#' or num == '':
            self.set_pin(self.__pins['sel'][sel], False)
            return

        n = self.__number_code[int(num)]
        if dp:
            n = n | 0x80

        for i in range(8):
            j = self.__pins['seg'][i]
            v = ((n & (1 << i)) != 0)
            if v != self.__pin_stat[j]:
                for k in range(4):
                    self.set_pin(self.__pins['sel'][k], False)
            self.set_pin(j, v)

        self.set_pin(self.__pins['sel'][sel], True)

    def flush_4bit(self):
        for p in self.__pins['seg'] + self.__pins['sel']:
            self.set_pin(p, False)
        while True:
            if self.__is_flushing:
                #print(self.__numbers)
                #print(range(min(4, len(self.__numbers))))
                try:
                    for i in range(min(4, len(self.__numbers))):
                        self.flush_bit(i, self.__numbers[i].replace('.',''), True if self.__numbers[i].count('.') > 0 else False)
                        time.sleep(0.005)
                except:
                    pass
            else:
                time.sleep(0.02)
