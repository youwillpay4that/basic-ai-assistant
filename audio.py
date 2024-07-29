from faster_whisper import WhisperModel
from pygame import mixer
import wave
import speech_recognition as sr
import librosa
import playsound as psound
import edge_tts
import configs
import time
#from Main import print_string
output_file = configs.output_file

whisper_model = ""
if configs.advanced_audio_recog:
    whisper_model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
        cpu_threads=2,
        num_workers=2,
    )


def print_string(s):
    if configs.print_output:
        print(s)


    
print('wopw')
print(get_audio_length("output.wav"))
# Speak the audio out loud using edge_tts
def speak_text(text):
    communicate = edge_tts.Communicate(text, configs.chosen_voice)

    with open(output_file, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])

    sound = mixer.Sound(output_file)
    sound.play()

    time.sleep(get_audio_length(output_file))
    return 
    # def play():
    #     psound.playsound("output.wav")

    # thread = threading.Thread(target=play, daemon=True)
    # thread.start()
    # time.sleep(3)
    # thread.join()
    # psound.playsound(output_file)
    #smokesignal.emit("finished_speaking")

# Transcribe audio to text
def audio_to_text(filename):
    if configs.advanced_audio_recog:
        segments, info = whisper_model.transcribe(filename)
        text = "".join(part.text for part in segments)

        return text.lower()
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        print_string("Skipping unkown error")
