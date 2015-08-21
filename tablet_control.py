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
	return subprocess.call(args)

def rotate_screen(orientation):
	#change orientation to one of normal, left, right, inverse
	return subprocess.call(["xrandr", "-o", "%s" % orientation])

def xinput_device_action(device, action):
	#call a simple actions such as enable or disable for a device
	return subprocess.call(["xinput","%s" %action,"%s" % device])

def set_normal(devices):
	rotate_screen("normal")
	for category, items in devices.items():
		for dev in items:
			xinput_device_action(dev, "enable")
			if category != 'keyboards':
				rotate_input(dev, "normal")

#effectively identical to setTabled("inverted")
def set_tent(devices):
	rotate_screen("inverted")
	for category, items in devices.items():
		if category in ["keyboards","trackpoints", "touchpads"]:
			for dev in items:
				xinput_device_action(dev, "disable")
		else:
			for dev in items:
				rotate_input(dev, "inverted")	

def set_tablet(devices, orientation):
	rotate_screen(orientation)
	for category, items in devices.items():
		if category in ["keyboards","trackpoints", "touchpads"]:
			for dev in items:
				pass
#				xinput_device_action(dev, "disable")
		else:
			for dev in items:
				ret = rotate_input(dev, orientation)
				#this code is required to address a bug on the thinkpad yoga 12
				#the touchscreen can sometimes not be found, which requires
				#repeated attempts. the loop variable prevents infinite loops
				for i in range(5):
					time.sleep(1)
					ret = rotate_input(dev, orientation)
					if ret:
						break

def set_scratchpad(devices):
	rotate_screen("normal")
	for category, items in devices.items():
		if category in ["trackpoints", "touchpads", "touchscreens"]:
			for dev in items:
				xinput_device_action(dev, "disable")
		else:
			if category != "keyboards":
				for dev in items:
					rotate_input(dev, "normal")	
	 	
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
	devices = load_device_configuration("inputDevices.json")	
	if len(sys.argv) > 2:
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()

