'''
     
'''
import time

class TwoSpeed():

    def __init__(self, instance):
        self._instance = instance
        self._outhigh = 0
        self._outlow = 0
        self._speed = 'Off'
        self._lastspeed = self._speed
        self._interval = 0
        self._delay = 0

    def get_speed(self):
        return self._speed

    def set_speed(self, speed, outlow, outhigh):
        self._speed = speed
        
        if self._speed != self._lastspeed and self._speed == 'Off':
            self._outlow = 0
            self._outhigh = 0
            self._delay = time.ticks_ms()
            self._interval = time.ticks_ms()
            self._lastspeed = self._speed
            return
        
        if self._speed != self._lastspeed and time.ticks_diff(time.ticks_ms(), self._interval) <= 5000:
            return
        
        if self._speed != self._lastspeed:
            self._outlow = 0
            self._outhigh = 0
            self._delay = time.ticks_ms()
            self._interval = time.ticks_ms()
            self._lastspeed = self._speed
            
        if self._speed == 'Low':
            self._outhigh = 0
            if time.ticks_diff(time.ticks_ms(), self._delay) > 2000 and self._outlow == 0: self._outlow = 1
        elif self._speed == 'High':
            self._outlow = 0
            if time.ticks_diff(time.ticks_ms(), self._delay) > 2000 and self._outhigh == 0: self._outhigh = 1
        else:
            self._outlow = 0
            self._outhigh = 0
        
        outlow.value(self._outlow)
        outhigh.value(self._outhigh)

#End