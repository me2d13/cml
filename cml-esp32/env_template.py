WIFI_SSID = 'some_net'
WIFI_PASSWORD = 'some_pwd'
MQTT_BROKER = "192.168.1.1"
MQTT_TOPIC = "/cml/"
LOG_TOPIC = "/devices/cml_esp32/log"
BAT_TOPIC = "/devices/cml_esp32/battery"

PIN_NO_BEEP = 33

PIN_NO_RED = 15
PIN_NO_GREEN = 27
PIN_NO_BLUE = 12
PIN_NO_BAT = 35

BAT_REPORT_SEC = 25

KEYPAD_ROW_PINS = [ 4, 26, 25, 21 ]
KEYPAD_COL_PINS = [ 36, 32, 34 ]

CANCEL_COMMAND_SEC = 10
DEEP_SLEEP_SEC = 300

"""
Usefull commands:


set AMPY_PORT=COM6
ampy -p COM3 reset
ampy -p COM6 ls

esptool.py --chip esp32 --port COM6 erase_flash
esptool.py --chip esp32 --port COM6 --baud 460800 write_flash -z 0x1000 /d/Temp/esp32-20210902-v1.17.bin

$ esptool.py -p COM3 flash_id

ESP pins

Vin GND D13 D12 D14 D27 D26 D25 D33
x   x   C2  R1  C1  R4  C3  R3  R2   col/row
x   x   IN  OUT IN  OUT IN  OUT OUT
        14!  A5  A4  21! A2  A1  A0
        32

RGB: 12,27,33 + 3.3V
           14
Beep: 15 + GND        
      33


ampy put asyn.py
ampy put beep.py
ampy -p COM6 put core.py
ampy -p COM6 put env.py
ampy -p COM6 put keypad.py
ampy -p COM6 put keypad_uasyncio.py
ampy -p COM6 put led.py
ampy -p COM6 put mqtt.py
ampy -p COM6 put mqtt_as.py
ampy -p COM6 put watchdog.py
"""