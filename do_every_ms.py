import time

class DoEveryMS():
    
    def __init__(self, name):
        self._name = name
        self._end = time.ticks_ms()
        self._newvalue = False
        self._lastvalue = False
        
    def every_ms(self, t):
        val = False
        if time.ticks_diff(time.ticks_ms(), self._end) < 0: self._end = time.ticks_ms()
        if time.ticks_diff(time.ticks_ms(), self._end) >= t:
            self._end = time.ticks_ms()
            self._newvalue = True
        else:
            self._newvalue = False
 
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue

        return val

#End