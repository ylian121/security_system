
# Motion Servo Alarm RGB
from gpiozero.pins.pigpio import PiGPIOFactory
from threading import Thread
from gpiozero import RGBLED, Buzzer, Servo, MotionSensor
from time import sleep

# Use pigpio pin factory for more accurate PWM
factory = PiGPIOFactory()

# Setup
servo = Servo(26, pin_factory=factory)  # GPIO 26 with pigpio for more stable control
pir = MotionSensor(16)

# System state
armed = False

def rotate_servo():
    """Rotate the servo motor between -90 and 90 degrees smoothly and consistently."""
    while True:
        # Gradually move from -90 to 90 degrees
        for position in range(-90, 91):  # Go from -90 to 90 degrees
            servo.value = position / 90  # Convert to servo value range (-1 to 1)
            sleep(0.05)  # Increase this value for smoother, slower movement

        # Gradually move from 90 to -90 degrees
        for position in range(90, -91, -1):  # Go back from 90 to -90 degrees
            servo.value = position / 90  # Convert to servo value range (-1 to 1)
            sleep(0.05)  # Increase this value for smoother, slower movement
def arm_system():
    global armed
    armed = True
    led_controller.set_color((0, 1, 0))  # Set LED to green
    print("System armed. Green LED on.")

def disarm_system():
    global armed
    armed = False
    led_controller.set_color((0, 0, 1))  # Set LED to blue
    led_controller.stop_alarm()           # Ensure alarm stops when disarmed
    print("System disarmed. Blue LED on.")

def trigger_alarm():
    if armed:  # Only trigger alarm if the system is armed
        led_controller.set_color((1, 0, 0))  # Set LED to red
        print("Motion detected! Alarm sounding, red LED on.")

        # Keep the alarm sounding until the system is disarmed
        while armed:
            led_controller.sound_alarm()  # Sound the alarm continuously
            sleep(0.5)  # Short delay to prevent CPU overuse

def check_motion():
    # Assign the trigger_alarm function to run when motion is detected
#    pir.when_motion = trigger_alarm
    pir.when_motion = 

# System state
armed = False

class LEDController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LEDController, cls).__new__(cls)
            cls._instance.led = RGBLED(red=5, green=6, blue=21)  # Initialize the LED
            cls._instance.buzzer = Buzzer(0)  # Initialize the Buzzer on GPIO 2
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
