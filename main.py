import sys
import time

def actualTime(t):
    date_str = "{:4}-{:02}-{:02}".format(t[0],t[1],t[2])
    time_str = "{:02}:{:02}:{:02}".format(t[3],t[4],t[5])
    return date_str+" "+time_str

try:
    import master
except Exception as e:
    f = open('error.log','a')
    f.write(actualTime(time.localtime())+'\n')
    sys.print_exception(e, f)
    f.write('--End--'+'\n')
    f.close()

#End    
