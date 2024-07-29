
from pygame import mixer
import time
mixer.init() #Initialzing pyamge mixer


print("Playing",time.time())
a = mixer.Sound("output.wav")
a.play() #Playing Music with Pygame

time.sleep(5)

print("Stopping", time.time())
a.stop()
print("fine",time.time())