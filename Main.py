
from faster_whisper import WhisperModel
from dotenv_vault import load_dotenv
import google.generativeai as genai
import speech_recognition as sr
import playsound as psound
import pyttsx3
import edge_tts
import os, asyncio, time, threading
import smokesignal



import configs
load_dotenv()

# Init text to speech engine
tts_engine = pyttsx3.init()
wake_word = configs.wake_word.lower()

output_file = "output.wav"
input_file = "input.wav"
#print(os.environ["OPENAI_API_KEY"])
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#openai_client = openai(api_key=os.environ["OPENAI_API_KEY"])

gemini_model = genai.GenerativeModel(
    model_name = configs.model_name,
    safety_settings = configs.safety_settings,
    generation_config = genai.GenerationConfig(
        max_output_tokens = configs.max_output_tokens,
        temperature = configs.temperature,
    )
)

whisper_model = ""
if configs.advanced_audio_recog:
    whisper_model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
        cpu_threads=2,
        num_workers=2,
    )

# Print output
def print_string(s):
    if configs.print_output:
        print(s)


start_time = time.time()
def tprint(s=""):
    if configs.time_trials: print(s,round(time.time()-start_time),1)

# Play sound asyncronously
def aplay_sound(filename):
    threading.Thread(target=play_sound, args=(filename,), daemon=True).start()

def play_sound(filename):
    psound.playsound("Sounds/"+filename)
    #task = asyncio.create_task(aplay_sound(filename))


# Get Ai Generated Response from Bot
def generate_response(chat, prompt):
    response = chat.send_message(configs.personality + prompt)
    
    return response.text

# Speak the audio out loud
def speak_text(text):
    communicate = edge_tts.Communicate(text, configs.chosen_voice)

    with open(output_file, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])

    psound.playsound(output_file)
    smokesignal.emit("finished_speaking")


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


def listen_callback(recognizer, audio, is_processing, chat):
    if is_processing: return 
    
    tprint("Hit callback!")

    filename = "input.wav"
    text = ""

    with open(filename, "wb") as f:
        # Write data into audiofile
        f.write(audio.get_wav_data())

    try:
        text = audio_to_text(filename)
        tprint("Transcribing done! ")
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
        speak_text(response)
   
    
    smokesignal.emit("prompt_finished")


def main():
    chat = gemini_model.start_chat(history=[])

    running = True
    
    recognizer = sr.Recognizer()
    audio_source = sr.Microphone()
   # with sr.Microphone() as audio_source:
    #    recognizer.adjust_for_ambient_noise(source=audio_source, duration=2)
    
    print("Running!")
    
    is_processing = False

    def interaction_began():
        nonlocal is_processing
        is_processing = True

    def interaction_ended():
        nonlocal is_processing
        is_processing = False

    # Call the listen function again
    def listen_again():
        nonlocal is_processing
        is_processing = True
        # nonlocal stop_func
        # stop_func = recognizer.listen_in_background(audio_source, callback=listen_callback)
        # smokesignal.once("prompt_started", custom_stop)

        print("got here")

    # Work around not having an async function!
    def simple_callback(r, a):
        listen_callback(r, a, is_processing, chat)

    stop_func = recognizer.listen_in_background(audio_source, callback=simple_callback)

    smokesignal.on("")

    # Stop listening once prompt has begun
    smokesignal.on("prompt_started", interaction_began)

    # Resume listening once prompt has finished
    smokesignal.on("prompt_finished", interaction_ended)


    while running:
        time.sleep(0.5)


if __name__ == "__main__":
    main()