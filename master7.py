import sys
import time
import uftpd
from machine import Pin, PWM
from data_exchange import DataExchange


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
fade_value = 0


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


while dim_value < 1024:
	dim_value+=1
	led.duty(round(pow(2.0,dim_value/102.4)-1))
	time.sleep_ms(4)

time.sleep(1)

while dim_value > 0:
	dim_value-=1
	led.duty(round(pow(2.0,dim_value/102.4)-1))
	time.sleep_ms(4)

dim_value = 0


def dim_up(val):
	global dim_value
	global fade_value
	while dim_value < val:
		dim_value+=1
		fade_value = round(pow(2.0,dim_value/102.4)-1)
		time.sleep_ms(4)		

	
def dim_down(val):
	global dim_value
	global fade_value
	while dim_value > val:
		dim_value-=1
		fade_value = round(pow(2.0,dim_value/102.4)-1)
		time.sleep_ms(4)


#booting
xfer.send_data({"route": "nred", "board": "esp32-Led-Cabinet", "state": "booting wait 1 sec..."}, SERVER_ADDR)


def handle_xfer(msg):
    _msg = msg[0].decode("utf8")
    _sender = msg[1]
    if _msg == "/esp32-LedCab/system/exit": xfer.resp_data(b'"rebooting...', _sender); _stop()
    if _msg == "/esp32-LedCab/system/date-heure": xfer.resp_data(str(actualTime(time.localtime())).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/ledCab/value/get": xfer.resp_data(str(led.duty()).encode("utf-8"), _sender)
    if _msg == "/esp32-LedCab/ledCab/value/set/100": led.duty(dim_up(1023)); xfer.resp_data(b'{"value":"100%"}', _sender)
    if _msg == "/esp32-LedCab/ledCab/value/set/0": led.duty(dim_down(0)); xfer.resp_data(b'{"value":"0"}', _sender)


while True:
    # Read data transfer
    read = xfer.recv_data()
    if read is not None:
        handle_xfer(read)
    
    time.sleep(0.1)
    
#End