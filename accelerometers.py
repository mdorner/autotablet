#!/usr/bin/env python3
"""
Copyright (C) 2015 Michael G. Dorner

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, see <http://www.gnu.org/licenses/>.
"""
from os import path
from os import listdir
from time import sleep

def get_acceleromters(device_path):
    return open_all_accelerometers(find_accelerometers(device_path))

def find_accelerometers(device_path):
    """
    Locate accelerometers in the device path

    device_path: the location where the files from which the value can be read
    are found

    return: a list of accelerometer
    """
    accelerometers = []
    for directory in listdir(device_path):
        with open(path.join(device_path, directory, 'name')) as candidate:
            if "iio:device" in directory and "accel" in candidate.read():
                accelerometers.append(path.join(device_path,directory))
    return accelerometers

def open_all_accelerometers(devices):
    """
    Open all accelerometer device files

    devices: the directory of the devices

    return: the accelerometers
    """
    accels = []
    for accel in devices:
        x, y, z, scale = open_accelerometer(accel)
        accels.append((x, y, z, scale))
    return accels

def open_accelerometer(name):
    """
    Open a particular accelerometer's device files

    name: the path to the accelerometer

    return: the opened files
    """
    x_axis = open(path.join(name, 'in_accel_x_raw'))
    y_axis = open(path.join(name, 'in_accel_y_raw'))
    z_axis = open(path.join(name, 'in_accel_z_raw'))
    scale = open(path.join(name, 'in_accel_scale'))
    return x_axis, y_axis, z_axis, scale

def close_all_accelerometers(accels):
    """Close all accelerometer files"""
    for accel in accels:
        close_accelerometer(accel)

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
        x, y, z, scale = accel
        ret &= x.readable() and y.readable() and z.readable() and scale.readable()
        #need to insert code to check whether the accel can bke read or not
        return ret

def read_accel(accel):
    """
    Read x, y, and z value from accelerometer along with the scale

    accel: the accelerometer

    return: the x and y value as well as the scale value as tuple
    """
    for desc in accel:
        desc.seek(0)
    x, y, z, scale = accel #these are actually the files
    scaleValue = float(scale.read())
    val_x = float(x.read()) * scaleValue
    val_y = float(y.read()) * scaleValue
    val_z = float(z.read()) * scaleValue
    return (val_x, val_y, val_z, scaleValue)

def main():
    accels = get_acceleromters("/sys/bus/iio/devices/")
    try:
        while(True):
            for accel in accels:
                x, y, z, scale = read_accel(accel)
                print ("x: " + str(x) + " y: " + str(y) +
                        " z: " + str(z) + " scale: " + str(scale))
            sleep(1.0)
    except OSError:
        print("Cannot recover from error" + str(sys.exc_info()[0]))
        close_all_accelerometers(accels)
        sys.exit(1)

if __name__ == "__main__":
    main()
