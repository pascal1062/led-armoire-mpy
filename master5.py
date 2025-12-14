import time
from machine import Pin

High = Pin(23, Pin.OUT)
High.value(0)

windowSize = 5000
windowStartTime = time.ticks_ms()
windowStopTime = time.ticks_ms()
pidOutput = 2500
Ton = 2500  
Toff = 2500

while True:
    if time.ticks_diff(time.ticks_ms(), windowStopTime) > Toff and High.value() == 0: High.value(1); windowStartTime = time.ticks_ms()
    if time.ticks_diff(time.ticks_ms(), windowStartTime) > Ton and High.value() == 1: High.value(0); windowStopTime = time.ticks_ms()
    print(windowStartTime, windowStopTime)
    
    #if time.ticks_ms() > windowSize:
    #    windowStartTime += windowSize
    #if pidOutput > (time.ticks_ms() - windowStartTime):
    #    High.value(1)
    #else:
    #    High.value(0)

ramp = 99

while True:
    if ramp <= 1: ramp = 99
    else: ramp -= 1
    out = Automation.aswitch(out, CO, ramp+0.01, ramp)
    print(ramp,out)
    High.value(out)
    time.sleep(0.1)
 