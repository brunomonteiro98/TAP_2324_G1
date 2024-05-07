# Importação de bibliotecas
import json  # Biblioteca para manipulação de ficheiros JSON

global firstrung
global lastrung

# Grava os dados do sensor
def record(pose_now, firstrung, lastrung, debug):
    # Verificar se é a primeira vez que o módulo é corrido
    if firstrung:
        print("Para parar insira 'h'")
        ficheiro = open("gravacao.txt", "w")
        firststring = "NOP\n"  #!!!!!!!!!!!!! continuar com velocidades, acelerações .....
        ficheiro.write(firststring)
        ficheiro.close()
        firstrung = False
        if debug == "s":
            print("Play - firststring:", firststring)
        return firstrung, lastrung
    if not firstrung and not lastrung:
        ficheiro = open("gravacao.txt", "a")  # Abrir o ficheiro para adicionar
        string = "MOVJ" + pose_now + "\n"
        ficheiro.write(string)  # Escrever a nova pose
        ficheiro.close()  # Fechar o ficheiro
        # Debug (se ativado)
        if debug == "s":
            print("Gravação - string:", string)
        return
    if lastrung:
        ficheiro = open("gravacao.txt", "a")  # Abrir o ficheiro para adicionar
        laststring = "END"
        ficheiro.write(laststring)
        lastrung = False
        if debug == "s":
            print("Play - laststring:", laststring)
        return firstrung, lastrung


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
