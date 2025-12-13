from machine import Pin
import time
import uasyncio

class ClickButton():
    
    click_debounce_delay = 30
    click_multiclick_delay = 300
    click_helddown_delay = 1000
    
    
    def __init__(self, button_pin):
        #pin = button_pin
        self.pin = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self.active_high = 0
        self.btn_state = not self.active_high
        self.last_state = self.btn_state
        self.click_count = 0
        self.clicks = 0
        self.depressed = False
        self.changed = False
        self.last_bounce_time = 0
        
    
    async def update(self):
        self.btn_state = self.pin.value()
        if not self.active_high: self.btn_state = not self.btn_state
        
        if (self.btn_state != self.last_state): self.last_bounce_time = time.ticks_ms() 
        
        if (time.ticks_diff(time.ticks_ms(), self.last_bounce_time) > self.click_debounce_delay) and (self.btn_state != self.depressed):
            self.depressed = self.btn_state
            if self.depressed: self.click_count += 1
        
        if self.last_state == self.btn_state: self.changed = False
        self.last_state = self.btn_state
        
        if not self.depressed and time.ticks_diff(time.ticks_ms(), self.last_bounce_time) > self.click_multiclick_delay:
            self.clicks = self.click_count
            self.click_count = 0
            if self.clicks != 0: self.changed = True
            
        if self.depressed and time.ticks_diff(time.ticks_ms(), self.last_bounce_time) > self.click_helddown_delay:
            self.clicks = 0 - self.click_count
            self.click_count = 0
            if self.clicks != 0: self.changed = True
        
        #await uasyncio.sleep_ms(1)
            
#End