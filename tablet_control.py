import subprocess
import sys
import json

def xinput_device_action(device, action):
	ret = subprocess.call(["xinput","%s" %action,"%s" % device])
	if ret == 0:
		print ("{dev} {state}".format(dev = device, state = action))
	else:
		print ("failed to do {state} for {dev}".format(
			dev = device, state = action))

def main(config="inputDevices.json"):
	if __name__ == '__main__':
		print ("Welcome to tablet control")
		#read input devices from config
		with open(config,"r") as conf:
			devices = json.load(conf)
		#found devices:
		for category, items in devices.items():
			print(category + ":" )
			for device in items:
				print(device)	
		touchscreens = devices["touchscreens"]
		for device in touchscreens:
			xinput_device_action(device,"disable")
			
main()

