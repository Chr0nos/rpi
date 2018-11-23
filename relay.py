#!/usr/bin/python3
import RPi.GPIO as GPIO
import schedule
import time
import datetime
import json

class Relay:
	def __init__(self, fullinit=False, database=None):
		self.states = [False, False, False, False]
		self.pins = [12, 11, 10, 8]
		self.fullinit = fullinit
		self.database = database
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pins, GPIO.OUT, initial=GPIO.HIGH)
		if self.load():
			self.update()

	def __del__(self):
		self.save()
		if self.fullinit:
			GPIO.cleanup()

	def setEnabled(self, index, state):
		self.states[index] = state
		GPIO.output(self.pins[index], state == False)

	def setAll(self, state):
		for i in range(0, 4):
			self.setEnabled(i, state)

	def test(self):
		self.setAll(False)
		for i in range(0, len(self.pins)):
			self.setEnabled(i, True)
			time.sleep(1)
		self.setAll(False)

	def update(self):
		for i in range(0, len(self.pins)):
			pin = self.pins[i]
			state = self.states[i]
			self.setEnabled(i, state)

	def save(self):
		if not self.database:
			return
		with open(self.database, 'w') as fd:
			json.dump({'states': self.states}, fd)
			fd.close()
		# print("saved")

	def load(self):
		if not self.database:
			return False
		try:
			with open(self.database, 'r') as fd:
				self.states = json.load(fd)['states']
				print(self.states)
			# print("loaded")
			return True
		except FileNotFoundError:
			return False
