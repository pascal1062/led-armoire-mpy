import time
import sys
import gc
from machine import Pin

button = Pin(0, Pin.IN)
Pulse = Pin(23, Pin.OUT)
Pulse.value(0)

scanOn = time.ticks_ms()
scanOff = time.ticks_ms()
#Ontime = 200
Ontime = 1000
#Offtime = 6000
Offtime = 3000

time.sleep_ms(1000)

while True:
    if button.value() == 0: gc.collect(); sys.exit()
    if time.ticks_diff(time.ticks_ms(), scanOff) >= Offtime and Pulse.value() == 0:
        Pulse.value(1)
        scanOn = time.ticks_ms()
        print("Pulse ON")
    if time.ticks_diff(time.ticks_ms(), scanOn) >= Ontime and Pulse.value() == 1:
        Pulse.value(0)
        scanOff = time.ticks_ms()
        print("Pulse OFF")

#End    
