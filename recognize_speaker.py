# recognize_speaker.py
import pveagle
from pvrecorder import PvRecorder
import os
import math
import struct

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
                    else:
                        print("User not recognized.")
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