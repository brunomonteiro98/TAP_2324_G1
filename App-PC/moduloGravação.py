# Impotação de bibliotecas
import json  # Biblioteca para manipulação de ficheiros JSON


# Grava os dados do sensor
def record(pose_now, firstrung, debug):
    # Verificar se é a primeira vez que o módulo é corrido
    if firstrung:
        print("Para parar insira 'h'")
        ficheiro = open("gravacao.txt", "w")
        jdata = json.dumps(pose_now)
        ficheiro.write(jdata)
        ficheiro.close()
        firstrung = False
        if debug == "s":
            print("Play - jdata:", jdata)
        return firstrung
    if not firstrung:
        ficheiro = open("gravacao.txt", "r")  # Abrir o ficheiro
        rdata = ficheiro.readline()  # Ler a primeira linha
        jdata = json.loads(rdata)  # Converter a ‘string’ para uma lista
        # Debug (se ativado)
        if debug == "s":
            print("Play - jdata:", jdata)
        ficheiro.close()  # Fechar o ficheiro
        ficheiro = open("gravacao.txt", "w")  # Abrir o ficheiro
        jdata = jdata + [pose_now]  # Adicionar a nova pose !!!linha super importante!!!
        # Debug (se ativado)
        if debug == "s":
            print("Play - jdata:", jdata)
        jdata = json.dumps(jdata)  # Converter a lista para uma ‘string’
        ficheiro.write(jdata)  # Escrever a nova pose
        ficheiro.close()  # Fechar o ficheiro
        # Debug (se ativado)
        if debug == "s":
            print("Play - rdata:", rdata)
            print("Play - jdata:", jdata)
        return
