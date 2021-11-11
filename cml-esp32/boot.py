# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
#import webrepl
#webrepl.start()
from machine import Pin
p15 = Pin(15, Pin.OUT)