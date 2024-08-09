from faster_whisper import WhisperModel
from pygame import mixer
import speech_recognition as sr
import playsound as psound
import edge_tts
import configs
import time, math, threading
import smokesignal


#from Main import print_string
output_file = configs.output_file
current_audio
whisper_model = ""

if configs.advanced_audio_recog:
    whisper_model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
        cpu_threads=2,
        num_workers=2,
    )

def init():
    mixer.init()

# Play sound asyncronously
def aplay_sound(filename):
    threading.Thread(target=play_sound, args=(filename,), daemon=True).start()

# Play sound
def play_sound(filename):
    psound.playsound("Sounds/"+filename)

def print_string(s):
    if configs.print_output:
        print(s)

# Speak the audio out loud using edge_tts
def speak_text(text):
    communicate = edge_tts.Communicate(text, configs.chosen_voice)

    with open(output_file, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])

    sound = mixer.Sound(output_file)
    global current_audio
    current_audio = sound

    sound.play()
    print('played audio ._.')



def get_mixer():
    return mixer
    
def stop_speaking():
    if not current_audio: return
    current_audio.stop()

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

# init()
# speak_text("Hey Hey Hey. HeyHeyHeyHeyHey. ok buddy! Okay kid. HeyHeyHeyHeyHeyHeyHeyHeyHey!")
# time.sleep(3)
# stop_speaking()