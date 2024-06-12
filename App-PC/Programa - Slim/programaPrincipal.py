# Importação das bibliotecas necessárias
import time  # Biblioteca para manipulação de tempo
import keyboard  # Biblioteca para manipulação de teclado
import threading  # Biblioteca para manipulação de threads
import numpy as np  # Biblioteca para manipulação de arrays
import moduloSerie as serie  # Biblioteca para comunicação serial
import moduloEthernet as ether  # Biblioteca para comunicação Ethernet
import moduloGravaçãoJBI as gravacaoJBI  # Biblioteca para gravação de dados

# ==================================================================================================================== #

# Conexões
# Conectar ao ESP32 por porta serial
portName = "COM3"
#portName = input("Porta COM (Ex:COM3) - ")  # Porta COM do ESP32
serie.connect_serial_port(portName)  # Conectar à porta serial

# Conectar ao controlador por Ethernet
ip = "192.168.2.66"
#ip = input("Endereço IP do controlador (mudar para o IP do controlador) - ")  # IP do controlador
conSuc, sock = ether.connectETController(ip)  # Conectar ao controlador

# ==================================================================================================================== #

# Velocidade do robô (0-100%)
speed = int(input("Velocidade do robô (0.05-100%) - "))  # Velocidade do robô

# ==================================================================================================================== #

# Debug
global debug
debug = input("Debug? (s/n) - ")

# ==================================================================================================================== #


# Definição das funções das threads
def task():
    global data
    while True:
        data = serie.read_serial_data(debug)  # Ler os dados do sensor
        time.sleep(0.01)

# Criar a thread e iniciar
t = threading.Thread(target=task, daemon=True)  # Criar a thread para ler os dados do sensor
t.start()  # Iniciar a thread

# ==================================================================================================================== #

