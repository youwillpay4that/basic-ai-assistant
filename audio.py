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
current_audio = ""
whisper_model = ""

recognizer = sr.Recognizer()

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

def get_source():
    return sr.Microphone(chunk_size=math.trunc(configs.chunk_size), sample_rate=math.trunc(configs.sample_rate))

# Play sound asyncronously
def aplay_sound(filename):
    threading.Thread(target=play_sound, args=(filename,), daemon=True).start()

def is_playing():
    return mixer.get_busy()

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


def stop_speaking():
    if not current_audio: return
    current_audio.stop()

# Transcribe audio to text
def audio_to_text(audio, filename="whisper_transcribe.wav"):
    if configs.advanced_audio_recog:
        with open(filename, "wb") as f:
            # Write data into audiofile
            f.write(audio.get_wav_data())

        segments, info = whisper_model.transcribe(filename)
        text = "".join(part.text for part in segments)

        return text.lower()
    
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        print_string("Skipping, no hot word heard")
        