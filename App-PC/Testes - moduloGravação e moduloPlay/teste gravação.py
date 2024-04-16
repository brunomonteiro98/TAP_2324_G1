import json

teste = [1, 2, 3, 4, 5, 6]
teste2 = [7, 8, 9, 10, 11, 12]

'''
ficheiro = open('teste.txt', 'w')
teste = [1, 2, 3, 4, 5, 6]
teste=[teste for i in range(0, 6)]
teste = json.dumps(teste)
ficheiro.write(teste)
ficheiro.close()
'''

ficheiro = open("teste.txt", "r")  # Abrir o ficheiro
rdata = ficheiro.readline()  # Ler a primeira linha
jdata = json.loads(rdata)  # Converter a ‘string’ para uma lista
ficheiro.close()  # Fechar o ficheiro
ficheiro = open("teste.txt", "w")  # Abrir o ficheiro
jdata = [jdata] + [teste2]  # Adicionar a nova pose
jdata = json.dumps(jdata)  # Converter a lista para uma ‘string’
ficheiro.write(jdata)  # Escrever a nova pose
ficheiro.close()  # Fechar o ficheiro
