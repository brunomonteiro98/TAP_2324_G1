# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import serial  # Biblioteca para comunicação serial

global portaSerie


# Função para conectar a porta serial
def connect_serial_port(portName):
    global portaSerie
    portaSerie = serial.Serial(portName)  # Cria o objeto da porta serial
    portaSerie.baudrate = 9600  # Configura a taxa de transmissão para 9600
    portaSerie.bytesize = 8  # Número de bits de dados = 8
    portaSerie.parity = 'N'  # Sem paridade
    portaSerie.stopbits = 1  # Número de stopbits = 1.
    print('Serial Port Connected')


# Função para desconectar a porta serial
def close_serial_port():
    portaSerie.close()
    print('Serial Port Closed')


# Função para ler os dados disponíveis na porta serial
def read_serial_data():  # Função para ler os dados disponíveis na porta serial
    data = portaSerie.readline()  # Lê a linha disponível
    jdata = json.loads(str(data, 'utf-8'))  # Converte a resposta para json
    data = [int(jdata["Item1"]), int(jdata["Item2"]), int(jdata["Item3"]), int(jdata["Item4"]), int(jdata["Item5"]),
            int(jdata["Item6"])]
    return data


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
