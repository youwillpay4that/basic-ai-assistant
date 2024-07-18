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

wake_word = "hey Jarvis"
last_prompt_time = time.time()
global boolean_convo
boolean_convo = False
convo_wait_time = 8

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def play_sound(filename):
    psong = AudioSegment.from_wav("/Sounds/"+filename)
    play(psong)


def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unkown error")


def generate_response(prompt):
    response = model.generate_content("Respond with less than 100 words, SHORT. "+prompt)
    t = response.text.replace("*","")
    t = t.replace("👋","")
    t = t.replace("😊","")
    return t


def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    global last_prompt_time
    last_prompt_time = time.time()
    ##global boolean_convo
    boolean_convo = True

def main():
    while True:
        # Wait for wake up word to be said
        print(f"Say {wake_word} to begin your question")
        recognizer = sr.Recognizer()

        if time.time() - last_prompt_time <= convo_wait_time:
            play_sound("wakeup.wav")

        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                #play_sound("wakeup.wav")
                can_continue = False

                global boolean_convo
                if boolean_convo == True:
                    can_continue = True

                # if there has been an extra long pause, and wake word is said
                if time.time() - last_prompt_time > convo_wait_time and transcription.lower() == wake_word:
                    can_continue = True
                
                # If short pause after taking, continue
                # if time.time() - last_prompt_time <= convo_wait_time and transcription.lower() != "":
                #     can_continue = True
                #     is_convo = True


                if can_continue:
                    play_sound("sound2.wav")

                    # Record audio
                    filename = "input.wav"
                    print("Listening...")
                    text = ""
                    if boolean_convo == False:
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1
                            audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)
                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())

                            # Transcribe audio to text
                            text = audio_to_text(filename)
                    else:
                        print("Used convo!")
                        text = transcription.lower()
                    
                    if text:

                        print(f" I heard: {text}")
                        # Replace with custom commands here

                        # Generate response from GPT-3
                        response = generate_response(text)
                        print(f"Gemini says: {response}")

                        # Read response using tts
                        speak_text(response)

            except Exception as e:
                #global boolean_convo
                #boolean_convo = False
                print("And error occured: {}".format(e))


if __name__ == "__main__":
    main()


