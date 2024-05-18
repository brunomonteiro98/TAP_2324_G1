# Grava os dados do sensor
def record(p_target, firstrung, lastrung, g, speed, debug):
    if firstrung:
        ficheiro = open("gravacaoJBI.txt", "w")
        firststring = "NOP\n"
        ficheiro.write(firststring)
        ficheiro.close()
        firstrung = False
        if debug == "s":
            print("Play - firststring:", firststring)
        return firstrung, lastrung, g
    if not firstrung and not lastrung:
        ficheiro = open("gravacaoJBI.txt", "a")  # Abrir o ficheiro para adicionar
        string = ("SETJOINT P001 " + str(p_target[0]) + "," + str(p_target[1]) + "," + str(p_target[2]) + "," + str(p_target[3]) + "," + str(p_target[4]) + "," + str(p_target[5]) + "\n")
        ficheiro.write(string)
        string = "MOVJ P001 VJ=" + str(speed) + "% CR=0.0MM ACC=50 DEC=50\n"
        ficheiro.write(string)  # Escrever a nova pose
        ficheiro.close()  # Fechar o ficheiro
        # Debug (se ativado)
        if debug == "s":
            print("Gravação - string:", string)
        return firstrung, lastrung, g
    if lastrung:
        ficheiro = open("gravacaoJBI.txt", "a")  # Abrir o ficheiro para adicionar
        laststring = "END"
        ficheiro.write(laststring)
        lastrung = False
        if debug == "s":
            print("Play - laststring:", laststring)
        return firstrung, lastrung, g


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
