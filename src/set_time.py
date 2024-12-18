import requests
import time
import machine

def set_time():
    # network must be up first
    r = requests.get("http://date.jsontest.com")
    mils = r.json()['milliseconds_since_epoch']
    r.close() # saw documentation that says this must be done manually
    time_tuple = time.gmtime(mils // 1000)
    time_tuple = time_tuple[0:3] + (0,) + time_tuple[3:6] + (0,)
    machine.RTC().datetime(time_tuple)
