# Importação das bibliotecas necessárias
import json  # Biblioteca para manipulação de arquivos json
import socket  # Biblioteca para comunicação por socket
import sys

import keyboard


# Função para conectar ao controlador por Ethernet
# ip: endereço IP do controlador
# port: porta de comunicação com o controlador
# sock: socket de comunicação com o controlador
def connectETController(ip, port=8055):  #
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket
    sock.settimeout(2)  # Define o timeout do socket
    try:  # Tenta conectar ao controlador
        sock.connect((ip, port))  # Conecta ao controlador
        return (True, sock)  # Retorna sucesso e o socket
    except Exception as e:  # Se houver erro na conexão, retorna o erro
        sock.close()  # Fecha o socket
        return (False, None)  # Retorna erro


# Função para desconectar ao controlador por Ethernet
# sock: socket de comunicação com o controlador
def disconnectETController(sock):
    if (sock):  # Se o socket estiver aberto, fecha o socket
        sock.close()  # Fecha o socket
        sock = None
    else:  # Se o socket já estiver fechado, não faz nada
        sock = None


# Função para enviar, receber e processar mensagens do controlador
# sock: socket de comunicação com o controlador
# cmd: comando a ser enviado: nome da função a ser chamada no controlador
# params: parâmetros a serem enviados para a função
# id: id da mensagem
# socket: socket de comunicação com o controlador
# ret: reposta do controlador
# jdata: mensagem recebida do controlador
def sendCMD(sock, cmd, debug="n", params=None, id=1) -> object:
    if not params:  # Se não houver parâmetros, envia uma string vazia
        params = []  # Cria uma lista vazia
    else:  # Se houver parâmetros, converte para string
        params = json.dumps(params)  # Converte os parâmetros para string
    sendStr = ("{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format
               (cmd, params, id) + "\n")  # Cria a mensagem a ser enviada
    try:  # Tenta enviar a mensagem
        sock.sendall(bytes(sendStr, "utf-8"))  # Envia a mensagem
        ret = sock.recv(1024)  # Recebe a resposta
        jdata = json.loads(str(ret, "utf-8"))  # Converte a resposta para json
        if debug == "s":
            print("Ethernet - sendStr:", sendStr)  # Imprime a mensagem enviada no terminal para debug
            # print("Ethernet - ret:", ret)  # Imprime a mensagem recebida no terminal para debug
            # print(jdata)  # Imprime a mensagem recebida no terminal para debug
        if "result" in jdata.keys():  # Se houver resultado, retorna o resultado
            if debug == "s":
                print("Ethernet - jdata:", jdata["result"], jdata["id"])  # Imprime o resultado no terminal para debug
            return True, json.loads(jdata["result"]), jdata["id"]  # Retorna o resultado
        elif "error" in jdata.keys():  # Se houver erro, retorna o erro
            if debug == "s":
                print("Ethernet - jdata:", jdata['error']['message'])  # Imprime a mensagem de erro
                continuar = input("Ocorreu um erro. Pretende limpar o erro e continuar o programa? (s/n) -")
                if continuar != "s":
                    sys.exit()
                cmd = "clearAlarm"
                params = None
                id = 1
                sendStr = ("{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format
                           (cmd, params, id) + "\n")  # Cria a mensagem a ser enviada
                sock.sendall(bytes(sendStr, "utf-8"))  # Envia a mensagem
                ret = sock.recv(1024)
                jdata = json.loads(str(ret, "utf-8"))
                if not jdata["result"]:
                    print("Erro ao limpar alarme. Programa parou.")
                    sys.exit()
                print("Alarme limpo")
            return False, json.loads(jdata["error"]), jdata["id"]  # Retorna o erro
        else:  # Se não houver resultado nem erro, retorna a mensagem recebida
            return False, None, None  # Retorna a mensagem recebida
    except Exception as e:  # Se houver erro na comunicação, retorna o erro
        return False, None, None  # Retorna o erro


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
