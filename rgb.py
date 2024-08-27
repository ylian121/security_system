# rgb.py
from gpiozero import RGBLED, Buzzer
from time import sleep

class LEDController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LEDController, cls).__new__(cls)
            cls._instance.led = RGBLED(red=9, green=10, blue=11)  # Initialize the LED
            cls._instance.buzzer = Buzzer(2)  # Initialize the Buzzer on GPIO 2
        return cls._instance

    def set_color(self, color):
        self.led.color = color

    def sound_alarm(self):
        # Make the buzzer sound like an alarm
        for _ in range(5):  # Beep 5 times
            self.buzzer.on()
            sleep(0.2)
            self.buzzer.off()
            sleep(0.2)

    def stop_alarm(self):
        self.buzzer.off()

# Create a global instance that can be imported
led_controller = LEDController()