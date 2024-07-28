import speech_recognition as sr


print(sr.Microphone().SAMPLE_RATE) # 44100
print(sr.Microphone().CHUNK) # 1024