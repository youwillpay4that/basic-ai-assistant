# Homemade chatbot that interacts via audio!
# V1.0
from dotenv_vault import load_dotenv
from groq import Groq
import google.generativeai as genai
import speech_recognition as sr
import os, time

import audio as audio_handler
import configs
load_dotenv()

# -- Setup --
audio_handler.init() #Initialzing pyamge mixer

wake_word = configs.wake_word.lower()
output_file = configs.output_file
input_file = configs.input_file

# Init all AI services
groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

gemini_model = ""
if not configs.prompt_generation == "Groq":
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    gemini_model = genai.GenerativeModel(
        model_name = configs.google_model_name,
        safety_settings = configs.safety_settings,
        generation_config = genai.GenerationConfig(
            max_output_tokens = configs.google_max_output_tokens,
            temperature = configs.google_temperature,
        )
    )


# -- Helper Functions --

# Print output
def print_string(s):
    if configs.print_output:
        print(s)

# Print output with time
start_time = time.time()

def tprint(s=""):
    if configs.time_trials: print(s,round(time.time()-start_time,2))

def can_chat(text, is_convo):
    if text == None or text == "": return False
    if is_convo: return True
    if wake_word in text: return True 
    

# -- Main Functions --

# Get Ai Generated Response from Bot
def generate_response(chat, prompt):
    if configs.prompt_generation == "Groq":
        print_string("Using Groq")
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": configs.personality,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=configs.groq_model_name,
            max_tokens=configs.groq_max_output_tokens,
        )

        return chat_completion.choices[0].message.content

    print_string("Using Google")
    try:
        response = chat.send_message(configs.personality+"[User Message]: 2"+ prompt)
        text = response.text.replace("*","")
    except Exception as e:
        print("Error geneating Gemini reponse:",e)
        return "Empty"

    return text


# Check if user said the hot word
def handle_hotword(audio):
    try:
        text = audio_handler.audio_to_text(audio)
        if text == None: return

        if configs.hot_word in text:
            print_string("Heard hot word!")
            audio_handler.stop_speaking()
            return True

    except Exception as e:
        return
        
    return 


# Process input audio and act accordingly
def listen_callback(audio, chat, is_convo):
    tprint("Hit callback!")

    text = ""
    
    try:
        text = audio_handler.audio_to_text(audio)
        if text == None: return
        tprint("Transcribing done!")

    except Exception as e:
        # Failed for some reason
        print_string("And error occured in listen_callback: {}".format(e))
        return
 

    if can_chat(text, is_convo):
        audio_handler.aplay_sound("wakeup.wav")
        print_string(f"I heard: {text} ")

        response = generate_response(chat, text)
        audio_handler.speak_text(response)
        
        print_string("Bot says: "+response)
        tprint("Speaking result!")

        return True


# Main method
def main():
    chat = ""
    if not configs.prompt_generation == "Groq":
        chat = gemini_model.start_chat()

    running = True
    is_convo = False
    recognizer = sr.Recognizer()
    # with sr.Microphone() as audio_source:
    # recognizer.adjust_for_ambient_noise(source=audio_source, duration=2)
    
    print("Running!")
    
    
    with audio_handler.get_source() as audio_source:
        while running:
            # Regular prompt detection
            audio = recognizer.listen(audio_source)
            is_convo = listen_callback(audio, chat, is_convo)

            # Hotword detection
            if is_convo == True:
                while audio_handler.is_playing():
                    audio = recognizer.listen(audio_source, phrase_time_limit=3)
                    handle_hotword(audio)


if __name__ == "__main__":
    main()