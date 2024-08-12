# Overview
100% Voice to Voice, full customizable, and easy-to-use chatbot. It supports voice interaction with customizable audio cues. Tons of different voices and features built in! This is a personal project to create a better voice assistant for free.



# Full List of Features
- Edge TTS for fast and smooth voices, +300 choices
- Manny different languages including English, Chinese, Spanish and more
- Fast Audio Recognition by speech_recognition or faster_whisper for more advanced machines
- Google Gemini or Groq for generating responses
- Wake word recognition and interruption 
- Dynamic sentence processing
- Conversational response listening
- Hot word interruption
- Audio cues
- Fully customizable

# Quick Start
Clone repository
```
git clone https://github.com/youwillpay4that/basic-ai-assistant
```

Install dependencies
```
pip install -r requirements.txt
```

Create .env file for settings and your API keys. Get your own for free here: 
Google: https://aistudio.google.com/app/apikey
Groq: https://console.groq.com/keys
```
# inside your .env file
GOOGLE_API_KEY="API-KEY-HERE"
GROQ_API_KEY="API-KEY-HERE"
```

All done! Run Main.py to start your chatbot!

# Settings
All settings are in configs.py. Defualt settings are pre-loaded.
All audio cues are inside the Sounds folder, fully customizable.
