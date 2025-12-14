#from twospeed import TwoSpeed
from twospeed2 import TwoSpeed
from machine import Pin
from machine import ADC
import time

low = Pin(22, Pin.OUT)
High = Pin(23, Pin.OUT)
pot = ADC(Pin(35))
pot.atten(ADC.ATTN_11DB) 
#low.value(0)
#High.value(0)
fanL = Pin(26, Pin.OUT)
fanH = Pin(27, Pin.OUT)

def selector(p):
    sel = 'off'
    if p < 1500:
        sel = 'off'
    elif p > 3000:
        sel = 'high'
    elif p > 1500 and p < 3000:
        sel = 'low'
    
    return sel

#pump = TwoSpeed(1)
pump = TwoSpeed(low,High)
#fan = TwoSpeed(2)
fan = TwoSpeed(fanL,fanH)
delay = time.ticks_ms()

sel = selector(pot.read())
print(sel)

while True:
    if sel == 'off':
        #pump.set_speed('Off', low, High)
        pump.set_speed('Off')
    elif  sel == 'low':   
        #pump.set_speed('Low', low, High)
        pump.set_speed('Low')
    elif  sel == 'high':   
        #pump.set_speed('High', low, High)
        pump.set_speed('High')
        
    #fan.set_speed('high', low, High)
    fan.set_speed('high')
        
    if time.ticks_diff(time.ticks_ms(), delay) > 100: sel = selector(pot.read()); print(pot.read(), sel, fan.get_speed()); delay = time.ticks_ms()
        
#End
