#Importação das bibliotecas necessárias
import serial # Biblioteca para comunicação serial

# Definição da variável global
global SerialObj

# Função para conectar a porta serial
def connect_serial_port():
    try:
        COMPort_Name = input("Porta COM (Ex:COM2) - ")
        SerialObj = serial.Serial(COMPort_Name) # Abre a porta serial
        SerialObj.baudrate = 9600  # Configura a taxa de transmissão para 9600
        SerialObj.bytesize = 8  # Número de bits de dados = 8
        SerialObj.parity = 'N'  # Sem paridade
        SerialObj.stopbits = 1  # Número de stopbits = 1.
    except serial.SerialException as var:
        print('An Exception Occured')
        print('Exception Details-> ', var)
    else:
        print('Serial Port Opened')

# Função para desconectar a porta serial
def close_serial_port():
    SerialObj.close()
    print('Serial Port Closed')

# Função para ler os dados disponíveis na porta serial
def read_serial_data(): # Função para ler os dados disponíveis na porta serial
    if SerialObj.in_waiting > 0: # Se houver dados disponíveis para leitura
        data = SerialObj.readline() # Lê a linha disponível

        # Importar como json deles!!! colocar no teams. para eles mandarem assim

        return data # Retorna a linha lida
    else: # Se não houver dados disponíveis
        return None # Retorna None se não houver dados disponíveis

if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass # Nada acontece