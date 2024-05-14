# Importação de bibliotecas
import json  # Biblioteca para manipulação de ficheiros JSON


# Grava os dados do sensor
def record(pose_now, firstrung, lastrung, ig, speed, g, debug):
    # Verificar se é a primeira vez que o módulo é corrido
    if firstrung:
        ficheiro = open("gravacaoJBI.txt", "w")
        firststring = "NOP\n"
        ficheiro.write(firststring)
        ficheiro.close()
        firstrung = False
        if debug == "s":
            print("Play - firststring:", firststring)
        return firstrung, lastrung, ig, g
    if not firstrung and not lastrung:
        ficheiro = open("gravacaoJBI.txt", "a")  # Abrir o ficheiro para adicionar
        if 1 <= ig < 10:
            string = ("SETJOINT P00" + str(ig) + " " + str(pose_now[0]) + "," + str(pose_now[1]) + "," + str(pose_now[2])
                      + "," + str(pose_now[3]) + "," + str(pose_now[4]) + "," + str(pose_now[5]) + "\n")
        elif 10 <= ig < 100:
            string = ("SETJOINT P0" + str(ig) + " " + str(pose_now[0]) + "," + str(pose_now[1]) + "," + str(pose_now[2])
                      + "," + str(pose_now[3]) + "," + str(pose_now[4]) + "," + str(pose_now[5]) + "\n")
        elif 100 <= ig < 255:
            string = ("SETJOINT P" + str(ig) + " " + str(pose_now[0]) + "," + str(pose_now[1]) + "," + str(pose_now[2])
                      + "," + str(pose_now[3]) + "," + str(pose_now[4]) + "," + str(pose_now[5]) + "\n")
        elif ig == 255:
            ficheiro.close()  # Fechar o ficheiro
            lastrung = True
            g = 0
            return firstrung, lastrung, ig, g
        if ig != 255:
            ficheiro.write(string)
            if 1 <= ig < 10:
                string = "P00" + str(ig)
            elif 10 <= ig < 100:
                string = "P0" + str(ig)
            elif 100 <= ig < 255:
                string = "P" + str(ig)
            string = "MOVJ " + string + " VJ=" + str(speed) + "% CR=0.0MM ACC=50 DEC=50\n"
            ficheiro.write(string)  # Escrever a nova pose
            ficheiro.close()  # Fechar o ficheiro
            # Debug (se ativado)
            if debug == "s":
                print("Gravação - string:", string)
            return firstrung, lastrung, ig, g
    if lastrung:
        ficheiro = open("gravacaoJBI.txt", "a")  # Abrir o ficheiro para adicionar
        laststring = "END"
        ficheiro.write(laststring)
        lastrung = False
        ig = 0
        if debug == "s":
            print("Play - laststring:", laststring)
        return firstrung, lastrung, ig, g


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
