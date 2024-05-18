# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import serial  # Biblioteca para comunicação serial

# Definição da variável global
global portaSerie

portName="COM3"
portaSerie = serial.Serial(portName)
portaSerie.baudrate = 9600
portaSerie.bytesize = 8
portaSerie.parity = 'N'
portaSerie.stopbits = 1
print('Serial Port Connected')

while True:
    data = portaSerie.readline()
    if data.startswith(b"S"):
        data = data.lstrip(b"S")
        data = data.rstrip(b"\r\n")
        data = data.decode("utf-8")
        split_data = data.split(",")
        print("Item1:", split_data[0], "Item2:", split_data[1], "Item3:", split_data[2], "Item4:", split_data[3],
              "Item5:", split_data[4], "Item6:", split_data[5])
