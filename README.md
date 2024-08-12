# Overview
100% Voice to Voice, full customizable, and easy-to-use chatbot. It supports voice interaction with customizable audio cues. Tons of different voices and features built in! This is a personal project to create a better voice assistant for free.


# Quick Start
Clone repository
```
git clone https://github.com/youwillpay4that/basic-ai-assistant
```

Install dependencies
```
pip install -r requirements.txt
```

Create .env file. This for keeping your API keys safe. Get your own for free here: 
Google: https://aistudio.google.com/app/apikey
Groq: https://console.groq.com/keys
```
# inside your .env file
GOOGLE_API_KEY="API-KEY-HERE"
GROQ_API_KEY="API-KEY-HERE"
```

All done! Run Main.py to start your chatbot!

# Settings
All settings are in configs.py. Settings such as wake and hot words, personality, voices, and much more are easily accessible.
All audio cues are inside the Sounds folder.

# Usage Guide
When speaking to the bot, all responses containing the wake word will be processed. The user can simply say "<wake_word>, where is Mount Everest?", and the bot will respond. To interupt simply say the hot word while the bot is speaking. If the bot has just replied or interupted, the user does not need to say the wake word for the following prompt. After a couple seconds the bot will sleep, and the wake word will be once again be required.

# Full List of Features
- Edge TTS for fast and smooth voices, +300 choices
- Many different languages TTS including English, Chinese, Spanish and many more
- Fast Audio Recognition by speech_recognition or faster_whisper for more advanced machines
- Google Gemini or Groq for generating responses
- Wake word recognition and interruption 
- Dynamic sentence processing
- Conversational response listening
- Hot word interruption
- Audio cues
- Fully customizable
