# Importação das bibliotecas necessárias
import keyboard  # Biblioteca para manipulação de teclado
import moduloEthernet as ether  # Biblioteca para comunicação Ethernet
import moduloSerie as serie  # Biblioteca para comunicação serial
import numpy  # Biblioteca para cálculos matemáticos
import time  # Biblioteca para manipulação de tempo

# Conexões
# Conectar ao ESP32 por porta serial ou wifi
sow = input("Conectar ao ESP32 por porta serial ou por wifi? (s/w) - ")
match sow:
    case "s":
        portName = input("Porta COM (Ex:COM2) - ")  # Porta COM do ESP32 (colocar COM2)
        serie.connect_serial_port(portName)  # Conectar à porta serial
    case "w":
        print("")  # Conectar ao ESP32 por wifi !!!!!!!!!!!! Continuar
# Conectar ao controlador por Ethernet
ip = input("Endereço IP do controlador (mudar para o IP do controlador) - ")  # IP do controlador (colocar 192.168.2.66)
# ip = "192.168.2.66"
conSuc, sock = ether.connectETController(ip)  # Conectar ao controlador

speed = int(input("Velocidade do robô (0-100%) - "))  # Velocidade do robô
if speed > 100:  # Se a velocidade for maior que 100%, define a velocidade como 100%
    speed = 100
elif speed < 0:  # Se a velocidade for menor que 0%, define a velocidade como 0%
    speed = 0

# Debug
debug = input("Debug? (s/n) - ")


# Calcula a posição do flange após a atualização da entrada do sensor
# position: lista com as posições atuais
# angle: lista com os ângulos atuais
def calculate_position(position: list, angle: list):
    # Ler os dados do sensor
    data = serie.read_serial_data(debug)
    ax = data[0]
    ay = data[1]
    az = data[2]
    gx = data[3]
    gy = data[4]
    gz = data[5]
    # Calcular a nova posição
    new_position_x = position[0] + ax
    new_position_y = position[1] + ay
    new_position_z = position[2] + az
    # Segurança para não sair do espaço de trabalho (posições)
    # Segurança em X
    if new_position_x <= 0:
        new_position_x = 0
    if new_position_x >= 750:
        new_position_x = 750
    # Segurança em Y
    if new_position_y <= -500:
        new_position_y = -500
    if new_position_y >= 500:
        new_position_y = 500
    # Segurança em Z
    if new_position_z <= 50:
        new_position_z = 50
    if new_position_z >= 750:
        new_position_z = 750
    # Calcular o novo ângulo
    new_angle_x = angle[0] + gx
    new_angle_y = angle[1] + gy
    new_angle_z = angle[2] + gz
    # Segurança para não sair do espaço de trabalho (ângulos)
    # Segurança em Y
    if new_angle_y <= 0:
        new_angle_y = 0
    if new_angle_y >= numpy.pi / 2:
        new_angle_y = numpy.pi / 2
    # Segurança em Z
    if new_angle_z <= -numpy.pi / 2:
        new_angle_z = -numpy.pi / 2
    if new_angle_z >= numpy.pi / 2:
        new_angle_z = numpy.pi / 2
    # Output
    if debug == "s":
        print("Principal - data:", data)
        print("Principal - nova posição: (", new_position_x, ", ", new_position_y, ", ", new_position_z, ", ",
              new_angle_x,
              ", ", new_angle_y, ", ", new_angle_z, ")")
    return new_position_x, new_position_y, new_position_z, new_angle_x, new_angle_y, new_angle_z


if conSuc:  # Se a conexão for bem sucedida
    stop = False
    _continue = "s"
    initialpoint = ([0, 100, 100, 0, 0, 0])  # posição inicial do robot!!!!!!!!!!!!!VERIFICAR!!!!!!!!!!!!!!!!!!!!!
    inicialpos = input("Prentende resetar a posição do robot? (s/n) - ")
    # Começa o main "loop"
    while True:
        if stop:
            _continue = input("Para continuar insira 's' caso contrário o programa para - ")
            inicialpos = input("Prentende resetar a posição do robot? (s/n) - ")
            if _continue != "s":
                break
            stop = False
        if _continue == "s":
            time.sleep(0.01)
            # obtain robot's original position and joint angle
            suc, v_origin, id = ether.sendCMD(sock, "get_tcp_pose", debug)  # Get robot's current pose (!!!tool!!!)
            x_now = v_origin[0]
            y_now = v_origin[1]
            z_now = v_origin[2]
            rx_now = v_origin[3]
            ry_now = v_origin[4]
            rz_now = v_origin[5]
            pose_now = []
            if debug == "s":
                print("Principal - v_origin:", v_origin)
            # transparent transmission init
            suc, result, id = ether.sendCMD(sock, "transparent_transmission_init", debug,
                                            {"lookahead": 200, "t": 20, "smoothness": 0.1})
            suc, result, id = ether.sendCMD(sock, "setSpeed", debug, {"value": speed})  # Set robot's speed

            if inicialpos == "s":
                suc, result, id = ether.sendCMD(sock, "moveByJoint", debug, {"targetPos": initialpoint,
                                                                             "speed": speed, "acc": 10,
                                                                             "dec": 10})  # Move robot to initialpos
            # CALIBRAR ACELERAÇÂO E DESACELERAÇÂO !!!!!!!!!!!!!!!!!!!!!!!!!!!!
            while True:
                if debug == "s":
                    print("Para parar insira 'q'")
                if keyboard.is_pressed("q"):
                    suc, result, id = ether.sendCMD(sock, "stop")
                    suc, result, id = ether.sendCMD(sock, "tt_clear_servo_joint_buf", debug, {"clear": 0})
                    stop = True
                    break
                # get new position and angle based on sensor key value and add it to tt buff
                x_now, y_now, z_now, rx_now, ry_now, rz_now = calculate_position([x_now, y_now, z_now],
                                                                                 [rx_now, ry_now, rz_now])
                pose_now = [x_now, y_now, z_now, rx_now, ry_now, rz_now]
                if debug == "s":
                    print("Principal - pose_now:", pose_now)
                suc, p_target, id = ether.sendCMD(sock, "inverseKinematic", debug, {"targetPose": pose_now})
                suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", debug, {"targetPos": p_target})
                time.sleep(0.02)
        suc, result, id = ether.sendCMD(sock, "stop")
        time.sleep(0.01)
ether.disconnectETController(sock)
serie.close_serial_port()
