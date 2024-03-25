"""

import mouse
import keyboard

events = []                 #This is the list where all the events will be stored
mouse.hook(events.append)   #starting the mouse recording
keyboard.wait("a")          #Waiting for 'a' to be pressed
mouse.unhook(events.append) #Stopping the mouse recording
mouse.play(events)          #Playing the recorded events

"""

# Temos de substituir o mouse pelo sensor e keyboard pelo butão de gravação