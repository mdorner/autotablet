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
	
def determine_orientation(accel):
	xVal, yVal, scaleVal = read_accel(accel)
	print("x: " + str(xVal) + " y: " + str(yVal) +
				 " scale: " + str(scaleVal))
	if abs(xVal) < 3 and yVal < -7:
		ort = "normal"
	elif xVal > 7 and abs(yVal) < 3:
		ort = "left"
	elif xVal < -7 and abs(yVal) < 3:
		ort = "right"
	elif abs(xVal) < 3 and yVal > 7:
		ort = "inverted"
	else:
		ort = "unknown"
	return ort

def adjust_orientation(devices, orientation, previous="unknown"):
	if orientation != previous:	
		if orientation == "normal":
			tc.set_normal(devices)
		elif orientation == "left":
			tc.set_tablet(devices, "left")
		elif orientation == "right":
			tc.set_tablet(devices, "right")	
		elif orientation == "inverted":
			tc.set_tent(devices)
		else:
			print ("unknown orientation")
	

def main(conf="inputDevices.json"):
	devices = tc.load_device_configuration(conf)
	accelerometers = devices['accelerometers']
	print("Found accelerometers: " + str(accelerometers))
	accels = open_all_accelerometers(accelerometers)
	previous = "unknown"
	while(accels_readable(accels)):
		for accel in accels:
			orientation = determine_orientation(accel)
			print ("My orientation is " + orientation)
		adjust_orientation(devices, orientation, previous)
		time.sleep(1.0)
		previous = orientation
	close_all_accelerometers(accels)	

if __name__ == '__main__':
	main()

