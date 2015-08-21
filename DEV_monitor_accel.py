import sys
from os import path
import time
import tablet_control as tc

def open_all_accelerometers(devices):
	accels = []
	for accel in devices:
		x, y, scale = open_accelerometer(accel)
		accels.append((x,y,scale))
	return accels

def close_all_accelerometers(accels):
	for accel in accels:
		close_accelerometer(accel)

def open_accelerometer(name):
	x_axis = open(path.join(name, 'in_accel_x_raw'))
	y_axis = open(path.join(name, 'in_accel_y_raw'))
	scale = open(path.join(name, 'in_accel_scale'))
	return x_axis, y_axis, scale
		
def close_accelerometer(accel):
	for desc in accel:
		close(desc)

def accels_readable(accels):
	return True

def read_accel(accel):
	for desc in accel:
		desc.seek(0)
	x,y,scale = accel
	scaleValue = float(scale.read())
	xValue = float(x.read()) * scaleValue
	yValue = float(y.read()) * scaleValue
	return (xValue, yValue, scaleValue)
	
def determine_mode(accel):
	xVal, yVal, scaleVal = read_accel(accel)
	print("x: " + str(xVal) + " y: " + str(yVal) +
				 " scale: " + str(scaleVal))
	#fairly horizontal position
	if abs(xVal) < 3:
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
	if "tablet" in mode:
		if mode.startswith("i"):
			ret = tc.set_tablet(devices, "inverted")
		elif mode.startswith("l"):
			ret =  tc.set_tablet(devices, "left")
		elif mode.startswith("r"):
			ret =  tc.set_tablet(devices, "right")
		else: 
			ret = False

	else:
		if mode == "tent":
			ret = tc.set_tent(devices)
		elif mode == "scratchpad":
			ret = tc.set_scratchpad(devices)
		elif mode == "normal":
			ret = tc.set_normal(devices)
	return ret

def main(conf="inputDevices.json"):
	devices = tc.load_device_configuration(conf)
	accelerometers = devices['accelerometers']
	print("Found accelerometers: " + str(accelerometers))
	accels = open_all_accelerometers(accelerometers)
	previous = "unknown"
	while(accels_readable(accels)):
		for accel in accels:
			mode = determine_mode(accel)
			print ("My orientation is " + mode)
		if mode != previous or not ok:
			ok = switch_mode(devices, mode)
		time.sleep(1.0)
		previous = mode
	close_all_accelerometers(accels)	
	tc.set_normal(devices)

if __name__ == '__main__':
	main()

