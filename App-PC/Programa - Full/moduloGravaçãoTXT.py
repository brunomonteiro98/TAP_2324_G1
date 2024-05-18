# Importação de bibliotecas
import json  # Biblioteca para manipulação de ficheiros JSON


# Grava os dados do sensor
def record(pose_now, firstrung, debug):
    # Verificar se é a primeira vez que o módulo é corrido
    if firstrung:
        ficheiro = open("gravacaoTXT.txt", "w")
        pose_now = [pose_now] # Adicionar a nova pose !!!linha super importante!!!
        jdata = json.dumps(pose_now)
        ficheiro.write(jdata)
        ficheiro.close()
        firstrung = False
        if debug == "s":
            print("Play - jdata:", jdata)
        return firstrung
    if not firstrung:
        ficheiro = open("gravacaoTXT.txt", "r")  # Abrir o ficheiro
        rdata = ficheiro.readline()  # Ler a primeira linha
        jdata = json.loads(rdata)  # Converter a ‘string’ para uma lista
        # Debug (se ativado)
        if debug == "s":
            print("Gravação - jdata:", jdata)
        ficheiro.close()  # Fechar o ficheiro
        ficheiro = open("gravacaoTXT.txt", "w")  # Abrir o ficheiro
        jdata = jdata + [pose_now]  # Adicionar a nova pose !!!linha super importante!!!
        # Debug (se ativado)
        if debug == "s":
            print("Gravação - jdata:", jdata)
        jdata = json.dumps(jdata)  # Converter a lista para uma ‘string’
        ficheiro.write(jdata)  # Escrever a nova pose
        ficheiro.close()  # Fechar o ficheiro
        # Debug (se ativado)
        if debug == "s":
            print("Gravação - rdata:", rdata)
            print("Gravação - jdata:", jdata)
        return


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
