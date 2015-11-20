#!/usr/bin/python3
"""
Copyright (C) 2015 Michael G. Dorner

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>. 
"""
import sys
import os
import time
import tablet_control as tc
from os import path

def open_all_accelerometers(devices):
    """
    Open all accelerometer device files
    
    devices: the directory of the devices
    
    return: the accelerometers
    """
    accels = []
    for accel in devices:
        x, y, scale = open_accelerometer(accel)
        accels.append((x,y,scale))
    return accels

def close_all_accelerometers(accels):
    """Close all accelerometer files"""
    for accel in accels:
        close_accelerometer(accel)

def open_accelerometer(name):
    """
    Open a particular accelerometer's device files
    
    name: the path to the accelerometer

    return: the opened files
    """
    x_axis = open(path.join(name, 'in_accel_x_raw'))
    y_axis = open(path.join(name, 'in_accel_y_raw'))
    scale = open(path.join(name, 'in_accel_scale'))
    return x_axis, y_axis, scale

def close_accelerometer(accel):
    """
    Close a particular accelerometer
    """
    for desc in accel:
        desc.close()

def accels_readable(accels):
    """
    Check if the accelerometer's files are readable

    accels: file-handles for the accelerometers

    return: whether the handles are readable
    """
    ret = True
    for accel in accels:
        x,y,scale = accel
        ret &= x.readable() and y.readable() and scale.readable()
        #need to insert code to check whether the accel can bke read or not
        return True

def read_accel(accel):
    """
    Read x and y value from accelerometer

    accel: the accelerometer

    return: the x and y value as well as the scale value as tuple
    """
    for desc in accel:
        desc.seek(0)
    x,y,scale = accel
    scaleValue = float(scale.read())
    xValue = float(x.read()) * scaleValue
    yValue = float(y.read()) * scaleValue
    return (xValue, yValue, scaleValue)

def determine_mode(accel):
    """
    Logic implementing the mode detection based on the x,y and scale values

    accel: the accelerometer

    return: the mode as a string
    """
    xVal, yVal, scaleVal = read_accel(accel)
#	print("x: " + str(xVal) + " y: " + str(yVal) +
#				 " scale: " + str(scaleVal))
        #fairly horizontal position
    if abs(xVal) < 4.5:
    #display is upright
        if yVal < -4:
             mode = "normal"
                #display is ~180 deg open
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

def find_accelerometers(device_path="/sys/bus/iio/devices/"):
    """
    Locate accelerometers in the device path

    device_path: the location where the files from which the value can be read
    are found
    
    return: a list of accelerometer
    """
    accelerometers = []
    for directory in os.listdir(device_path):
        with open(path.join(device_path, directory, 'name')) as candidate:
            if "iio:device" in directory and "accel" in candidate.read():
                accelerometers.append(path.join(device_path,directory))
    return accelerometers

def main(conf="/etc/autotablet/inputDevices.json"):
    devices = tc.load_device_configuration(conf)
#    print("Found accelerometers: " + str(accelerometers))
    accels = open_all_accelerometers(find_accelerometers())
    previous = "unknown"
    try:
        while(accels_readable(accels)):
            for accel in accels:
                mode = determine_mode(accel)
                if mode != previous or not ok:
                    ok = switch_mode(devices, mode)
                    time.sleep(1.0)
                    previous = mode
    except OSError:
        print("Cannot recover from error" + str(sys.exc_info()[0]))
        tc.set_normal(devices)
        close_all_accelerometers(accels)	
        sys.exit(1)
    tc.set_normal(devices)
    close_all_accelerometers(accels)	

if __name__ == '__main__':
    main()

