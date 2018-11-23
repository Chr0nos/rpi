#!/usr/bin/python3
import RPi.GPIO as GPIO
import schedule
import time
import datetime

class Relay:
	def __init__(self, fullinit=False):
		if fullinit:
			GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setwarnings(False)
		self.states = [False, False, False, False]
		self.pins = [12, 11, 10, 8]
        self.fullinit = fullinit
		for p in self.pins:
			GPIO.setup(p, GPIO.OUT)

	def __del__(self):
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
            pass