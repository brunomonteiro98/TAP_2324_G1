# Importar bibliotecas
import time  # Importar a biblioteca time
import json  # Importar a biblioteca json


# Função para ler o ficheiro
def play(i, debug):
    ficheiro = open("ficheiro.txt", "r")  # Abrir o ficheiro
    rdata = ficheiro.readline()  # Ler a primeira linha
    jdata = json.loads(rdata)  # Converter a ‘string’ para uma lista
    fichlen = len(jdata)  # Guardar o número de linhas do ficheiro
    data = jdata[i]  # Ler a linha i
    ficheiro.close()  # Fechar o ficheiro
    # Debug (se ativado)
    if debug == "s":
        print("Play - i:", i)
        print("Play - rdata:", rdata)
        print("Play - jdata:", jdata)
        print("Play - data:", data)
    time.sleep(0.02)  # Esperar 20ms
    # Output
    return data, fichlen
