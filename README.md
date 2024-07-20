# Overview

100% Voice to Voice, full customizable, and easy-to-use chatbot built with Google Gemini. It supports voice interaction with customizable audio cues. This is a personal project to create a better voice assistant.


# Quick Start
Clone repository
```
git clone https://github.com/youwillpay4that/basic-ai-assistant
```

Install dependencies
```
pip install -r requirements.txt
```

Create .env file for settings and your Google API Key. You can view your current ones and get one for free here: https://aistudio.google.com/app/apikey
```
# inside your .env file
API_KEY = "YOUR-KEY-HERE"
```

All done! Run Main.py to start your chatbot!

# Settings
All settings are in configs.py. Defualt settings are pre-loaded.
```
model_name = # (str) Name of the model
max_output_tokens = # (int) Maximum tokens the bot will respond with. 100 - 400 is my recommended range
temperature = # (float) 0-2. 2 is very creative responses, 0 is determinsitic
wake_word =  # (str) Word that will wake up the bot
personality = # (str) Optional personality prompt sent with each response to the bot. Can leave blank if wished
print_output = # (bool) If the bot will also respond via terminal
```

All audio cues are inside the Sounds folder, fully customizable.
