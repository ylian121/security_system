
# Motion Servo Alarm RGB
from gpiozero.pins.pigpio import PiGPIOFactory
from threading import Thread
from gpiozero import RGBLED, Buzzer, Servo, MotionSensor
from time import sleep, time

#email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Use pigpio pin factory for more accurate PWM
factory = PiGPIOFactory()

# Setup
servo = Servo(26, pin_factory=factory)  # GPIO 26 with pigpio for more stable control
pir = MotionSensor(16)

# System state
armed = False

def SENDEMAILACTIVITY(email):
    # Email details
    sender_email = "pajaka755@gmail.com"
    receiver_email = email
    subject = "URGENT: GISS MOTION DETECTED"
    body = "Hello, MOTION HAS BEEN DETECTED! view the activity log here. Here is the live viewing feed: http://172.20.10.11:5001/"

    # SMTP server configuration (Example for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    password = "lrvp iztv zwsb rfuc"  # Consider using an environment variable for the password

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Attach the JSON file
    attachment = MIMEText(json.dumps(activity_data), 'json')
    attachment.add_header('Content-Disposition', 'attachment', filename="activity_log_file.json")
    msg.attach(attachment)


    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

#JSON def
# File paths
activity_info_file = 'activity_log_file.json'

# Function to load activity data from JSON file
def load_activity():
    if os.path.exists(activity_info_file):
        with open(activity_info_file, 'r') as file:
            return json.load(file)
    return {}

# Function to save activity data to JSON file
def save_activity(data):
    with open(activity_info_file, 'w') as file:
        json.dump(data, file, indent=4)

# Load the activity data
activity_data = load_activity()


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
    seconds = time.time()
    result = ("motion detected:", seconds)
    save_activity(result)
    if armed:  # Only trigger alarm if the system is armed
        led_controller.set_color((1, 0, 0))  # Set LED to red
        print("Motion detected! Alarm sounding, red LED on.")
        SENDEMAILACTIVITY(
        

        # Keep the alarm sounding until the system is disarmed
        while armed:
            led_controller.sound_alarm()  # Sound the alarm continuously
            sleep(0.5)  # Short delay to prevent CPU overuse

def check_motion():
    # Assign the trigger_alarm function to run when motion is detected
    pir.when_motion = trigger_alarm

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
