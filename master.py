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
from automation import Automation as func

# network data exchange
xfer = DataExchange()
xfer.attach('192.168.0.20')
read = None
SERVER_ADDR = "192.168.0.90"

# Under cabinet Led Light To Dim
frequency = 5000
led = PWM(Pin(16), frequency)
led.duty(0)

# var
fade_dem = BinaryValue(1,"fade")
sunset = AnalogValue(1,"sunset")
tz = AnalogValue(2,"timeZone"); tz.value = -5
sunset_dec = AnalogValue(3,"sunset_dec")
event_a = AnalogValue(4,"event_a")
event_b = AnalogValue(5,"event_b")
event_c = AnalogValue(6,"event_c")
dim_led = AnalogValue(7,"dim_led")
dim_led.value = int(0)

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
sunset_dec.value = timdiff.time_to_dec(sunset.value)[2]
#sunset event calculated in decimalformat
event_a.value = timdiff.dec_to_time(int(func.scale(sunset_dec.value,1600,2075,1950,2150)))[2]
event_b.value = timdiff.dec_to_time(int(func.scale(event_a.value,1950,2150,2050,2200)))[2]
event_c.value = timdiff.dec_to_time(int(func.scale(event_b.value,2050,2200,2250,2250)))[2]

hor_matin = Schedule(1,"hor_matin",530,830)
hor_midi = Schedule(2,"hor_midi",1100,1300)
hor_soir_a = Schedule(3,"hor_soir_a",timdiff.offset(sunset.value,-15)[2],event_a.value)
hor_soir_b = Schedule(4,"hor_soir_b",event_a.value,event_b.value)
hor_soir_c = Schedule(5,"hor_soir_c",event_b.value,event_c.value)


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


#courbe dimming, 0-255 - moins long pour tracer la courbe
async def dim_light(val):
    if dim_led.value < val:
        #dim up
        while dim_led.value <= min(val,255):
            dim_led.value+=1 if dim_led.value >= 1 else 1
            if dim_led.value == 256: led.duty(1023); break
            led.duty(round(pow(dim_led.value*2/512,2.8)*1024))
            await uasyncio.sleep_ms(5)
    else:
        #dim down
        while dim_led.value >= min(max(1, val),255):
            dim_led.value-=1 if dim_led.value >= 1 else 0
            led.duty(round(pow(dim_led.value*2/512,2.8)*1024))
            await uasyncio.sleep_ms(5)   


#booting
schedules = {"sunset":str(sunset.value), "sunset-on":str(hor_soir_a.start_time), "sunset-event-a":str(hor_soir_b.start_time), 
             "sunset-event-b":str(hor_soir_c.start_time), "sunset-event-c":str(hor_soir_c.stop_time)}
xfer.send_data({"route": "nred", "board": "esp32-Led-Cabinet", "state": "booting wait 1 sec..."}, SERVER_ADDR)
xfer.send_data({"route": "nred", "board": "esp32-Led-Cabinet", "date-heure": str(actualTime(time.localtime())).encode("utf-8"), "tzone=":int(tz.value)}, SERVER_ADDR)
xfer.send_data(schedules, SERVER_ADDR)


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
    if _msg == "/esp32-LedCab/system/sunset/on" and _cmd == "True": xfer.resp_data(str(hor_soir_a.start_time).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/system/sunset/off" and _cmd == "True": xfer.resp_data(str(hor_soir_c.stop_time).encode("utf-8"), _sender)


def append_file(val):
	f = open('log.txt','a')
	f.write(str(actualTime(time.localtime()))+'; '+ str(val) +'\n')
	f.close()
    

async def main():
    btn = ClickButton(18)

    while True:
        # Read data transfer
        read = xfer.recv_data()
        if read is not None:
            handle_xfer(read)
            if read[0][0] == "/esp32-LedCab/ledCab/value/set": await dim_light(int(read[0][1]))
        
        await btn.update()
        if btn.clicks == 1: await dim_light(0)
        if btn.clicks == -1: await dim_light(255)

        if t1.every(1):
            #min
            hor_matin.update(time.localtime())
            hor_midi.update(time.localtime())        
            hor_soir_a.update(time.localtime())
            hor_soir_b.update(time.localtime())         
            hor_soir_c.update(time.localtime())
            
            schedules = {"sunset":str(sunset.value), "sunset-on":str(hor_soir_a.start_time), "sunset-event-a":str(hor_soir_b.start_time), 
                         "sunset-event-b":str(hor_soir_c.start_time), "sunset-event-c":str(hor_soir_c.stop_time)}
            xfer.send_data(schedules, SERVER_ADDR)

        if t2.every(1):
            #hour
            _settime()
            
            sunset.value = int(str(sun.get_sunset_time()[3]) + str('{:02}'.format(sun.get_sunset_time()[4])))
            sunset_dec.value = timdiff.time_to_dec(sunset.value)[2]
            
            event_a.value = timdiff.dec_to_time(int(func.scale(sunset_dec.value,1600,2075,1950,2150)))[2]
            event_b.value = timdiff.dec_to_time(int(func.scale(event_a.value,1950,2150,2050,2200)))[2]
            event_c.value = timdiff.dec_to_time(int(func.scale(event_b.value,2050,2200,2250,2250)))[2]
            
            hor_soir_a.start_time = timdiff.offset(sunset.value,-15)[2]
            hor_soir_a.stop_time = event_a.value
            hor_soir_b.start_time = event_a.value
            hor_soir_b.stop_time = event_b.value
            hor_soir_c.start_time = event_b.value
            hor_soir_c.stop_time = event_c.value


        if hor_matin.value() == True and hor_matin.changed(): append_file(hor_matin.value()); await dim_light(255)
        if hor_matin.value() == False and hor_matin.changed(): append_file(hor_matin.value()); await dim_light(0)

        if hor_midi.value() == True and hor_midi.changed(): append_file(hor_midi.value()); await dim_light(255)
        if hor_midi.value() == False and hor_midi.changed(): append_file(hor_midi.value()); await dim_light(0)

        if hor_soir_a.value() == True and hor_soir_a.changed(): append_file(hor_soir_a.value()); await dim_light(255)

        if hor_soir_b.value() == True and hor_soir_b.changed(): append_file(hor_soir_b.value()); await dim_light(126)

        if hor_soir_c.value() == True and hor_soir_c.changed(): append_file(hor_soir_c.value()); await dim_light(75)
        if hor_soir_c.value() == False and hor_soir_c.changed(): append_file(hor_soir_c.value()); await dim_light(0)

        await uasyncio.sleep_ms(1)

uasyncio.run(main())

#End