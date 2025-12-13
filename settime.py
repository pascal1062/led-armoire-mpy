
def set_time():
    import socket
    import select
    import re
    from machine import RTC

    addr = ('192.168.0.90', 47900)
    date_time = "null"
    regex = re.compile("^([2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9])\s([0-9][0-9]:[0-5][0-9]:[0-5][0-9][-][0-9])$")
    tz = -5

    rtc = RTC()
    s = socket.socket()
    s.setblocking(False)

    try:
        s.connect(addr)
    except OSError:
        pass

    poller = select.poll()
    poller.register(s, select.POLLOUT | select.POLLIN)

    i = 0
    while True:
        i+=1
        if i >= 5: break
        res = poller.poll(1000)
        if res:
            if res[0][1] & select.POLLOUT:
                try:
                    s.send(b"set_time_request\n")
                except:
                    pass
                poller.modify(s,select.POLLIN)
                continue
            if res[0][1] & select.POLLIN:
                try:
                    date_time = s.recv(22)
                except:
                    pass
                break
        break

    s.close()

    if regex.match(date_time):
        year = int(date_time[0:4])
        month = int(date_time[5:7])
        day = int(date_time[8:10])
        hour = int(date_time[11:13])
        minute = int(date_time[14:16])
        second = int(date_time[17:19])
        subsecond = 0
        tz = int(date_time[19:21])
        rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
        print("RTC updated\n")
    else:
        print("RTC not updated\n")
        
    return date_time, tz

#End
#time.localtime() --> (2019, 10, 6, 16, 39, 28, 6, 279)