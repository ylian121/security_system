# enroll_speaker.py
import pveagle
from pvrecorder import PvRecorder
import os
import math
import struct
from time import time
# from led_alarm_servo import led_controller  # Import the LEDController instance

def enroll_speaker():

    access_key = "UQOnRaJ10JVpaGU0XYreQaSBIV+JMUU387+IzalVU+C2U1bAyvC4EQ=="

    # Update: Have user insert their name for their profile 
    speaker_name = input("Enter the speaker's name: ")

    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(f"Failed to create Eagle Profiler: {e}")
        exit(1)

    DEFAULT_DEVICE_INDEX = -1
    recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_profiler.min_enroll_samples
    )

    recorder.start()

    enroll_percentage = 0.0
    while enroll_percentage < 100.0:
        audio_frame = recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
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

    DEFAULT_DEVICE_INDEX = -1
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
