#!/usr/bin/python
import RPi.GPIO as GPIO


class light:

	def __init__(self, mode, pin):
		self.mode = mode
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)
		if self.mode == 'switch':
			self.output = None
			GPIO.output(self.pin, 0)
		elif self.mode == 'pwm':
			self.output =  GPIO.output(self.pin, 1000)
			self.output.start(0)

	def switch(self, value):
		if self.mode == 'pwm':
			self.outptu.ChangeDutyCycle(value*100)
		elif self.mode == 'switch':
			GPIO.output(self.pin, value)

	def switchOn(self):
		if self.mode == 'pwm':
			self.output.ChangeDutyCycle(100)
		elif self.mode == 'switch':
			GPIO.output(self.pin, 1)

	def switchOff(self):
		if self.mode == 'pwm':
			self.output.ChangeDutyCycle(0)
		elif self.mode == 'switch':
			GPIO.output(self.pin, 0)


	def dim(self, dc):
		if self.mode == 'pwm':
			self.output.ChangeDutyCycle(dc)

	def disable(self):
		if self.mode == 'pwm':
			self.output.stop()
