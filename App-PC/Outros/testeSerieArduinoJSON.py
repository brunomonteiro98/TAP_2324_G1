# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import serial  # Biblioteca para comunicação serial

# Definição da variável global
global portaSerie

portName="COM3"
portaSerie = serial.Serial(portName)
portaSerie.baudrate = 115200
portaSerie.bytesize = 8
portaSerie.parity = 'N'
portaSerie.stopbits = 1
print('Serial Port Connected')

while True:
    data = portaSerie.readline()
    jdata = json.loads(str(data, 'utf-8'))
    data = [(jdata["Item1"]), (jdata["Item2"]), (jdata["Item3"]), (jdata["Item4"]),
            (jdata["Item5"]), (jdata["Item6"])]
    print(data)