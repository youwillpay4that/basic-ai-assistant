
from dotenv_vault import load_dotenv
from pygame import mixer
import google.generativeai as genai
import speech_recognition as sr
import playsound as psound
import pyttsx3
import edge_tts
import os, time, threading
import smokesignal

import audio as audio_handler
import configs
load_dotenv()

# Init text to speech engine
tts_engine = pyttsx3.init()
mixer.init() #Initialzing pyamge mixer

wake_word = configs.wake_word.lower()
output_file = configs.output_file
input_file = configs.input_file


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

gemini_model = genai.GenerativeModel(
    model_name = configs.model_name,
    safety_settings = configs.safety_settings,
    generation_config = genai.GenerationConfig(
        max_output_tokens = configs.max_output_tokens,
        temperature = configs.temperature,
    )
)

# Print output
def print_string(s):
    if configs.print_output:
        print(s)

# Print output with time
start_time = time.time()
def tprint(s=""):
    if configs.time_trials: print(s,round(time.time()-start_time),2)

# Play sound asyncronously
def aplay_sound(filename):
    threading.Thread(target=play_sound, args=(filename,), daemon=True).start()
# Play sound
def play_sound(filename):
    psound.playsound("Sounds/"+filename)


# Get Ai Generated Response from Bot
def generate_response(chat, prompt):
    response = chat.send_message(configs.personality + prompt)
    
    return response.text


# Respond to 
def listen_callback(recognizer, audio, is_processing, chat):
    if is_processing: return 
    
    tprint("Hit callback!")

    filename = "input.wav"
    text = ""

    with open(filename, "wb") as f:
        # Write data into audiofile
        f.write(audio.get_wav_data())
    try:
        text = audio_handler.audio_to_text(filename)

        if text == None: return

        tprint("Transcribing done! ")
        aplay_sound("wakeup.wav")

    except Exception as e:
        # Failed for some reason
        print_string("And error occured in listen_callback: {}".format(e))
        smokesignal.emit("prompt_finished")
        return
    
    smokesignal.emit("prompt_started")

    print_string(f"I heard: {text} ")

    if text != None and " " in text:
        ##aplay_sound("wakeup.wav")
        response = generate_response(chat, text)

        print_string("Bot says: "+response)
        tprint("Speaking result! ")
        audio_handler.speak_text(response)
   
    
    smokesignal.emit("prompt_finished")


def main():
    chat = gemini_model.start_chat(history=[])

    running = True
    
    recognizer = sr.Recognizer()
    audio_source = sr.Microphone()
    sr.Microphone(chunk_size=configs.chunk_size, sample_rate=configs.sample_rate)

    # with sr.Microphone() as audio_source:
    # recognizer.adjust_for_ambient_noise(source=audio_source, duration=2)
    
    print("Running!")
    
    is_processing = False

    def interaction_began():
        nonlocal is_processing
        is_processing = True

    def interaction_ended():
        nonlocal is_processing
        is_processing = False

    # Work around not having an async function!
    def simple_callback(r, a):
        listen_callback(r, a, is_processing, chat)


    stop_func = recognizer.listen_in_background(audio_source, callback=simple_callback)

    # Stop listening once prompt has begun
    smokesignal.on("prompt_started", interaction_began)

    # Resume listening once prompt has finished
    smokesignal.on("prompt_finished", interaction_ended)


    while running:
        time.sleep(0.5)


if __name__ == "__main__":
    main()