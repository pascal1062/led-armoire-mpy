'''
    Two Speed control FAN ou PUMP with internal delays between speeds. Require two binary outputs to operate.
    construct: pump = TwoSpeed(1) ... instance #1 other will be instance #2,3,4 etc...never use same instance!
    use: set to low -> pump.set_speed('Low', BO1, BO2)
         set to high -> pump.set_speed('High', BO1, BO2)
         set to off -> pump.set_speed('Off', BO1, BO2)
'''
import time

class TwoSpeed():

    def __init__(self, outlow, outhigh):
        #self._instance = instance
        self._low = outlow
        self._high = outhigh
        self._outhigh = 0
        self._outlow = 0
        self._speed = 'Off'
        self._lastspeed = self._speed
        self._interval = 0
        self._delay = 0
        
    def get_output(self):
        return self._low, self._high

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        #if outlow != self._low: return "pas la bonne sortie de basse vitesse"
        #if outhigh != self._high: return "pas la bonne sortie de haute vitesse"
        
        self._speed = speed
        
        if self._speed != self._lastspeed and self._speed == 'Off':
            self._outlow = 0
            self._outhigh = 0
            self._delay = time.ticks_ms()
            self._interval = time.ticks_ms()
            self._lastspeed = self._speed
            self._low.value(self._outlow)
            self._high.value(self._outhigh)
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
            if time.ticks_diff(time.ticks_ms(), self._delay) > 2000 and self._outlow == 0 and self._outhigh == 0: self._outlow = 1
        elif self._speed == 'High':
            self._outlow = 0
            if time.ticks_diff(time.ticks_ms(), self._delay) > 2000 and self._outhigh == 0 and self._outlow == 0: self._outhigh = 1
        else:
            self._outlow = 0
            self._outhigh = 0
        
        #outlow.value = self._outlow
        #outhigh.value = self._outhigh
        #outlow.value(self._outlow)
        #outhigh.value(self._outhigh)
        self._low.value(self._outlow)
        self._high.value(self._outhigh)
        return

#End