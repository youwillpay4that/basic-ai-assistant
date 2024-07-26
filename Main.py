
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

# Play sound asyncronously
def aplay_sound(filename):
    threading.Thread(target=play_sound, args=(filename,), daemon=True).start()

def play_sound(filename):
    psound.playsound("Sounds/"+filename)
    #task = asyncio.create_task(aplay_sound(filename))


# Get Ai Generated Response from Bot
def generate_response(chat, prompt):
    response = chat.send_message(configs.personality+prompt)

    t = response.text.replace("*","")
    t = t.replace("👋","")
    t = t.replace("😊","")
    
    return t

# Speak the audio out loud
async def speak_text(text):
    communicate = edge_tts.Communicate(text, configs.chosen_voice)
    await communicate.save(output_file)
    psound.playsound(output_file)

def audio_to_text(filename):
    segments, info = whisper_model.transcribe(filename)
    text = "".join(part.text for part in segments)

    return text


def listen_callback(recognizer, audio):
    try:
        filename = "input.wav"
        with open(filename, "wb") as f:
            # Write data into audiofile
            f.write(audio.get_wav_data())

        text = audio_to_text(filename)
        
        print_string("I heard: ",text)

        if wake_word in text:
            aplay_sound("wakeup.wav")
            reponse = generate_response(chat, text)
            speak_text(reponse)
    except:
        smokesignal.emit("prompt_finished")
        return
    
    smokesignal.emit("prompt_finished")



def begin_listening(recognizer, audio_source):
    stop_func = recognizer.listen_in_background(audio_source, callback=listen_callback)
    good = True

    def exit():
        stop_func()
        good = False

    # Stop listening once the bot has begun speaking, (switch to hot word detection...)
    smokesignal.once("prompt_started", exit)

    while good:
        time.sleep(0.5)


async def main():
    global chat
    chat = gemini_model.start_chat(history=[])

    running = True
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as audio_source:
        recognizer.adjust_for_ambient_noise(source=audio_source, duration=2)
    
    print("Running!")
    
    begin_listening(recognizer, audio_source)
    smokesignal.on("prompt_finished", begin_listening)

    while running:
        time.sleep(0.5)


async def amain():
    chat = gemini_model.start_chat(history=[])
    
    recognizer = sr.Recognizer()
    audio_source = sr.Microphone()

    recognizer.adjust_for_ambient_noise(audio_source, 2)

    is_convo = False
    print("Running...")

    while True:
        # Wait for wake up word to be said
        print_string(f"Say {wake_word} to begin your question")
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            if is_convo:
                aplay_sound("wakeup.wav")               
                #asyncio.create_task(aplay_sound("wakeup.wav"))

            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                can_continue = is_convo

                # if not in a convo and wake word is said
                if not is_convo and wake_word in transcription.lower():
                    can_continue = True
                
                if can_continue:
                    if is_convo:
                        aplay_sound("sound2.wav")

                    # Record audio
                    filename = "input.wav"
                    text = ""

                    if is_convo == False:
                        print_string("Listening...")
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1

                            aplay_sound("wakeup.wav")
                            audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)

                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())

                            # Transcribe audio to text
                            text = audio_to_text(filename)
                            
                            aplay_sound("sound2.wav")
                    else:
                        text = transcription.lower()
                    
                    if text:
                        print_string(f" I heard: {text}")

                        # Generate response from Gemini
                        response = generate_response(chat, text)
                        print_string(f"Gemini says: {response}")
                        is_convo = True

                        # Read response using tts
                        speaking_task = asyncio.create_task(speak_text(response))
                        
                        await speaking_task
                         

            except Exception as e:
                # Failed for some reason
                is_convo = False
                print_string("And error occured: {}".format(e))


if __name__ == "__main__":
    asyncio.run(main())
    #main()