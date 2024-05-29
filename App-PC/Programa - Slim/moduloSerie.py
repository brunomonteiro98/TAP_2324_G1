# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import serial  # Biblioteca para comunicação serial

# Definição da variável global
global portaSerie


# Função para conectar a porta serial
def connect_serial_port(portName):
    global portaSerie
    portaSerie = serial.Serial(portName)  # Cria o objeto da porta serial
    portaSerie.baudrate = 115200  # Configura a taxa de transmissão para 9600
    portaSerie.bytesize = 8  # Número de bits de dados = 8
    portaSerie.parity = 'N'  # Sem paridade
    portaSerie.stopbits = 1  # Número de stopbits = 1
    print('Serial Port Connected')


# Função para desconectar a porta serial
def close_serial_port():
    portaSerie.close()
    print('Serial Port Closed')


# Função para ler os dados disponíveis na porta serial
def read_serial_data(debug="n"):  # Função para ler os dados disponíveis na porta serial
    if portaSerie.in_waiting == 0:
        data = None
        return data
    else:
        data = portaSerie.readline().decode('utf-8').rstrip()
        data = data.split(',')
        data = [-float(data[1]), -float(data[0]), -float(data[2]), float(data[4]), float(data[3]), float(data[5]),
                float(data[6])]
        if debug == "s":
            print("Serie - data:", data)  # Imprime a mensagem recebida no terminal para debug
        return data


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
