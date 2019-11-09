import gpiozero, pysnooper, time
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
def start_button_work():
    start_button.led.blink()

def init_buttons():
    for number in range(1, len(buttons_specs)+1):
        butttons.append(BUTTON(number, *buttons_specs[number-1]))
        butttons[number-1].led.on()
    t = Thread(target=start_button_work)
    t.start()