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

class SAKSPins(object):
    '''
    SAKS Pins Code With BCM for Raspberry Pi Model B.
    '''
    '''
    _inst = None
    def __new__(cls, var ):
        if cls._inst is None:
            cls._inst = object.__new__(cls)
            cls._inst.var = var
        return cls._inst
    instance = pinstable()
    def __new__(cls):
        if cls._inst is None:
            cls._inst = object.__new__(cls)
        return cls._inst
    '''

    LED_BLUE_1 = 5
    LED_BLUE_2 = 6
    LED_BLUE_3 = 13
    LED_BLUE_4 = 19
    LED_GREEN_1 = 0
    LED_GREEN_2 = 1
    LED_YELLOW = 7
    LED_RED = 8

    BUZZER = 11

    TACT_RIGHT = 23
    TACT_LEFT = 18
    DIP_SWITCH_1 = 24
    DIP_SWITCH_2 = 25

    DIGITAL_DISPLAY_A = 21
    DIGITAL_DISPLAY_B = 16
    DIGITAL_DISPLAY_C = 19
    DIGITAL_DISPLAY_D = 6
    DIGITAL_DISPLAY_E = 5
    DIGITAL_DISPLAY_F = 20
    DIGITAL_DISPLAY_G = 26
    DIGITAL_DISPLAY_DP = 13
    DIGITAL_DISPLAY_SELECET_1 = 17
    DIGITAL_DISPLAY_SELECET_2 = 27
    DIGITAL_DISPLAY_SELECET_3 = 22
    DIGITAL_DISPLAY_SELECET_4 = 10

    IR_SENDER = 12
    IR_RECEIVER = 9
    DS18B20 = 4
    UART_TXD = 14
    UART_RXD = 15
    I2C_SDA = 2
    I2C_SLC = 3

    LEDS = (
        LED_BLUE_1,
        LED_BLUE_2,
        LED_BLUE_3,
        LED_BLUE_4,
        LED_GREEN_1,
        LED_GREEN_2,
        LED_YELLOW,
        LED_RED
    )

    DIGITAL_DISPLAY = (
        DIGITAL_DISPLAY_A,
        DIGITAL_DISPLAY_B,
        DIGITAL_DISPLAY_C,
        DIGITAL_DISPLAY_D,
        DIGITAL_DISPLAY_E,
        DIGITAL_DISPLAY_F,
        DIGITAL_DISPLAY_G,
        DIGITAL_DISPLAY_DP
    )

    DIGITAL_DISPLAY_SELECT = (
        DIGITAL_DISPLAY_SELECET_1,
        DIGITAL_DISPLAY_SELECET_2,
        DIGITAL_DISPLAY_SELECET_3,
        DIGITAL_DISPLAY_SELECET_4,
    )
