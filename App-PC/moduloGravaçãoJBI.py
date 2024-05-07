# Importação de bibliotecas
import json  # Biblioteca para manipulação de ficheiros JSON

global firstrung
global lastrung


# Grava os dados do sensor
def record(pose_now, firstrung, lastrung, ig, speed, debug):
    # Verificar se é a primeira vez que o módulo é corrido
    if firstrung:
        print("Para parar insira 'h'")
        ficheiro = open("gravacao.txt", "w")
        firststring = "NOP\n"
        ficheiro.write(firststring)
        ficheiro.close()
        firstrung = False
        if debug == "s":
            print("Play - firststring:", firststring)
        return firstrung
    if not firstrung and not lastrung:
        ficheiro = open("gravacao.txt", "a")  # Abrir o ficheiro para adicionar
        if 1 <= ig < 10:
            string = ("SETJOINT P00" + ig + " " + pose_now[0] + "," + pose_now[1] + "," + pose_now[2] + "," + pose_now[3]
                      + "," + pose_now[4] + "," + pose_now[5])
        elif 10 <= ig < 100:
            string = ("SETJOINT P0" + ig + " " + pose_now[0] + "," + pose_now[1] + "," + pose_now[2] + "," + pose_now[3]
                      + "," + pose_now[4] + "," + pose_now[5])
        elif 100 <= ig < 255:
            string = ("SETJOINT P" + ig + " " + pose_now[0] + "," + pose_now[1] + "," + pose_now[2] + "," + pose_now[3]
                      + "," + pose_now[4] + "," + pose_now[5])
        ficheiro.write(string)
        if 1 <= ig < 10:
            string = "P00" + ig
        elif 10 <= ig < 100:
            string = "P0" + ig
        elif 100 <= ig < 255:
            string = "P" + ig
        string = "MOVJ " + string + " VJ=" + speed + "% CR=0.0MM ACC=50 DEC=50\n"
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
        ig = 0
        if debug == "s":
            print("Play - laststring:", laststring)
        return firstrung, lastrung, ig


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
