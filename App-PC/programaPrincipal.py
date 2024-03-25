# Importação das bibliotecas necessárias
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
        print("") # Conectar ao ESP32 por wifi !!!!!!!!!!!! Continuar
# Conectar ao controlador por Ethernet
#ip = input("Endereço IP do controlador (mudar para o IP do controlador) - ")  # IP do controlador (colocar 192.168.2.66)
ip = "192.168.2.66"
conSuc, sock = ether.connectETController(ip)  # Conectar ao controlador

"""
Verificar diferença entre base e ponta. Se for necessário passar de base a ponta (mandar e receber). 
"""


# Calcula a posição do flange após a atualização da entrada do sensor
# position: lista com as posições atuais
# angle: lista com os ângulos atuais
def calculate_position(position: list, angle: list):
    # Ler os dados do sensor
    data = serie.read_serial_data()
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
    print("Principal - data:",data)
    print("Principal - nova posição: (", new_position_x, ", ", new_position_y, ", ", new_position_z, ", ", new_angle_x, ", "
          , new_angle_y, ", ", new_angle_z, ")")
    return new_position_x, new_position_y, new_position_z, new_angle_x, new_angle_y, new_angle_z


if conSuc:  # Se a conexão for bem sucedida
    # Começa o main "loop"
    while True:
        # Começa se algo
        if True:
            time.sleep(0.01)
            # obtain robot's original position and joint angle
            suc, v_origin, id = ether.sendCMD(sock, "getRobotPose")  # Get robot's current pose
            suc, p_origin, id = ether.sendCMD(sock, "getRobotPos")  # Get robot's current joint angle
            x_now = v_origin[0]
            y_now = v_origin[1]
            z_now = v_origin[2]
            rx_now = v_origin[3]
            ry_now = v_origin[4]
            rz_now = v_origin[5]
            speed_x = 0
            speed_y = 0
            speed_z = 0
            pose_now = []
            print("Principal - v_origin:",v_origin)
            print("Principal - p_origin:",p_origin)
            # transparent transmission init
            suc, result, id = ether.sendCMD(sock, "transparent_transmission_init",
                                            {"lookahead": 200, "t": 20, "smoothness": 0.1})
            while True:
                # Para se virar-mos o sensor ao contrário ou accelerámos mt rápido
                if False:
                    suc, result, id = ether.sendCMD(sock, "stop")
                    suc, result, id = ether.sendCMD(sock, "tt_clear_servo_joint_buf", {"clear": 0})  #
                    break
                # get new position and angle based on sensor key value and add it to tt buff
                x_now, y_now, z_now, rx_now, ry_now, rz_now = calculate_position([x_now, y_now, z_now],
                                                                                 [rx_now, ry_now, rz_now])
                pose_now = [x_now, y_now, z_now, rx_now, ry_now, rz_now]
                print("Principal - pose_now:",pose_now)
                suc, p_target, id = ether.sendCMD(sock, "inverseKinematic", {"targetPose": pose_now})
                suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", {"targetPos": p_target})
                time.sleep(0.02)
        suc, result, id = ether.sendCMD(sock, "stop")
        time.sleep(0.01)

ether.disconnectETController(sock)
serie.close_serial_port()
