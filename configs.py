from google.generativeai.types import HarmCategory, HarmBlockThreshold
import speech_recognition as sr
import math

# Google Gemini
model_name = "gemini-1.5-flash-latest"
max_output_tokens = 200 
temperature = 1.5

print_output = True
advanced_audio_recog = False
time_trials = True

safety_settings = {
   HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
   HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
   HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
   HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
}

# Audio Recog 
sample_rate = sr.Microphone().SAMPLE_RATE # 44.1K
chunk_size = math.trunc(sr.Microphone().CHUNK * 0.85) # 1024
output_file = "output.wav"
input_file = "input.wav"

# Customization
wake_word = "jarvis" 
personality = "You are an AI assistant. Be creative and a little sarcastic. Keep answers SHORT. "
hot_word = "tiger"

# Edge TTS Settings
voices = ['en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', "en-US-EricNeural", "en-HK-YanNeural", "en-NG-EzinneNeural"]
chosen_voice = voices[5]