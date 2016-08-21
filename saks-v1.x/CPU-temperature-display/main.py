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
# tutorials url: http://shumeipai.nxez.com/2015/09/21/saks-diy-tutorials-cpu-temperature-display-and-alarm.html

__author__ = 'Spoony'
__license__  = 'Copyright (c) 2015 NXEZ.COM'

from sakshat import SAKSHAT
import time
import commands

#Declare the SAKS Board
SAKS = SAKSHAT()

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp) / 1000
    # Uncomment the next line if you want the temp in Fahrenheit
    #return float(1.8*cpu_temp)+32

def get_gpu_temp():
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    return float(gpu_temp)
    # Uncomment the next line if you want the temp in Fahrenheit
    # return float(1.8* gpu_temp)+32

if __name__ == "__main__":
    while True:
        t = get_cpu_temp()
        # Uncomment if need print the temperature to screen
        #print("%.2f" % t)
        SAKS.digital_display.show("%.2f" % t)
        # set any value you want
        if t > 50:
            SAKS.buzzer.beepAction(0.02,0.02,30)
        time.sleep(1)

    input("Enter any keys to exit...")
