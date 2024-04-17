# Importar bibliotecas
import time  # Importar a biblioteca time
import json  # Importar a biblioteca json


# Função para ler o ficheiro
def play(i, debug):
    ficheiro = open("gravacao.txt", "r")  # Abrir o ficheiro
    rdata = ficheiro.readline()  # Ler a primeira linha
    jdata = json.loads(rdata)  # Converter a ‘string’ para uma lista
    ficheiro.close()  # Fechar o ficheiro
    data = jdata[i]  # Ler a linha i
    fichlen = len(jdata)  # Guardar o número de linhas do ficheiro
    # Debug (se ativado)
    if debug == "s":
        print("Play - i:", i)
        #print("Play - rdata:", rdata)
        #print("Play - jdata:", jdata)
        print("Play - data:", data)
    time.sleep(0.08)  # Esperar 80ms ???
    # Output
    return data, fichlen

if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
