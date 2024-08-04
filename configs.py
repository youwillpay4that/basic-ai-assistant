# Google Gemini
model_name = "gemini-1.5-flash-latest"
max_output_tokens = 200 
temperature = 1.5
print_output = True

safety_settings=[
 {
    'category': "HARM_CATEGORY_HATE_SPEECH",
    'threshold': "BLOCK_NONE"
 },
 {
    'category': "HARM_CATEGORY_HARASSMENT",
    'threshold': "BLOCK_NONE"
 },
 {
    'category': "HARM_CATEGORY_DANGEROUS_CONTENT",
    'threshold': "BLOCK_NONE"
 },
]

# Customization
wake_word = "jarvis" 
personality = "Be creative and a little sarcastic. Keep answers SHORT. "
hot_word = "tiger"

# Edge TTS Settings
voices = ['en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', "en-US-EricNeural", "en-HK-YanNeural", "en-NG-EzinneNeural"]
chosen_voice = voices[5]