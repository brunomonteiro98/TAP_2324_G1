# Importação das bibliotecas necessárias
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
    data = data.decode('utf-8').rstrip()
    data = data.split(',')
    data = [0, 0, 0, float(data[3]), float(data[5]), float(data[4])]  # [x, y, z, roll, pitch, yaw] Não adicionar z!
    print(data)
