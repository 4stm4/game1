import gpiozero, pysnooper
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

@pysnooper.snoop()
def init_buttons():
    for number in range(1, len(buttons_specs)+1):
        print(number)
        butttons.append(BUTTON(number, *buttons_specs[number]))
        butttons[number].led.on()
    