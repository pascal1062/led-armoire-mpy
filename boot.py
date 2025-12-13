# This file is executed on every boot (including wake-boot from deepsleep)
import wifi_connect
import settime
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

wifi_connect.do_connect()
settime.set_time()
