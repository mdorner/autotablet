import subprocess
import sys
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
			if c.isalpha() or c.isspace() or c.isnumeric():
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
	#Report findings
	print("Identified the following devices:")
	for category, devices in classified_devices.items():
		print(str(category) + ":")
		for device in devices:
			print(device)
	#write to file
	conf = open("inputDevices.json","w")
	conf.truncate()
	json.dump(classified_devices, conf)
	conf.close()
main()

