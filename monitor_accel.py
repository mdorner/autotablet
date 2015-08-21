import sys
from os import path
import tablet_control as tc

def main(conf="inputDevices.json"):
	devices = tc.load_device_configuration(conf)
	accelerometers = devices['accelerometers']
	print("Found accelerometers: " + str(accelerometers))

main()

