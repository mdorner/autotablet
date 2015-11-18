#!/usr/bin/python3
"""
Copyright (C) 2015 Michael G. Dorner

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>. 
"""
import subprocess
import sys
import time
import json

#TODO: replace "handle failure" comments with logging suitable for a daemon

#coordination transformation matrices for different orientations
ctms = {
        #row major representation, inputs are multiplied with this matrix
        #this allows them to be correctly translated to the orientation
        "normal":  "1 0 0 0 1 0 0 0 1",
        "left":    "0 -1 1 1 0 0 0 0 1",
        "right":   "0 1 0 -1 0 1 0 0 1",
        "inverted": "-1 0 1 0 -1 1 0 0 1" 
        }

def rotate_input(device, orientation):
    if orientation not in ctms:
        print("No such orientation")
   #this construction is necessary because every one of the matrix entries
        #has to be passed as single parameter not as one string
    args = ["xinput", "set-prop", device, "Coordinate Transformation Matrix"]
    for entry in ctms[orientation].split(" "):
        args.append(entry)
    return subprocess.call(args) == 0

def rotate_screen(orientation):
    #change orientation to one of normal, left, right, inverse
    return subprocess.call(["xrandr", "-o", "%s" % orientation]) == 0

def xinput_device_action(device, action):
    #call a simple actions such as enable or disable for a device
    return subprocess.call(["xinput","%s" %action,"%s" % device]) == 0

def set_normal(devices):
    all_ok = True
    ret = rotate_screen("normal")
    all_ok &= ret
    for category, items in devices.items():
        for dev in items:
           ret = xinput_device_action(dev, "enable")
           all_ok &= ret
           if category != 'keyboards':
               ret = rotate_input(dev, "normal")
               all_ok &= ret
    return all_ok

#effectively identical to setTabled("inverted")
def set_tent(devices):
    all_ok = True
    ret = rotate_screen("inverted")
    all_ok &= ret
    for category, items in devices.items():
        if category in ["keyboards","trackpoints", "touchpads"]:
            for dev in items:
                ret = xinput_device_action(dev, "disable")
                all_ok &= ret
        else:
            for dev in items:
                ret = xinput_device_action(dev, "enable")
                all_ok &= ret
                ret = rotate_input(dev, "inverted")	
                all_ok &= ret
    return all_ok

def set_tablet(devices, orientation):
    all_ok = True
    ret = rotate_screen(orientation)
    all_ok &= ret
    for category, items in devices.items():
        if category in ["keyboards","trackpoints", "touchpads"]:
            for dev in items:
                ret = xinput_device_action(dev, "disable")
                all_ok &= ret
        else:
            for dev in items:
                ret = xinput_device_action(dev, "enable")
                all_ok &= ret
                ret = rotate_input(dev, orientation)
                all_ok &= ret
    return all_ok

def set_scratchpad(devices):
    rotate_screen("normal")
    all_ok = True
    for category, items in devices.items():
        if category in ["trackpoints", "touchpads", "touchscreens"]:
            for dev in items:
                ret = xinput_device_action(dev, "disable")
                all_ok &= ret
        else:
            if category != "keyboards":
                for dev in items:
                    ret = xinput_device_action(dev, "enable")
                    all_ok &= ret
                    ret = rotate_input(dev, "normal")	
                    all_ok &= ret
    return all_ok 

def load_device_configuration(filename):
    #read input devices from config
    with open(filename,"r") as conf:
        devs = json.load(conf)
    return devs

def main(mode="normal", orientation="normal"):
    if mode == "normal":
        set_normal(devices)
    elif mode == "tent":
        set_tent(devices)
    elif mode == "tablet":
        set_tablet(devices, orientation)
    elif mode == "scratchpad":
        set_scratchpad(devices)
    else:
        print("Unsupported mode")	

if __name__ == '__main__':
    devices = load_device_configuration("/etc/autotablet/inputDevices.json")	
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

