import time
from machine import Pin

low = Pin(22, Pin.OUT)
High = Pin(23, Pin.OUT)
low.value(1)
High.value(1)

def twoSpeed(speed):
    if speed == 'off':
        l = 0 
        h = 0
    elif speed == 'low':
        h = 0
        t = time.ticks_ms()
        l = 1 #if time.ticks_diff(time.ticks_ms(), t) > 2000 else 0
    elif speed == 'High':
        l = 0
        t = time.ticks_ms()
        h = 1 #if time.ticks_diff(time.ticks_ms(), t) > 2000 else 0
    else:
        l = 0
        h = 0
        
    return l,h


t = time.ticks_ms()

while True:
    low.value(twoSpeed('High')[0])
    if time.ticks_diff(time.ticks_ms(), t) > 2000: High.value(twoSpeed('High')[1])
    else: High.value(0)