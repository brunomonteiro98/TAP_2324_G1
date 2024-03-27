'''
import mouse
import keyboard

events = []                 #This is the list where all the events will be stored
mouse.hook(events.append)   #starting the mouse recording
keyboard.wait("a")          #Waiting for 'a' to be pressed
mouse.unhook(events.append) #Stopping the mouse recording
mouse.play(events)          #Playing the recorded events

# Temos de substituir o mouse pelo sensor e keyboard pelo butão de gravação

ficheiro = open("ficheiro1.txt", "r+", newline='\n')
events = [1, 2, 3, 4, 5, 6]
for i in range(1, 5):
    ficheiro.write(str(events)+'\n')
    i = i + 1
output = ficheiro.readlines()
for i in range(1, 5):
    print(output[i])
ficheiro.close()
'''


# Grava os dados do sensor
def record(pose_now, firstrung):
    # Verificar se é a primeira vez que o módulo é corrido
    if firstrung:
        print("Para parar insira 'h'")
        ficheiro = open("ficheiro1.txt", "w", newline='\n')
        ficheiro.write(str(pose_now) + '\n')
        ficheiro.close()
        firstrung = False
        return firstrung
    if not firstrung:
        ficheiro = open("ficheiro1.txt", "a", newline='\n')
        ficheiro.write(str(pose_now) + '\n')
        ficheiro.close()
        return
