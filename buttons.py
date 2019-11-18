import gpiozero, pysnooper, time, requests
from utils import do_photo, play_music
from threading import Thread

# pin_sensor, pin_led, points : int, start
buttons_specs = [
    [20, 16, 20],
    [7, 8, 15],
    [25,24,10],
    [18,15,25],
    [26,19,10],
    [13,6, 15],
    [5, 11, 20],
    [9, 10, 25],
    [22,27, 20]
]
butttons = []

class BUTTON(object):
    def __init__(self, number, pin_sensor, pin_led, points : int):
        self.number = number
        self.sensor = gpiozero.Button(pin_sensor, pull_up = False, bounce_time= None)
        self.led = gpiozero.LED(pin_led)
        self.points_per_click = points

start_button = BUTTON(0, 21, 12, 0)
