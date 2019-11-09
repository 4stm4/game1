import gpiozero
button_specs = [
    [20, 12, 20, False],
    [21, 16,  0, True]
]

class BUTTON(object):
    def __init__(self, number, pin_sensor, pin_led, points : int, start : bool):
        self.number = number
        self.sensor = gpiozero.Button(pin_sensor)
        self.led = gpiozero.LED(pin_led)
        self.points_per_click = points
        self.start = start

butttons = []

for number in range(0, len(button_specs)-1):
    butttons.append(BUTTON(number, *button_specs[number]))