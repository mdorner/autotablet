#!/usr/bin/python3
"""
Copyright (C) 2015 Michael G. Dorner

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>. 
"""
import sys
import tablet_control as tc
import accelerometers as acmon
from os import path
from time import sleep

def determine_mode(accel):
    """
    Logic implementing the mode detection based on the x,y and scale values

    accel: the accelerometer

    return: the mode as a string
    """
    xVal, yVal, zVal, scaleVal = acmon.read_accel(accel)
#	print("x: " + str(xVal) + " y: " + str(yVal) +
#				 " scale: " + str(scaleVal))
        #fairly horizontal position
    if zVal > 7:
        #display facing ground, i.e. assumed closing lid/opening it
        mode = "normal"
    elif abs(xVal) < 4.5:
    #display is in wide orientation
        if yVal < -4:
             mode = "normal"
        elif yVal < 1:
                mode = "scratchpad"	
        elif yVal < 6:
                mode = "itablet"
        elif yVal < 10:
                mode = "tent"	
        else:
                mode = "unknown"
    else:
        if xVal > 0:
            mode = "ltablet"
        else:
            mode = "rtablet"
    return mode

def switch_mode(devices, mode):
    """
    Call the mode's configuration routine defined in the tc module based on the 
    mode.

    devices: the devices we modify
    mode: the mode the device is in

    return: whether the operation was a success
    """
    ret = False
    if "tablet" in mode:
        if mode.startswith("i"):
            ret = tc.set_tablet(devices, "inverted")
        elif mode.startswith("l"):
            ret =  tc.set_tablet(devices, "left")
        elif mode.startswith("r"):
            ret =  tc.set_tablet(devices, "right")
    else:
        if mode == "tent":
            ret = tc.set_tent(devices)
        elif mode == "scratchpad":
            ret = tc.set_scratchpad(devices)
        elif mode == "normal":
            ret = tc.set_normal(devices)
    return ret


def main(conf="/etc/autotablet/inputDevices.json"):
    devices = tc.load_device_configuration(conf)
#    print("Found accelerometers: " + str(accelerometers))
    accels = acmon.get_acceleromters("/sys/bus/iio/devices/") 
    previous = "unknown"
    try:
        while(acmon.accels_readable(accels)):
            for accel in accels:
                mode = determine_mode(accel)
                if mode != previous or not ok:
                    ok = switch_mode(devices, mode)
                    sleep(1.0)
                    previous = mode
    except OSError:
        print("Cannot recover from error" + str(sys.exc_info()[0]))
        tc.set_normal(devices)
        acmon.close_all_accelerometers(accels)	
        sys.exit(1)
    tc.set_normal(devices)
    acmon.close_all_accelerometers(accels)	

if __name__ == '__main__':
    main()

