from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(14)  # Replace 17 with the GPIO pin you used
#pir2 = MotionSensor(11)
#pir3 = MotionSensor(10)
#pir4 = MotionSensor(9)
# or pir2.motion or pir3.motion or pir4.motion:

while True:
    if pir.motion:
        print("Motion detected!")
    else:
        print("No motion.")
    sleep(1)
