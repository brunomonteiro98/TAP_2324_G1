# Grava os dados do sensor
def record(p_target, firstrung, lastrung, g, speed):
    if firstrung:
        ficheiro = open("gravacaoJBI.jbi", "w")
        firststring = "NOP\n"
        ficheiro.write(firststring)
        ficheiro.close()
        firstrung = False
        return firstrung, lastrung, g
    if not firstrung and not lastrung:
        ficheiro = open("gravacaoJBI.jbi", "a")
        string = ("SETJOINT P001 " + str(p_target[0]) + "," + str(p_target[1]) + "," + str(p_target[2]) + "," + str(
            p_target[3]) + "," + str(p_target[4]) + "," + str(p_target[5]) + "\n")
        ficheiro.write(string)
        string = "MOVJ P001 VJ=" + str(speed) + "% CR=0.0MM ACC=50 DEC=50\n"
        ficheiro.write(string)
        ficheiro.close()
        return firstrung, lastrung, g
    if lastrung:
        ficheiro = open("gravacaoJBI.jbi", "a")
        laststring = "END"
        ficheiro.write(laststring)
        lastrung = False
        firstrung = True
        return firstrung, lastrung, g


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
