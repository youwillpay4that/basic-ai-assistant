import os, asyncio
import google.generativeai as genai
import speech_recognition as sr

import playsound as psound
import pyttsx3
import edge_tts
from dotenv_vault import load_dotenv

import configs

load_dotenv()

# Init text to speech engine
tts_engine = pyttsx3.init()
wake_word = configs.wake_word.lower()

output_file = "output.wav"
input_file = "input.wav"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel(
    configs.model_name,
    generation_config = genai.GenerationConfig(
        max_output_tokens = configs.max_output_tokens,
        temperature = configs.temperature,
    )
)

async def aplay_sound(filename):
    psound.playsound("Sounds/"+filename)

def play_sound(filename):
    psound.playsound("Sounds/"+filename)
    #task = asyncio.create_task(aplay_sound(filename))


def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print_string("Skipping unkown error")


def generate_response(chat, prompt):
    response = chat.send_message(configs.personality+prompt)

    t = response.text.replace("*","")
    t = t.replace("👋","")
    t = t.replace("😊","")
    
    return t


async def speak_text(text):
    communicate = edge_tts.Communicate(text, configs.chosen_voice)
    await communicate.save(output_file)
    psound.playsound(output_file)


def print_string(s):
    if configs.print_output:
        print(s)

async def amain():
    chat = model.start_chat(history=[])
    is_convo = False
    print("Running...")

    while True:
        # Wait for wake up word to be said
        print_string(f"Say {wake_word} to begin your question")
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            if is_convo:
                play_sound("wakeup.wav")

            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                can_continue = is_convo

                # if not in a convo and wake word is said
                if not is_convo and wake_word in transcription.lower():
                    can_continue = True

                
                if can_continue:
                    if is_convo:
                        play_sound("sound2.wav")

                    # Record audio
                    filename = "input.wav"
                    text = ""

                    if is_convo == False:
                        print_string("Listening...")
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1

                            play_sound("wakeup.wav")
                            audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)

                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())

                            # Transcribe audio to text
                            text = audio_to_text(filename)
                            
                            play_sound("sound2.wav")
                    else:
                        text = transcription.lower()
                    
                    if text:
                        print_string(f" I heard: {text}")

                        # Generate response from Gemini
                        response = generate_response(chat, text)
                        print_string(f"Gemini says: {response}")
                        is_convo = True

                        # Read response using tts
                        finish = speak_text(response)
                        # set up hotkey interruption here
                        await finish
                         

            except Exception as e:
                # Failed for some reason
                is_convo = False
                print_string("And error occured: {}".format(e))


if __name__ == "__main__":
    asyncio.run(amain())


