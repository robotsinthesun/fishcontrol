#!/usr/bin/python
import sys
from datetime import datetime
import time
import light
import RPi.GPIO as GPIO
hourOffset = 1

GPIO.cleanup()

tasks = {}

class taskSwitch:
	
	def __init__(self, name, times=[], values=[]):
		self.name = name
		if type(times) != list:
			print "Warning: times must be in list format!"
		self.times = []
		for time in times:
			h, m, s = [int(i) for i in time.split(':')]
			seconds = h*3600 + m*60 + s
			self.times.append(seconds)
		self.values = values

	def addAction(self, time, value):
		h, m, s = [int(i) for i in time.split(':')]
		self.times.append(h*3600 + m*60 + s)
		self.values.append(value)

	def checkForAction(self, timeSeconds):
		timeSeconds = int(timeSeconds)
		for time, value in zip(self.times, self.values):
			if timeSeconds == time:
				return self.name, value
		return None, None
		

tasks['light'] = taskSwitch('light')
tasks['light'].addAction("06:00:00", 1)
tasks['light'].addAction("19:40:00", 1)
tasks['light'].addAction("23:00:00", 0)



light = light.light(mode='switch', pin=28)

dtSecondsOld = 0
while(True):
	# Get time.
	dt = datetime.now().time()
	h, m, s = [int(i) for i in [dt.hour, dt.minute, dt.second]]
	h += hourOffset
	dtSeconds = (h * 60 + m) * 60 + s
	if dtSeconds != dtSecondsOld:
		sys.stdout.write("Current time: {:02d}:{:02d}:{:02d}.".format(h, m, s))
		sys.stdout.write('\r')
		sys.stdout.flush()

		dtSecondsOld = dtSeconds

		# Check if there are any tasks for this second.
		for task in tasks:
			name, value = tasks[task].checkForAction(dtSeconds)
			if name == 'light':
				if value == 0:
					print "Switching light off at {:02d}:{:02d}:{:02d}.".format(h, m, s)
				elif value == 1:
					print "Switching light on at {:02d}:{:02d}:{:02d}.".format(h, m, s)
				light.switch(value)
	time.sleep(0.1)
GPIO.cleanup()
