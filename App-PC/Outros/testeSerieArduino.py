# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import serial  # Biblioteca para comunicação serial

# Definição da variável global
global portaSerie

portName = "COM3"
portaSerie = serial.Serial(portName)
portaSerie.baudrate = 115200
portaSerie.bytesize = 8
portaSerie.parity = 'N'
portaSerie.stopbits = 1
print('Serial Port Connected')

while True:
    data = portaSerie.readline()
    data = portaSerie.readline().decode('utf-8').rstrip()
    data = data.split(',')
    data = [-float(data[1]), -float(data[0]), -float(data[2]), float(data[4]), float(data[3]), float(data[5]),
            float(data[6])]
    print(data)
