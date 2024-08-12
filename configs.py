from google.generativeai.types import HarmCategory, HarmBlockThreshold
import speech_recognition as sr
import math

# General Settings
prompt_generation = "Google" # Google or Groq. Google for better responses, Groq for speed
wake_word = "jarvis"
hot_word = "stop"
personality = f'''[System Message] You are a helpful AI assistant. 
Keep answers SHORT and DO NOT include "{hot_word}", in your response. '''
print_output = True # For debuging
time_trials = True

# Edge TTS Settings
voices = ['en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', "en-US-EricNeural", "en-NG-EzinneNeural"]
chosen_voice = voices[4] # List of voices in tts_voices.txt
speech_rate = "+10%"
speech_volume = "+0%"

# Google Gemini
google_model_name = "gemini-1.5-flash-latest"
google_max_output_tokens = 200 
google_temperature = 1.5

# Groq
groq_model_name = "llama3-8b-8192"
groq_max_output_tokens = 200 
groq_temperature = 1.5

safety_settings = {
   HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
   HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
   HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
   HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
} # BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE, BLOCK_NONE

# Audio Recog 
advanced_audio_recog = False
sample_rate = sr.Microphone().SAMPLE_RATE # 44.1K
chunk_size = math.trunc(sr.Microphone().CHUNK * 0.85) # 1024
output_file = "output.wav"
input_file = "input.wav"