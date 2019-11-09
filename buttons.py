import gpiozero, pysnooper, time, requests
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

@pysnooper.snoop()
def led_off_3sec(led_num):
    butttons[led_num].led.off()
    time.sleep(3)
    butttons[led_num].led.on()

def start_button_work():
    cnt = 0 
    while True:
        if start_button.sensor.is_active:
            cnt += 1
            print('start {}'.format(cnt))
            time.sleep(1)
            continue

def init_buttons():
    for number in range( len(buttons_specs)):
        butttons.append(BUTTON(number, *buttons_specs[number]))
        butttons[number].led.on()
    start_button.led.blink()
    t = Thread(target=start_button_work)
    t.start()