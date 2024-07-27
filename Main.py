
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
# async def speak_text(text):
#     communicate = edge_tts.Communicate(text, configs.chosen_voice)
#     await communicate.save(output_file)
#     psound.playsound(output_file)
#     smokesignal.emit("finished_speaking")

def speak_text(text):
    communicate = edge_tts.Communicate(text, configs.chosen_voice)

    with open(output_file, "wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

    psound.playsound(output_file)
    smokesignal.emit("finished_speaking")
    


def audio_to_text(filename):
    segments, info = whisper_model.transcribe(filename)
    text = "".join(part.text for part in segments)

    return text.lower()


def listen_callback(recognizer, audio):
    if processing:
        return 
    
    print("made to callback!")
    filename = "input.wav"
    text = ""

    with open(filename, "wb") as f:
        # Write data into audiofile
        f.write(audio.get_wav_data())

    try:
        text = audio_to_text(filename)
    except Exception as e:
        # Failed for some reason
        print_string("And error occured in listen_callback: {}".format(e))
        smokesignal.emit("prompt_finished")
        return
    
    smokesignal.emit("prompt_started")

    print_string(f"I heard:{text} ")

    if "a" in text:
        ##aplay_sound("wakeup.wav")
        response = generate_response(chat, text)

        print_string("Bot says:"+response)
        speak_text(response)
        # task = asyncio.create_task()
        
        # good = True

        # def call():
        #     nonlocal good
        #     good = False
        # smokesignal.once("finished_speaking",call)

        # while good:
        #     time.sleep(0.1)
   
    
    smokesignal.emit("prompt_finished")


async def main():
    global chat
    chat = gemini_model.start_chat(history=[])

    global processing
    processing = False
    running = True
    
    stop_func = None

    recognizer = sr.Recognizer()
    with sr.Microphone() as audio_source:
        recognizer.adjust_for_ambient_noise(source=audio_source, duration=2)
    
    print("Running!")
    
    is_processing = False

    def custom_stop():
        print("custom stop called ;)")
        # nonlocal stop_func
        # stop_func(False)
        nonlocal is_processing
        is_processing = True
        print("custom stop finished I see")

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
        listen_callback(r, a, is_processing)

    stop_func = recognizer.listen_in_background(audio_source, callback=simple_callback)

    smokesignal.on("")

    # Stop listening once prompt has begun
    smokesignal.on("prompt_started", custom_stop)

    # Resume listening once prompt has finished
    smokesignal.on("prompt_finished", listen_again)


    while running:
        time.sleep(0.5)


async def aoldmain():
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