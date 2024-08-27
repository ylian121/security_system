# enroll_speaker.py
import pveagle
from pvrecorder import PvRecorder
import os

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
