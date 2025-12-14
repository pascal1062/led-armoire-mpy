'''
    Binary output class, on/off digital value True/False
    IC chip is TLV5620 connected through SPI serial interface. resolution is 8 bits 0-255
'''
from machine import Pin, SPI

class BinaryOutput():

    def __init__(self, instance, name):
        self._spi = SPI(-1, baudrate=50000, polarity=0, phase=1, sck=Pin(5), mosi=Pin(18), miso=Pin(19))
        self._cs1 = Pin(14, Pin.OUT)
        self._cs1.value(1)
        self._cs2 = Pin(15, Pin.OUT)
        self._cs2.value(1)
        self._instance = instance
        self._name = name
        self._newvalue = None
        self._lastvalue = None

    def writeDAC_A(self, addr, val):
        #addr = DAC address and RNG bit, first byte to send
        #val = value (0-255) second byte to send
        buf = bytearray(2)
        buf[0] = addr
        buf[1] = val
        self._cs1.value(1)
        self._spi.write(buf)  
        self._cs1.value(0)
        self._cs1.value(0)
        self._cs1.value(0)
        self._cs1.value(1)

    def writeDAC_B(self, addr, val):
        #addr = DAC address and RNG bit, first byte to send
        #val = value (0-255) second byte to send
        buf = bytearray(2)
        buf[0] = addr
        buf[1] = val
        self._cs2.value(1)
        self._spi.write(buf)
        self._cs2.value(0)
        self._cs2.value(0)
        self._cs2.value(0)
        self._cs2.value(1)
         
    def get_name(self):
        return self._name    

    def get_value(self):
        return self._newvalue

    def set_value(self, val):
        if isinstance(val, bool):
            self._newvalue = val
            dac_value = 255 if self._newvalue == True else 0
        else:
            return
        inst = self._instance

        if inst == 1:
            self.writeDAC_A(3, dac_value)
        elif inst == 2:
            self.writeDAC_A(1, dac_value)
        elif inst == 3:
            self.writeDAC_A(5, dac_value)
        elif inst == 4:
            self.writeDAC_A(7, dac_value)
        elif inst == 5:
            self.writeDAC_B(3, dac_value)
        elif inst == 6:
            self.writeDAC_B(1, dac_value)
        elif inst == 7:
            self.writeDAC_B(5, dac_value)
        elif inst == 8:
            self.writeDAC_B(7, dac_value)

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def rising(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def falling(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue == False):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    value = property(get_value, set_value)
    name = property(get_name)

# End
