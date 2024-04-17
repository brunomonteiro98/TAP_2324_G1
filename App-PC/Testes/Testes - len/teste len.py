import json

ficheiro = open("gravacao.txt", "r")  # Abrir o ficheiro
rdata = ficheiro.readline()  # Ler a primeira linha
jdata = json.loads(rdata)  # Converter a ‘string’ para uma lista
ficheiro.close()  # Fechar o ficheiro

comp=len(jdata)  # Guardar o número de linhas do ficheiro
print(comp)  # Guardar o número de linhas do ficheiro
