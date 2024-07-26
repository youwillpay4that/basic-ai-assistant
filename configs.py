from google.generativeai.types import HarmCategory, HarmBlockThreshold
# Google Gemini
model_name = "gemini-1.5-flash-latest"
max_output_tokens = 200 
temperature = 1.5
print_output = True

safety_settings = {
   HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
   HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
   HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
   HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
}

# Customization
wake_word = "dave" 
personality = "Be creative and a little sarcastic. Keep answers SHORT. "
hot_word = "tiger"

# Edge TTS Settings
voices = ['en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', "en-US-EricNeural", "en-HK-YanNeural", "en-NG-EzinneNeural"]
chosen_voice = voices[5]