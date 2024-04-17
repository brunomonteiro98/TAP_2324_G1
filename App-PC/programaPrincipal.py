# Importação das bibliotecas necessárias
import keyboard  # Biblioteca para manipulação de teclado
import threading  # Biblioteca para manipulação de threads
import moduloEthernet as ether  # Biblioteca para comunicação Ethernet
import moduloSerie as serie  # Biblioteca para comunicação serial
import moduloGravação as gravacao  # Biblioteca para gravação de dados
import moduloPlay as play  # Biblioteca para play dos dados
from moduloWifi import WiFiCommunicator  # Biblioteca para comunicação wifi

# ==================================================================================================================== #

# Conexões
# Conectar ao ESP32 por porta serial ou wifi
# ‘Input’ com respetiva segurança
while True:
    sow = input("Conectar ao ESP32 por porta serial ou por wifi? (s/w) - ")
    if sow == "s" or sow == "w":
        break
    else:
        print("Insira s ou w, idiota!")
match sow:
    case "s":
        portName = input("Porta COM (Ex:COM2) - ")  # Porta COM do ESP32 (colocar COM2)
        serie.connect_serial_port(portName)  # Conectar à porta serial
    case "w":
        communicator = WiFiCommunicator(max_buffer_sz=128)  # Criar o comunicador WiFi (máximo de 128 bytes)
# Conectar ao controlador por Ethernet
#ip = input("Endereço IP do controlador (mudar para o IP do controlador) - ")  # IP do controlador (colocar 192.168.2.66)
ip = "192.168.2.66"
conSuc, sock = ether.connectETController(ip)  # Conectar ao controlador

# ==================================================================================================================== #

# Velocidade do robô (0-100%)
speed = int(input("Velocidade do robô (0.05-100%) - "))  # Velocidade do robô
if speed > 100:  # Se a velocidade for maior que 100%, define a velocidade como 100%
    speed = 100  # Velocidade do robô
elif speed < 0.05:  # Se a velocidade for menor que 0%, define a velocidade como 0%
    speed = 0.05  # Velocidade do robô

# ==================================================================================================================== #

# Debug
# ‘Input’ com respetiva segurança
global debug
while True:
    debug = input("Debug? (s/n) - ")
    if debug == "s" or debug == "n":
        break
    else:
        print("Insira s ou n, idiota!")

# ==================================================================================================================== #

# Criar a thread para ler os dados do sensor
global data
data = [0, 0, 0, 0, 0, 0]  # Inicializar a lista de dados


# Define a função da thread
def task(debug):
    global data
    print("Thread iniciada")
    while True:
        if sow == "s":  # Se a conexão for por porta serial
            data = serie.read_serial_data(debug)  # Ler os dados do sensor
        elif sow == "w":  # Se a conexão for por wifi
            data = communicator.read_wifi_data(debug)  # Ler os dados do sensor


# Criar a thread e iniciar
t = threading.Thread(target=task, args=debug)  # Criar a thread para ler os dados do sensor
t.start()  # Iniciar a thread


# ==================================================================================================================== #


# Calcula a posição do flange após a atualização da entrada do sensor
# position: lista com as posições atuais
# angle: lista com os ângulos atuais
def calculate_position(position: list, angle: list):
    # Ler os dados do sensor
    global data
    if data is None:  # Se não houver dados, retorna 0's
        ax = 0
        ay = 0
        az = 0
        gx = 0
        gy = 0
        gz = 0
    else:  # Se houver dados
        ax = data[0]
        ay = data[1]
        az = data[2]
        gx = data[3]
        gy = data[4]
        gz = data[5]

    # Calcular a nova posição (verificar + ou - conforme o sensor)
    new_position_x = position[0] + ax
    new_position_y = position[1] - az  # Y do robot é o Z do sensor. Tbm está invertido (cresce para baixo)
    new_position_z = position[2] + ay  # Z do robot é o Y do sensor

    # Segurança para não sair do espaço de trabalho (posições)
    # Segurança em X
    '''if new_position_x <= ---:
        new_position_x = ---
    if new_position_x >= ---:
        new_position_x = ---
    # Segurança em Y
    if new_position_y <= ---:
        new_position_y = ---
    if new_position_y >= ---:
        new_position_y = ---
    # Segurança em Z
    if new_position_z <= ---:
        new_position_z = ---
    if new_position_z >= ---:
        new_position_z = ---'''

    # Calcular o novo ângulo
    new_angle_x = angle[0] + gx
    new_angle_y = angle[1] + gy
    new_angle_z = angle[2] + gz

    # Segurança para não sair do espaço de trabalho (ângulos)
    # Segurança em Y
    '''if new_angle_y <= ---:
        new_angle_y = ---
    if new_angle_y >= ---:
        new_angle_y = ---
    # Segurança em Z
    if new_angle_z <= ---:
        new_angle_z = ---
    if new_angle_z >= ---:
        new_angle_z = --- '''

    # Debug
    if debug == "s":
        print("Principal - position, angle:", position, angle)
        print("Principal - data:", data)

    # Output
    return new_position_x, new_position_y, new_position_z, new_angle_x, new_angle_y, new_angle_z


