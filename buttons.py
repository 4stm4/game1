import gpiozero, pysnooper, time, requests
from threading import Thread


buttons_specs = [
    [21, 16, 20, False]
]
butttons = []

class BUTTON(object):
    def __init__(self, number, pin_sensor, pin_led, points : int, start : bool):
        self.number = number
        self.sensor = gpiozero.Button(pin_sensor)
        self.led = gpiozero.LED(pin_led)
        self.points_per_click = points
        self.start = start

start_button = BUTTON(0, 20, 12, 0, True)

def led_off_3sec(led_num):
    butttons[led_num].led.off()
    time.sleep(3)
    butttons[led_num].led.on()

def init_buttons():
    for number in range( len(buttons_specs)):
        butttons.append(BUTTON(number, *buttons_specs[number]))
        butttons[number].led.on()
        butttons[number].sensor.when_pressed = led_off_3sec(number)
    start_button.led.blink()