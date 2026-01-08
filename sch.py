import time

'''
    --- Important --- si on veut utiliser l'horaire "une fois ifonce",il faut caller le changedOn et aussi le changedOff
    pour setter les newvalue lastvalue
'''

class Schedule():
    
    def __init__(self, instance, name, starttime, stoptime):
        self._inst = instance
        self._name = name
        self._starttime = starttime
        self._stoptime = stoptime
        self._newvalue = False
        self._lastvalue = False


    def update(self):
        output = False
        actual_time = time.localtime()

        #get actual time as integer
        hour_min = int(str(actual_time[3]) + str('{:02}'.format(actual_time[4])))

        if hour_min >= self._starttime and hour_min < self._stoptime: output = True

        self._newvalue = output
        #return output
    
    def value(self):
        self.update()
        return self._newvalue
    
    def get_start_time(self):
        return self._starttime
    
    def set_start_time(self, val):
        self._starttime = val

    def get_stop_time(self):
        return self._stoptime
    
    def set_stop_time(self, val):
        self._stoptime = val

    def changed(self):
        self.value()
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def changedOn(self):
        self.value()
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def changedOff(self):
        self.value()
        if (self._newvalue != self._lastvalue) and (self._newvalue == False):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    start_time = property(get_start_time, set_start_time)
    stop_time = property(get_stop_time, set_stop_time)

#End
        