# ==================================================================================================================== #

if conSuc:  # Se a conexão for bem sucedida

    # Definição de variáveis
    g = 0  # Variável para identificar se a gravação corre
    p = 0  # Variável para identificar se o play corre
    i = 0  # Variável para identificar a linha do ficheiro
    fichlen = 0  # Variável para identificar o número de linhas do ficheiro
    stop = False  # Variável para identificar se o programa deve parar
    continua = True  # Variável para identificar se o programa deve continuar
    firstrun = True  # Variável para identificar se é a primeira vez que o programa corre
    firstrung = True  # Variável para identificar se é a primeira vez que o modulo gravação corre
    initialpoint = ([90, -100, 110, -190, 85, 0])  # posição inicial do robô (em joint angles)
    # ‘Input’ com respetiva segurança
    while True:
        inicialpos = input("Prentende resetar a posição do robot? (s/n) - ")
        if inicialpos == "s" or inicialpos == "n":
            break
        else:
            print("Insira s ou n, idiota!")

    # Começa o main "loop"
    while True:

        # Pergunta se o utilizador quer continuar após parar (não é necessário na primeira vez)
        if stop:
            # ‘Input’ com respetiva segurança
            while True:
                continua = input("Pretende continuar (s/n)? - ")
                if continua == "s" or continua == "n":
                    break
                else:
                    print("Insira s ou n, idiota!")
            if continua == "s":
                firstrun = True
                stop = False
            else:
                break
            # ‘Input’ com respetiva segurança
            while True:
                inicialpos = input("Prentende resetar a posição do robot? (s/n) - ")
                if inicialpos == "s" or inicialpos == "n":
                    break
                else:
                    print("Insira s ou n, idiota!")

        # Move robot to initialpos if requested
        if inicialpos == "s":
            suc, result, id = ether.sendCMD(sock, "moveByJoint", debug, {"targetPos": initialpoint,
                                                                         "speed": speed, "acc": 10, "dec": 10})
            # Try again after cleaning alarm
            if not suc:
                suc, result, id = ether.sendCMD(sock, "moveByJoint", debug, {"targetPos": initialpoint,
                                                                             "speed": speed, "acc": 10,
                                                                             "dec": 10})
            while True:
                suc, result, id = ether.sendCMD(sock, "getRobotState")
                # Try again after cleaning alarm
                if not suc:
                    suc, result, id = ether.sendCMD(sock, "getRobotState")
                if result == 0:
                    break
            inicialpos = "n"

        # Sets the coordinate system
        suc, result, id = ether.sendCMD(sock, "setCurrentCoord", debug, {"coord_mode": 2})
        if not suc:
            suc, result, id = ether.sendCMD(sock, "setCurrentCoord", debug, {"coord_mode": 2})

        # Obtain robot's original position and joint angle
        suc, v_origin, id = ether.sendCMD(sock, "get_tcp_pose", debug, {"unit_type": 0})  # Get robot's
        # current pose (!!!tool!!!). Rotations in degrees.
        if not suc:
            suc, v_origin, id = ether.sendCMD(sock, "get_tcp_pose", debug, {"unit_type": 0})
        x_now = v_origin[0]
        y_now = v_origin[1]
        z_now = v_origin[2]
        rx_now = v_origin[3]
        ry_now = v_origin[4]
        rz_now = v_origin[5]
        pose_now = []
        # Debug
        if debug == "s":
            print("Principal - v_origin:", v_origin)

        # Initialize transparent transmission
        suc, result, id = ether.sendCMD(sock, "get_transparent_transmission_state")
        # Try again after cleaning alarm
        if not suc:
            suc, result, id = ether.sendCMD(sock, "get_transparent_transmission_state")
        if result == 0:
            suc, result, id = ether.sendCMD(sock, "transparent_transmission_init",
                                            debug, {"lookahead": 200, "t": 2, "smoothness": 1, "response_enable": 1})
            # Try again after cleaning alarm
            if not suc:
                suc, result, id = ether.sendCMD(sock, "transparent_transmission_init",
                                                debug,
                                                {"lookahead": 200, "t": 2, "smoothness": 1, "response_enable": 1})
        # Set robot's speed
        suc, result, id = ether.sendCMD(sock, "setSpeed", debug, {"value": speed})
        # Try again after cleaning alarm
        if not suc:
            suc, result, id = ether.sendCMD(sock, "setSpeed", debug, {"value": speed})

        while True:
            # Print instructions if it is the first run
            if firstrun:
                print("Para parar insira 'q'")
                print("Para gravar insira 'g'")
                print("Para play insira 'p'")
                firstrun = False

            # Stop the robot if 'q' is pressed
            if keyboard.is_pressed("q"):
                suc, result, id = ether.sendCMD(sock, "stop")
                # Try again after cleaning alarm
                if not suc:
                    suc, result, id = ether.sendCMD(sock, "stop")
                suc, result, id = ether.sendCMD(sock, "tt_clear_servo_joint_buf", debug, {"clear": 0})
                # Try again after cleaning alarm
                if not suc:
                    suc, result, id = ether.sendCMD(sock, "tt_clear_servo_joint_buf", debug, {"clear": 0})
                stop = True
                break

            # Start recording if 'g' is pressed
            if keyboard.is_pressed("g"):
                print("Gravação iniciada")
                g = 1

            # Record the sensor data
            if g == 1:
                firstrung = gravacao.record(pose_now, firstrung, debug)

            # Stop recording if 'h' is pressed
            if keyboard.is_pressed("h"):
                print("Gravação terminada")
                g = 0

            # Start playing if 'p' is pressed
            if keyboard.is_pressed("p"):
                print("Play iniciado")
                p = 1

            # Stop recording if '+' is pressed
            if keyboard.is_pressed("+"):
                print("Play terminado")
                p = 0
                i = 6

            # If the program is not stopped, recording or playing, get new position and angle based on sensor key value
            if p != 1:
                # Get new position and angle based on sensor key value and add it to tt buff
                x_now, y_now, z_now, rx_now, ry_now, rz_now = calculate_position([x_now, y_now, z_now],
                                                                                 [rx_now, ry_now, rz_now])
                pose_now = [x_now, y_now, z_now, rx_now, ry_now, rz_now]
                if debug == "s":
                    print("Principal - pose_now:", pose_now)

            # Play the recorded data
            if p == 1:
                pose_now, fichlen = play.play(i, debug)
                '''if i == 0: # Send the robot to the first position
                    pose_now, fichlen = play.play(i, debug)
                    suc, result, id = ether.sendCMD(sock, "moveByJoint", debug, {"targetPos": pose_now,
                                                                                 "speed": speed, "acc": 10,
                                                                                 "dec": 10})
                    # Try again after cleaning alarm
                    if not suc:
                        suc, result, id = ether.sendCMD(sock, "moveByJoint", debug, {"targetPos": pose_now,
                                                                                     "speed": speed, "acc": 10,
                                                                                     "dec": 10})
                    while True:
                        suc, result, id = ether.sendCMD(sock, "getRobotState")
                        # Try again after cleaning alarm
                        if not suc:
                            suc, result, id = ether.sendCMD(sock, "getRobotState")
                        if result == 0:
                            break
                    i += 1'''
                # !!! (colocar 0 < qd descomentar) !!!
                if i < fichlen - 1:  # fichlen-1 because it starts at 0 so the last one is fichlen-1
                    pose_now, fichlen = play.play(i, debug)
                    i += 1
                if i == fichlen - 1:  # fichlen-1 because it starts at 0 so the last one is fichlen-1
                    pose_now, fichlen = play.play(i, debug)
                    i = 0
                # Pause the play if 'space' is pressed
                if keyboard.is_pressed("space"):
                    pause = True
                    print("Play pausado para continuar insira 'space' novamente")
                    while pause:
                        if keyboard.is_pressed("space"):
                            pause = False
                            print("Play continuado")

            # Inverse kinematics and send to buffer
            suc, p_target, id = ether.sendCMD(sock, "inverseKinematic", debug, {"targetPose": pose_now, "unit_type": 0})
            # Try again after cleaning alarm
            if not suc:
                suc, p_target, id = ether.sendCMD(sock, "inverseKinematic", debug,
                                                  {"targetPose": pose_now, "unit_type": 0})
            suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", debug, {"targetPos": p_target})
            # Try again after cleaning alarm
            if not suc:
                suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", debug, {"targetPos": p_target})

            # Debug
            if debug == "s":
                print("Principal - p_target:", p_target)
                print("Principal - result:", result)

        # Stop the robot
        suc, result, id = ether.sendCMD(sock, "stop")
        # Try again after cleaning alarm
        if not suc:
            suc, result, id = ether.sendCMD(sock, "stop")

# Desconectar o controlador, a porta serial e o comunicador wifi
ether.disconnectETController(sock)
match sow:
    case "s":
        serie.close_serial_port()
    case "w":
        communicator.destroy()
print("Programa terminado")
