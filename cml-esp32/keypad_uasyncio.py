# inspired by https://github.com/BrendanSimon/micropython_experiments/blob/master/keypad/keypad_uasyncio.py

import micropython
from machine import Pin
import uasyncio as asyncio
from primitives.queue import Queue
import env

QUEUE_SIZE_DEFAULT = 5
LONG_KEYPRESS_COUNT_DEFAULT = 20

class Keypad_uasyncio():
    ## Key states/events
    KEY_UP          = 0
    KEY_DOWN        = 1
    KEY_DOWN_LONG   = 2
    KEY_UP_LONG     = 3     ## an event only, not a state.

    def __init__(self, queue_size=QUEUE_SIZE_DEFAULT, long_keypress_count=LONG_KEYPRESS_COUNT_DEFAULT):
        self.init(queue_size=queue_size, long_keypress_count=long_keypress_count)

    #-------------------------------------------------------------------------

    def init(self, queue_size=QUEUE_SIZE_DEFAULT, long_keypress_count=LONG_KEYPRESS_COUNT_DEFAULT):
        ## Create the queue to push key events to.
        self.queue = Queue(maxsize=queue_size)

        self.running = False
        self.long_keypress_count = long_keypress_count

        ## The chars on the keypad
        keys = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '*', '0', '#',
            ]

        ## The chars to display/return when the key is pressed down for a long time.
        self.chars_long = [
            'A', 'B', 'C',
            'D', 'E', 'F',
            'G', 'H', 'I',
            'J', 'K', 'L',
            ]

        ## Initialise all keys to the UP state.
        self.keys = [ { 'char':key, 'state':self.KEY_UP, 'down_count':0 } for key in keys ]

        ## Pin names for rows and columns.
        self.rows = env.KEYPAD_ROW_PINS
        self.cols = env.KEYPAD_COL_PINS

        ## Initialise row pins as outputs.
        self.row_pins = [ Pin(pin_name, mode=Pin.OUT, pull=None) for pin_name in self.rows ]

        ## Initialise column pins as inputs.
        self.col_pins = [ Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in self.cols ]

        self.row_scan_delay_ms = 40 // len(self.rows)

    #-------------------------------------------------------------------------

    def start(self):
        self.running = True

    #-------------------------------------------------------------------------

    def stop(self):
        self.running = False
        for _, row_pin in enumerate(self.row_pins):
            row_pin.value(1) # prepare rows up and to cols wake up from deep sleep

    #-------------------------------------------------------------------------

    def get_key(self):
        key = self.queue.get()
        return key

    #-------------------------------------------------------------------------

    def key_process(self, key_code, col_pin):
        key = self.keys[key_code]
        key_event = None

        if col_pin.value():
            ## key pressed down
            if key['state'] == self.KEY_UP:
                ## just pressed (up => down)
                key_event = self.KEY_DOWN
                key['state'] = key_event
            elif key['state'] == self.KEY_DOWN:
                ## key still down
                    key['down_count'] += 1
                    if key['down_count'] >= self.long_keypress_count:
                        key_event = self.KEY_DOWN_LONG
                        key['state'] = key_event
        else:
            ## key not pressed (up)
            if key['state'] == self.KEY_DOWN:
                ## just released (down => up)
                key_event = self.KEY_UP if key['down_count'] < self.long_keypress_count else self.KEY_UP_LONG
            key['state'] = self.KEY_UP
            key['down_count'] = 0

        return key_event

    async def scan_coro(self):
        """A coroutine to scan each row and check column for key events."""

        while self.running:
            key_code = 0
            for row, row_pin in enumerate(self.row_pins):
                ## Assert row.
                row_pin.value(1)

                ## Delay between processing each row.
                await asyncio.sleep_ms(self.row_scan_delay_ms)

                ## Check for key events for each column of current row.
                for col, col_pin in enumerate(self.col_pins):
                    ## Process pin state.
                    key_event = self.key_process(key_code=key_code, col_pin=col_pin)
                    ## Process key event.
                    if key_event == self.KEY_UP:
                        key_char = self.keys[key_code]['char']
                        await self.queue.put(key_char)
                    elif key_event == self.KEY_DOWN_LONG:
                        key_char = self.chars_long[key_code]
                        await self.queue.put(key_char)

                    key_code += 1

                ## Deassert row.
                row_pin.value(0)

