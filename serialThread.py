# -*- coding: latin-1 -*-
#
#	Copyright (c) 2015-2016 Paul Bomke
#	Distributed under the GNU GPL v2.
#
#	This file is part of monkeyprint.
#
#	monkeyprint is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	monkeyprint is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You have received a copy of the GNU General Public License
#    along with monkeyprint.  If not, see <http://www.gnu.org/licenses/>.

import serial
import re
import threading
import time

#class serialThread(threading.Thread):
#	# Override init function.
#	def __init__(self):
#		# Call super class init function.
#		super(serialThread, self).__init__()


class serialThread(threading.Thread):
	def __init__(self, port, baud, queue):

		# Internalise parameters.
		self.queue = queue
		self.port = port
		self.baud = baud

		# Stop event.
		self.stopThread = threading.Event()

		# Configure and open serial.
		try:
			self.serial = serial.Serial(
				port=self.port,
				baudrate=self.baud,
				bytesize = serial.EIGHTBITS, #number of bits per bytes
				parity = serial.PARITY_NONE, #set parity check: no parity
				stopbits = serial.STOPBITS_ONE,
				timeout = 0	# Wait for incoming bytes forever.
				)
			print("Serial port " + self.port + " connected.")
		# If serial port does not exist...
		except serial.SerialException:
			# ... define a dummy.
			self.serial = None
			print("Serial port " + self.port + " not found.\nMake sure your board is plugged in and you have defined the correct serial port in the settings menu.")

		# Call super class init function.
		super(serialThread, self).__init__()

	# Send function. This simply puts the command inside the input queue.
	# This way the send command can be initiated without having to pass a queue
	# to the serial object from outside.
	def send(self, command):
		self.queue.put(command)

	# Override run function.
	# Send a command string with optional value.
	# Method allows to retry sending until ack is received as well
	# as waiting for printer to process the command.
	def run(self):
		if self.serial != None:
			print("Serial waiting for commands to send.")
		else:
			print('Serial not operational.')
		# Start loop.
		while 1 and not self.stopThread.isSet():
			# Get command from queue.
			if self.queue.qsize():
				command = self.queue.get()
				string = command[0]
				value = command[1]
				retry = command[2]
				wait = command[3]
				if self.serial != None:
					# Cast inputs.
					if value != None: value = float(value)
					if wait != None: wait = int(wait)
					# ... start infinite loop that sends and waits for ack.
					count = 0
					# Set timeout to 5 seconds.
					self.serial.timeout = 5
					while count < 5 and not self.stopThread.isSet():
						# Create command string from string and value.
						# Separate string and value by space.
						if value != None:
							string = string + " " + str(value)
						# Place send message in queue.
						print("Sending command \"" + string + "\".")
						# Send command.
						self.serial.write(string.encode())
						# If retry flag is set...
						if retry:
							# ... listen for ack until timeout.
							printerResponse = self.serial.readline()
							printerResponse = printerResponse.strip()
							# Compare ack with sent string. If match...
							if printerResponse == string:
								# Place success message in queue.
								print("Command \"" + string + "\" sent successfully.")
								if wait != None:
									print("Wait for printer to finish...")
								# ... exit the send loop.
								break
						# If retry flag is not set...
						else:
							# ... exit the loop.
							break
						# Increment counter.
						count += 1
						# Place giving up message in queue if necessary.
						if count == 5:
							print("Printer not responding. Giving up...")

					# Wait for response from printer that signals end of action.
					# If wait value is provided...
					if wait != 0:
						# ... set timeout to one second...
						self.serial.timeout = 1
						count = 0
						while count < wait and not self.stopThread.isSet():
							# ... and listen for "done" string until timeout.
							printerResponse = self.serial.readline()
							printerResponse = printerResponse.strip()
							# Listen for "done" string.Check if return string is "done".
							if printerResponse == "done":
								print("Printer done.")
								break
							else:
								count += 1
						# In case of timeout...
						if count == wait:
							# ... place fail message.
							print("Printer did not finish within timeout.")
					# Reset the timeout.
					self.serial.timeout = None
					# Put done flag into queue to signal end of command process.
					print('done')
				else:
					print('Sending failed. Port does not exist.')
					print('done')
			else:
				time.sleep(.1)


	# Send a command string with optional value.
	# Method allows to retry sending until ack is received as well
	# as waiting for printer to process the command.
#	def sendCommand(self, string, value=None, retry=False, wait=None):
#		self.run(string, value, retry, wait)

	def stop(self):
		self.close()
		print("Stopping serial.")
		self.stopThread.set()

	def join(self, timeout=None):
		self.close()
		self.stopThread.set()
		threading.Thread.join(self, timeout)

	def close(self):
		if self.serial != None:
			self.serial.close()
