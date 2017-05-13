#!/usr/bin/python3
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
import subprocess
import sys
import os
import json

encoding = "utf-8"

def parse_devices(raw_devices):
	out = []
	tmp = ""
	for device in raw_devices:
		for c in device:
			if c == '\t':
				out.append(tmp.strip())
				tmp = ""
				break
			if c.isalpha() or c.isspace() or c.isnumeric() or c =="/":
				tmp = tmp + c
	return out

def classify_devices(device_names):
	known_devices = {}
	known_devices['keyboards'] = []
	known_devices['touchpads'] = []
	known_devices['touchscreens'] = []
	known_devices['trackpoints'] = []
	known_devices['stylus'] = []
	known_devices['erasers'] = []
	for device in device_names:
		if "keyboard" in device and not "Virtual" in device:
			known_devices['keyboards'].append(device)
		if "stylus" in device:
			known_devices['stylus'].append(device)
		if "eraser" in device:
			known_devices['erasers'].append(device)
		if "TrackPoint" in device:
			known_devices['trackpoints'].append(device)
		if "TouchPad" in device:
			known_devices['touchpads'].append(device)
		if "Digitizer" in device:
			known_devices['touchscreens'].append(device)
	return known_devices


def main():
	#list input devices
	stdout = subprocess.check_output(["xinput","list"])
	lines = stdout.splitlines()
	#decode output
	decoded = []
	for line in lines:
		decoded.append(line.decode(encoding))
	#parse devices to filter out their names
	parsed_devices = parse_devices(decoded)
	#categorize the devices
	classified_devices = classify_devices(parsed_devices)
	#write to file
	conf = open("inputDevices.json","w")
	conf.truncate()
	json.dump(classified_devices, conf)
	conf.close()
main()

