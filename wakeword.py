import pvporcupine
from pvrecorder import PvRecorder
import pvcheetah
import time

porcupine = pvporcupine.create(
  access_key="UQOnRaJ10JVpaGU0XYreQaSBIV+JMUU387+IzalVU+C2U1bAyvC4EQ==",
  keyword_paths=["C:\\Users\\brian\\gitHub_Projects\\CS179J\\CS179J-Pajaka-Parnika-Yongyan-Briana\\Hey-Guardian_en_windows_v3_0_0\\Hey-Guardian_en_windows_v3_0_0.ppn"]
)

# Initialize Cheetah for speech-to-text
cheetah = pvcheetah.create(access_key="UQOnRaJ10JVpaGU0XYreQaSBIV+JMUU387+IzalVU+C2U1bAyvC4EQ==")

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
recorder.start()

try:
    print("Listening for wake word...")
    while True:
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected! Listening for the voice password...")

            # Start capturing and processing speech after wake word detection
            transcript = ""
            timeout = 10  # 10 seconds to say the passcode
            end_time = time.time() + timeout
            expected_password = "lock up"  # Replace with the actual voice password

            while time.time() < end_time:
                pcm = recorder.read()
                partial_transcript, is_endpoint = cheetah.process(pcm)
                transcript += partial_transcript
                print(f"Partial Transcript: {partial_transcript}")
                
                # Check if the expected password is within the transcript
                if expected_password.lower() in transcript.lower():
                    print("Voice password matched! Do something...")
                    break
            else:
                print("Voice password not detected within the time limit. Try again.")
            
finally:
    recorder.stop()
    recorder.delete()
    porcupine.delete()
    cheetah.delete()