from machine import Pin, unique_id
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import time
import env



ssid = env.WIFI_SSID
password = env.WIFI_PASSWORD
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

print('Trying to wifi connect')

while station.isconnected() == False:
  time.sleep_ms(500)

print('Connection successful')
print(station.ifconfig())

import uftpd
uftpd.start()