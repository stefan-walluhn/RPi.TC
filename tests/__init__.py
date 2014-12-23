from unittest.mock import Mock
import sys
import imp

rpi = imp.new_module("rpi")
rpi.GPIO = Mock()
gpio = imp.new_module("gpio")

sys.modules['RPi'] = rpi
sys.modules['RPi.GPIO'] = gpio
