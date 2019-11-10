import gpiozero, pysnooper, time, requests
from utils import do_photo, play_music
from threading import Thread


buttons_specs = [
    [20, 16, 20, False]
]
butttons = []

class BUTTON(object):
    def __init__(self, number, pin_sensor, pin_led, points : int, start : bool):
        self.number = number
        self.sensor = gpiozero.Button(pin_sensor, pull_up = False, bounce_time= None)
        self.led = gpiozero.LED(pin_led)
        self.points_per_click = points
        self.start = start

start_button = BUTTON(0, 21, 12, 0, True)
