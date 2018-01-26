#!/usr/bin/python
import sys
from datetime import datetime
import time
import serialThread
import queue
import signal

hourOffset = 0


# Clean up on closing.
def close():
	runningThreads = threading.enumerate()
	# End kill threads. Main gui thread is the first...
	for i in range(len(runningThreads)):
		if i != 0:
			runningThreads[-1].join(timeout=10000)	# Timeout in ms.
			print("Serial thread " + str(i) + " finished.")
			del runningThreads[-1]

# Handle sigterm to shut down gracefully.
signal.signal(signal.SIGTERM, close)


tasks = {}

class taskSwitch:

	def __init__(self, name, times=[], values=[]):
		self.name = name
		if type(times) != list:
			print ("Warning: times must be in list format!")
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
tasks['light'].addAction("23:00:00", 0)



queue = queue.Queue()
serialThread = serialThread.serialThread("/dev/ttyACM0", 9600, queue)
serialThread.start()



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
					print ("Switching light off at {:02d}:{:02d}:{:02d}.".format(h, m, s))
					queue.put(['PWM2', 0, 0, 0])
				elif value == 1:
					print ("Switching light on at {:02d}:{:02d}:{:02d}.".format(h, m, s))
					queue.put(['PWM2', 1000, 0, 0])
				#light.switch(value)
	time.sleep(0.1)




