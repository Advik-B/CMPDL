from winsound import Beep, PlaySound
from random import choice, randint

sounds = ("DeviceDisconnect", "DeviceConnect", "SystemAsterisk")


while True:
    PlaySound(choice(sounds), 0)
    Beep(randint(37, 32767), randint(100, 6000))
