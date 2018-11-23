#!/usr/bin/python3
import schedule
import time
import datetime
from relay import Relay

LIGHT = 0
GAS = 1

# i'm forced to use a global object
r = Relay(True)

def light_on():
	print("Switching light on")
	r.setEnabled(LIGHT, True)

def light_off():
	print("Switching light off")
	r.setEnabled(LIGHT, False)

def gas_on():
	print("Switching gas on")
	r.setEnabled(GAS, True)

def gas_off():
	print("Switching gas off")
	r.setEnabled(GAS, False)

def resume():
	print("resuming to correct states")
	now = datetime.datetime.now()
	print("for info: {}:{}".format(now.hour, now.minute))
	if now.hour >= 12:
		light_on()
	else:

		light_off()
	if (now.hour >= 11 and now.minute >= 50) or now.hour > 12:
		gas_on()
	else:
		gas_off()
	print("resume done.")

def aquarium():
	resume()
	print("Starting main instance of aquarium")
	schedule.every().day.at("12:00").do(light_on)
	schedule.every().day.at("00:00").do(light_off)
	schedule.every().day.at("11:50").do(gas_on)
	schedule.every().day.at("23:30").do(gas_off)
	print("Setup ok, entering into the main loop")
	try:
		while True:
			schedule.run_pending()
			time.sleep(1)
	except KeyboardInterrupt:
		print("Manuel exit requested")


if __name__ == "__main__":
	r.test()
	aquarium()
