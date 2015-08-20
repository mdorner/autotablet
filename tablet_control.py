import subprocess
import sys
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
	ret = subprocess.call(args)
	#handle failure

def rotate_screen(orientation):
	#change orientation to one of normal, left, right, inverse
	ret = subprocess.call(["xrandr", "-o", "%s" % orientation])
	#handle failure

def xinput_device_action(device, action):
	#call a simple actions such as enable or disable for a device
	ret = subprocess.call(["xinput","%s" %action,"%s" % device])
	#handle failure

def setNormal():
	for category, items in devices.items():
		for dev in items:
			xinput_device_action(dev, "enable")
			if category != 'keyboards':
				rotate_input(dev, "normal")
	rotate_screen("normal")

#effectively identical to setTabled("inverted")
def setTent():
	for category, items in devices.items():
		if category in ["keyboards","trackpoints", "touchpads"]:
			for dev in items:
				xinput_device_action(dev, "disable")
		else:
			for dev in items:
				rotate_input(dev, "inverted")	
	rotate_screen("inverted")

def setTablet(orientation):
	for category, items in devices.items():
		if category in ["keyboards","trackpoints", "touchpads"]:
			for dev in items:
				xinput_device_action(dev, "disable")
		else:
			for dev in items:
				rotate_input(dev, orientation)	
	rotate_screen(orientation)

def setScratchpad():
	for category, items in devices.items():
		if category in ["trackpoints", "touchpads", "touchscreens"]:
			for dev in items:
				xinput_device_action(dev, "disable")
		else:
			for dev in items:
				rotate_input(dev, "normal")	
	rotate_screen("normal")
	 	
def loadDeviceConfiguration(filename):
	#read input devices from config
	with open(filename,"r") as conf:
		devs = json.load(conf)
	return devs

def main(mode="normal", orientation="normal"):
		if mode == "normal":
			setNormal()
		elif mode == "tent":
			setTent()
		elif mode == "tablet":
			setTablet(orientation)
		elif mode == "scratchpad":
			setScratchpad()
		else:
			print("Unsupported mode")	
	
if __name__ == '__main__':
	devices = loadDeviceConfiguration("inputDevices.json")	
	if len(sys.argv) > 2:
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()

