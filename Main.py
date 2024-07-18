# Video Source: https://www.youtube.com/watch?v=8z8Cobsvc9k

import os
import time
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
from dotenv_vault import load_dotenv

global last_prompt_time

load_dotenv()

# Init text to speech engine
tts_engine = pyttsx3.init()

wake_word = "hey jarvis"
last_prompt_time = time.time()
convo_wait_time = 8

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config = genai.GenerationConfig(
        max_output_tokens = 100,
        temperature = 0.9,
    )
)

def play_sound(filename):
    psong = AudioSegment.from_wav("Sounds/"+filename)
    play(psong)


def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unkown error")


def generate_response(chat, prompt):
    response = chat.send_message(prompt)

    t = response.text.replace("*","")
    t = t.replace("👋","")
    t = t.replace("😊","")

    return t


def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


def main():
    chat = model.start_chat(history=[])
    is_convo = False

    while True:
        # Wait for wake up word to be said
        print(f"Say {wake_word} to begin your question")
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            if is_convo:
                play_sound("wakeup.wav")

            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                can_continue = is_convo

                # if not in a convo and wake word is said
                if not is_convo and transcription.lower() == wake_word:
                    can_continue = True

                
                if can_continue:
                    if not is_convo:
                        play_sound("wakeup.wav")
                    else:
                        play_sound("sound2.wav")

                    # Record audio
                    filename = "input.wav"
                    print("Listening...")
                    text = ""

                    if is_convo == False:
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1
                            audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)

                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())

                            # Transcribe audio to text
                            text = audio_to_text(filename)
                    else:
                        text = transcription.lower()
                    
                    if text:
                        play_sound("sound2.wav")

                        print(f" I heard: {text}")
                        # Replace with custom commands here

                        # Generate response from GPT-3
                        response = generate_response(chat, text)
                        print(f"Gemini says: {response}")
                        is_convo = True
                        # Read response using tts
                        speak_text(response)

            except Exception as e:
                # Failed for some reason
                is_convo = False
                print("And error occured: {}".format(e))


if __name__ == "__main__":
    main()


