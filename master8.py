import sys
import time
import uasyncio
import uftpd
from machine import Pin, PWM
from data_exchange import DataExchange
from click_button import ClickButton
from sch import Schedule
from bv import BinaryValue
from av import AnalogValue
from suntime import Sun
from timediff import TimeDiff as timdiff
from do_every import DoEvery

# network data exchange
xfer = DataExchange()
xfer.attach('192.168.0.20')
read = None
SERVER_ADDR = "192.168.0.90"

# Under cabinet Led Light To Dim
frequency = 5000
led = PWM(Pin(16), frequency)
led.duty(0)
dim_value = 1

#btn = ClickButton(5)
#fade_up = False
dim_value = 0

fade_dem = BinaryValue(1,"fade")
sunset = AnalogValue(1,"sunset")
tz = AnalogValue(2,"timeZone"); tz.value = -5

#timer Doevery
t1 = DoEvery("t1", "min")
t2 = DoEvery("t2", "hour")

#Create suntime from local city
sun = Sun(46.82,-71.25,int(tz.value))

#function set time clock
def _settime():
    import settime
    #returned tuple example (b'2025-03-30 14:59:58-4', -4)
    tz.value = settime.set_time()[1]
    sun.set_tzone(int(tz.value))

_settime()
sunset.value = int(str(sun.get_sunset_time()[3]) + str('{:02}'.format(sun.get_sunset_time()[4])))

#horaires
hor_matin = Schedule(1,"hor_matin",530,830)
hor_midi = Schedule(2,"hor_midi",1130,1230)
hor_soir = Schedule(3,"hor_soir",timdiff.offset(sunset.value,-15)[2],timdiff.offset(sunset.value,180)[2])


#function stop board
def _stop():
    xfer.send_data({"route": "nred", "board": "esp32-Led-Cabinet", "state": "soft reset command received..."}, SERVER_ADDR)
    from machine import reset
    reset()


#function return date-time
def actualTime(t):
    date_str = "{:4}-{:02}-{:02}".format(t[0],t[1],t[2])
    time_str = "{:02}:{:02}:{:02}".format(t[3],t[4],t[5])
    return date_str+" "+time_str


async def dim_up(val):
    global dim_value
    #was at 1023 (255)
    while dim_value <= min(val,254):
        dim_value+=1 if dim_value >= 1 else 1
        #led.duty(round(pow(2.0,dim_value/102.4)-1))
        led.duty(round(pow(dim_value*2/512,2.8)*1024))
        await uasyncio.sleep_ms(5)


async def dim_down(val):
    global dim_value
    while dim_value >= min(max(1, val),254):
        dim_value-=1 if dim_value >= 1 else 0
        #led.duty(round(pow(2.0,dim_value/102.4)-1))
        led.duty(round(pow(dim_value*2/512,2.8)*1024))
        await uasyncio.sleep_ms(5)


async def dim_upm():
    global dim_value
    #led.duty(round(pow(2.0,dim_value/102.4)-1))
    led.duty(round(pow(dim_value*2/512,2.8)*1024))
    await uasyncio.sleep_ms(0)


#booting
xfer.send_data({"route": "nred", "board": "esp32-Led-Cabinet", "state": "booting wait 1 sec..."}, SERVER_ADDR)
xfer.send_data({"route": "nred", "board": "esp32-Led-Cabinet", "date-heure": str(actualTime(time.localtime())).encode("utf-8"), "tzone=":int(tz.value)}, SERVER_ADDR)
xfer.send_data({"sunset":str(sunset.value), "sunset-on":str(hor_soir.start_time), "sunset-off":str(hor_soir.stop_time)}, SERVER_ADDR)


def handle_xfer(msg):
    _msg = msg[0][0]
    _cmd = msg[0][1]
    _sender = msg[1]
    #print(_msg, _cmd, _sender)
    if _msg == "/esp32-LedCab/system/exit" and _cmd == "True": xfer.resp_data(b'"rebooting...', _sender); _stop()
    if _msg == "/esp32-LedCab/system/date-heure" and _cmd == "True": xfer.resp_data(str(actualTime(time.localtime())+" tz"+str(tz.value)).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/system/set-time" and _cmd == "True": _settime(); xfer.resp_data(str(actualTime(time.localtime())+" tz"+str(tz.value)).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/ledCab/value/get" and _cmd == "True": xfer.resp_data(str(led.duty()).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/system/sunset/" and _cmd == "True": xfer.resp_data(str(sunset.value).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/system/sunset/on" and _cmd == "True": xfer.resp_data(str(timdiff.offset(sunset.value,-15)[2]).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/system/sunset/off" and _cmd == "True": xfer.resp_data(str(timdiff.offset(sunset.value,180)[2]).encode("utf-8"), _sender)

async def main():
    btn = ClickButton(5)
    global dim_value
    #global sunset

    while True:
        # Read data transfer
        read = xfer.recv_data()
        if read is not None:
            handle_xfer(read)
            if read[0][0] == "/esp32-LedCab/ledCab/value/set": await dim_up(int(read[0][1])) if int(read[0][1]) > dim_value else await dim_down(int(read[0][1]))
        
        await btn.update()
        if btn.clicks == 1: await dim_down(0)
        if btn.clicks == -1 and btn.depressed: fade_dem.value = True
        if btn.depressed == False: fade_dem.value = False

        if fade_dem.value:
            #if dim_value >= 1023:
            #    dim_value = 1024
            #elif dim_value <= 0:
            #    dim_value = 1
            #elif dim_value >= 1000:
            #    dim_value += 1
            #else:
            #    dim_value += 5
            if dim_value >= 254:
                dim_value = 255
            elif dim_value <= 0:
                dim_value = 1
            else:
                dim_value += 1
            await dim_upm()
    
        
        if t1.every(1):
            sunset.value = int(str(sun.get_sunset_time()[3]) + str('{:02}'.format(sun.get_sunset_time()[4])))
            hor_soir.start_time = timdiff.offset(sunset.value,-15)[2]
            hor_soir.stop_time = timdiff.offset(sunset.value,180)[2]
            xfer.send_data({"sunset":str(sunset.value), "sunset-on":str(hor_soir.start_time), "sunset-off":str(hor_soir.stop_time)}, SERVER_ADDR)

        if t2.every(1):
            _settime()

        hor_matin.update(time.localtime())
        if hor_matin.changedOn(): await dim_up(255)
        if hor_matin.changedOff(): await dim_down(0)

        hor_midi.update(time.localtime())
        if hor_midi.changedOn(): await dim_up(255)
        if hor_midi.changedOff(): await dim_down(0)
        
        hor_soir.update(time.localtime())
        if hor_soir.changedOn(): await dim_up(255)
        if hor_soir.changedOff(): await dim_down(0)

        await uasyncio.sleep_ms(1)

uasyncio.run(main())


#End