if conSuc:  # Se a conexão for bem sucedida

    # Definição de variáveis
    g = 0  # Variável para identificar se a gravação corre
    stop = False  # Variável para identificar se o programa deve parar
    continua = True  # Variável para identificar se o programa deve continuar
    firstrun = True  # Variável para identificar se é a primeira vez que o programa corre
    initialpos = "n"  # Variável para identificar se o robô deve ir para a posição inicial
    firstrungJBI = True  # Variável para identificar se é a primeira vez que o modulo gravação corre
    lastrungJBI = False  # Variável para identificar se é a última vez que o modulo gravação corre
    initialpoint = [90, -100, 110, -190, 85, 0]  # posição inicial do robô (em joint angles)

    # Set robot's speed
    suc, result, id = ether.sendCMD(sock, "setSpeed", debug, {"value": speed})

    # Obter a posição atual do robô
    suc, v_origin, id = ether.sendCMD(sock, "get_joint_pos", debug,
                                      {"unit_type": 0})  # Get robot's current pos (!!!joint!!!). Rotations in degrees.
    v_origin = list(np.round(v_origin))
    if v_origin != initialpoint:  # Se a posição inicial for diferente da posição atual
        initialpos = input("Pretende resetar a posição do robot? (s/n) - ")

    # Começa o main "loop"
    while True:
        # Pergunta se o utilizador quer continuar após parar (não é necessário na primeira vez)
        if stop:
            continua = input("Pretende continuar (s/n)? - ")
            if continua == "s":
                firstrun = True
                stop = False
            else:
                break

            # Obter a posição atual do robô
            suc, v_origin, id = ether.sendCMD(sock, "get_joint_pos", debug, {
                "unit_type": 0})  # Get robot's current pos (!!!joint!!!). Rotations in degrees.
            v_origin = list(np.round(v_origin))
            if v_origin != initialpoint:  # Se a posição inicial for diferente da posição atual
                initialpos = input("Prentende resetar a posição do robot? (s/n) - ")

        # Move robot to initialpos if requested
        if initialpos == "s":
            suc, result, id = ether.sendCMD(sock, "moveByJoint", debug,
                                            {"targetPos": initialpoint, "speed": speed, "acc": 75, "dec": 75})
            while True:
                suc, result, id = ether.sendCMD(sock, "getRobotState")
                if result == 0:
                    break
            initialpos = "n"

        # Sets the coordinate system
        suc, result, id = ether.sendCMD(sock, "setCurrentCoord", debug, {"coord_mode": 2})

        # Obtain robot's original position and joint angle
        suc, v_origin, id = ether.sendCMD(sock, "get_tcp_pose", debug, {
            "unit_type": 0})  # Get robot's current pose (!!!tool!!!). Rotations in degrees.
        v_origin = np.array(v_origin)

        # Debug
        if debug == "s":
            print("Principal - v_origin:", v_origin)

        # Initialize transparent transmission
        suc, result, id = ether.sendCMD(sock, "get_transparent_transmission_state")

        if result == 0:
            suc, result, id = ether.sendCMD(sock, "transparent_transmission_init", debug,
                                            {"lookahead": 200, "t": 2, "smoothness": 1, "response_enable": 1})

        while True:
            speedCP = [0, 0, 0]  # Velocidade para o cálculo da posição

            # Print instructions if it is the first run
            if firstrun:
                print("Para parar insira 'q'")
                print("Para gravar insira 'g'")
                firstrun = False

            # Stop the robot if 'q' is pressed
            if keyboard.is_pressed("q"):
                time.sleep(0.1)
                suc, result, id = ether.sendCMD(sock, "stop")
                suc, result, id = ether.sendCMD(sock, "tt_clear_servo_joint_buf", debug, {"clear": 0})
                stop = True
                break

            # Start recording if 'g' is pressed
            if keyboard.is_pressed("g"):
                time.sleep(0.1)
                gmode = input("Gravação em modo tempo ou pontos no modo JBI? (t/p) - ")
                print("Gravação iniciada")
                if gmode == "t":
                    print("O programa tirará pontos a cada 2 segundos. Para parar insira 'h'")
                elif gmode == "p":
                    print("O programa tirará pontos sempre que 'f' for premido. Para parar insira 'h'")
                    print("Atenção: 1º ponto não conta")
                g = 1
                starttime = time.time()

            # Record the sensor data
            if g == 1:
                if gmode == "t":
                    now = time.time()
                    elapsedtime = now - starttime  # Calculate elapsed time
                    if elapsedtime > 2:  # Record every 2 seconds
                        firstrungJBI, lastrungJBI, g = gravacaoJBI.record(p_target, firstrungJBI, lastrungJBI, g, speed,
                                                                          debug)
                        starttime = now  # Reset start time
                        print("Ponto gravado")
                elif gmode == "p":
                    if keyboard.is_pressed("f"):
                        time.sleep(0.1)
                        firstrungJBI, lastrungJBI, g = gravacaoJBI.record(p_target, firstrungJBI, lastrungJBI, g, speed,
                                                                          debug)
                        print("Ponto gravado")

            # Stop recording if 'h' is pressed
            if keyboard.is_pressed("h"):
                time.sleep(0.1)
                print("Gravação terminada")
                lastrungJBI = True
                firstrungJBI, lastrungJBI, g = gravacaoJBI.record(p_target, firstrungJBI, lastrungJBI, g, speed, debug)
                g = 0

            # Get new pose based on sensor key value and add it to tt buff
            global data
            if data is not None:
                v_origin += data
            pose_now = v_origin  # Convert the new position to a list

            if debug == "s":
                print("Principal - pose_now:", pose_now)

            # Inverse kinematics and send to buffer
            suc, p_target, id = ether.sendCMD(sock, "inverseKinematic", debug, {"targetPose": pose_now, "unit_type": 0})
            suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", debug, {"targetPos": p_target})

            # Debug
            if debug == "s":
                print("Principal - p_target:", p_target)
                print("Principal - result:", result)

        # Stop the robot
        suc, result, id = ether.sendCMD(sock, "stop")

        time.sleep(0.01)

# Desconectar o controlador e a porta serial
ether.disconnectETController(sock)
#serie.close_serial_port()
print("Programa terminado")
