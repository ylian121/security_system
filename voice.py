import pveagle
from pvrecorder import PvRecorder
import os
import math
import struct
#from time import time
import time
from alarm_components import led_controller  # Import the LEDController instance
import pvporcupine
import pvcheetah
from alarm_components import arm_system

#def list_audio_devices():
 #   devices = PvRecorder.get_available_devices()
  #  for i, device in enumerate(devices):
   #     print(f"Device {i}: {device}")

def enroll_speaker(speaker_name=None):

    access_key = "UQOnRaJ10JVpaGU0XYreQaSBIV+JMUU387+IzalVU+C2U1bAyvC4EQ=="

    # List available audio devices
##   print("Available audio devices:")
##   list_audio_devices()

    # Ask the user to select the device index
    #device_index = int(input("Enter the device index to use: "))

    # Update: Have user insert their name for their profile
   #testing purposes only speaker_name = input("Enter the speaker's name: ")

    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(f"Failed to create Eagle Profiler: {e}")
        exit(1)
#testing changed -1 to 0 for index
    DEFAULT_DEVICE_INDEX = 10
    recorder = PvRecorder(
##        device_index=device_index,  # Use the selected device index
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_profiler.min_enroll_samples
    )

    recorder.start()

    enroll_percentage = 0.0
    while enroll_percentage < 100.0:
        audio_frame = recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
#testing purposes only delete for final turn in
        print(f"Enrollment: {enroll_percentage:.2f}% - {feedback}")

    recorder.stop()

    speaker_profile = eagle_profiler.export()

    # Update Save the profile and assign with the user's name
    profile_filename = f"{speaker_name}_profile.eagle"
    with open(profile_filename, "wb") as f:
        f.write(speaker_profile.to_bytes())

    recorder.delete()
    eagle_profiler.delete()

def delete_speaker(speaker_name):
    speaker_to_remove = f"{speaker_name}_profile.eagle"

    if os.path.exists(speaker_to_remove):
        os.remove(speaker_to_remove)
#all print statements testing purposes only
        print(f"Profile '{speaker_to_remove}' deleted successfully.")
    else:
        print(f"No profile found for '{speaker_name}'.")

def recognize_speaker():

    access_key = "UQOnRaJ10JVpaGU0XYreQaSBIV+JMUU387+IzalVU+C2U1bAyvC4EQ=="

    # Update: Load all speaker profiles
    profiles = []
    profile_files = [f for f in os.listdir('.') if f.endswith('_profile.eagle')]
    for file_name in profile_files:
        with open(file_name, "rb") as f:
            speaker_profile_bytes = f.read()
        profiles.append(pveagle.EagleProfile.from_bytes(speaker_profile_bytes))

    try:
        eagle = pveagle.create_recognizer(
            access_key=access_key,
            speaker_profiles=profiles
        )
    except pveagle.EagleError as e:
        print(f"Failed to create Eagle Recognizer: {e}")
        exit(1)

    DEFAULT_DEVICE_INDEX =10
    recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle.frame_length
    )

    recorder.start()

    # Update: Sets a threshold (fixes issue with printing last store user regardless of audio input)
    RECOGNITION_THRESHOLD = 0.5  # May need to adjust
    VOLUME_THRESHOLD = 1000      # Microphone sensitivity
    recognition_start_time = time() ##RGB

    try:
        while True:
            audio_frame = recorder.read()
            rms_value = calculate_rms(audio_frame)

            if rms_value > VOLUME_THRESHOLD:
                scores = eagle.process(audio_frame)
                if scores:
                    highest_score = max(scores)
                    highest_score_index = scores.index(highest_score)
                    if highest_score > RECOGNITION_THRESHOLD:
                        print(f"{profile_files[highest_score_index].split('_')[0]} is speaking.")
                        led_controller.set_color((0, 0, 1))  # Set the LED to blue#RGB
                    else:
                        print("User not recognized.")
                        led_controller.set_color((1, 0, 0))  # Set the LED to red#RGB
                        led_controller.sound_alarm() #buzzer

            if time() - recognition_start_time > 5:#RGB
                print("Speaker recognition timed out.")#RGB
                led_controller.set_color((1, 0, 1))  # Set the LED to red  # Turn the RGB light red for timeout#RGB
                break  # Exit the loop after 5 seconds without recognition#RGB

            # If below the volume threshold, do nothing (silence)
    except KeyboardInterrupt:
        pass

    recorder.stop()
    recorder.delete()
    eagle.delete()

def calculate_rms(frame):
    # If the frame is a list of integers (fixes conversion), pack them into bytes
    if isinstance(frame, list):
        # Format string for 'struct.pack' for a list of integers (16bit)
        format_str = f'{len(frame)}h'
        frame_bytes = struct.pack(format_str, *frame)
    else:
        frame_bytes = frame  # Assume already in bytes

    count = len(frame_bytes) // 2
    shorts = struct.unpack(f'{count}h', frame_bytes)  # Unpack bytes back to a list of integers
    sum_squares = sum(s ** 2 for s in shorts)
    return math.sqrt(sum_squares / count)

## Add wakeword and speechtotext
def listen_for_wake_word_and_password(access_key, keyword_path, expected_password, timeout=10):
    # Initialize Porcupine for wake word detection
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[keyword_path]
    )

    # Initialize Cheetah for speech-to-text
    cheetah = pvcheetah.create(access_key=access_key)

    recorder = PvRecorder(device_index=10, frame_length=porcupine.frame_length)
    recorder.start()

    try:
        ##added while True:
        while True:
            print("Listening for wake word...")
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected! Listening for the voice password...")

                # Start capturing and processing speech after wake word detection
                transcript = ""
                timeout = 15
                end_time = time.time() + timeout

                while time.time() < end_time:
                    pcm = recorder.read()
                    partial_transcript, is_endpoint = cheetah.process(pcm)
                    transcript += partial_transcript
                    print(f"Partial Transcript: {partial_transcript}")

                    # Check if the expected password is within the transcript
                    if expected_password.lower() in transcript.lower():
                        print("Voice password matched! Arming Guardian...")
                        arm_system()
                        return True

                print("Voice password not detected within the time limit. Try again.")
                return False

    finally:
        recorder.stop()
        recorder.delete()
        porcupine.delete()
        cheetah.delete()

# Example function usage to start the listener as a thread in Guardian_main.py
def start_voice_recognition_thread():
    access_key = "UQOnRaJ10JVpaGU0XYreQaSBIV+JMUU387+IzalVU+C2U1bAyvC4EQ=="
    keyword_path = "Hey-Guardian_en_raspberry-pi_v3_0_0.ppn"
    expected_password = "arm"
    while True:
        detected = listen_for_wake_word_and_password(access_key, keyword_path, expected_password)
        if detected:
            print("Wake word if loop here")
    time.sleep(0.30)
