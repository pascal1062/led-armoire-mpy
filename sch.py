
class Schedule():
    
    def __init__(self, instance, name, starttime, stoptime):
        self._inst = instance
        self._name = name
        self._starttime = starttime
        self._stoptime = stoptime
        self._newvalue = False
        self._lastvalue = False


    def update(self,actual_time):
        output = False

        #get actual time as integer
        hour_min = int(str(actual_time[3]) + str('{:02}'.format(actual_time[4])))

        if hour_min >= self._starttime and hour_min < self._stoptime: output = True

        self._newvalue = output
        #return output
    
    def value(self):
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
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def changedOn(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def changedOff(self):
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
        