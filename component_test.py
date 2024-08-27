from gpiozero import Servo, MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from threading import Thread
from led_alarm_servo import led_controller

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
    pir.when_motion = trigger_alarm

def main():
    global armed
    led_controller.set_color((0, 0, 1))  # Start with LED blue (disarmed state)
    print("System ready. Press 1 to arm or 2 to disarm.")

    # Start the servo rotation in a separate thread to keep it moving
    servo_thread = Thread(target=rotate_servo, daemon=True)
    servo_thread.start()

    # Set up motion detection
    check_motion()

    while True:
        choice = input("Enter 1 to arm, 2 to disarm: ")
        if choice == '1' and not armed:
            arm_system()
        elif choice == '2' and armed:
            disarm_system()
        else:
            print("Invalid input or system already in that state.")

if __name__ == "__main__":
    main()

