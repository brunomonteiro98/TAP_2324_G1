# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import serial  # Biblioteca para comunicação serial

# Definição da variável global
global portaSerie

portName=input("Digite a porta serial: ")
portaSerie = serial.Serial(portName)
portaSerie.baudrate = 9600
portaSerie.bytesize = 8
portaSerie.parity = 'N'
portaSerie.stopbits = 1
print('Serial Port Connected')

debug=input("Debug (s/n): ")
while True:
    data = portaSerie.readline()
    jdata = json.loads(str(data, 'utf-8'))
    data = [(jdata["Item1"]), (jdata["Item2"]), (jdata["Item3"]), (jdata["Item4"]),
            (jdata["Item5"]), (jdata["Item6"])]
    if debug == "s":
        print("Serie - data:", data)
