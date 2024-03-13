# Importação das bibliotecas necessárias
import moduloEthernet as ether
import moduloSerie as serie
import numpy
import time

serie.connect_serial_port()

# resolver maneira de colocar a correr quando calculate_position_a e calculate_position_g forem chamadas
"""data = serie.read_serial_data()
ax = data[1]
ay = data[2]
az = data[3]
data = serie.read_serial_data()
gx = data[4]
gy = data[5]
gz = data[6]"""

"""
Tentar meter o input como o rato. Ver pygame mouse motion 1024.
Tentar passar a e g a uma única.
Falar com os gajos json de output.
Verificar diferença entre base e ponta. Se for necessário passar de base a ponta (mandar e receber). 
Incremento não deve fazer diferença
"""

# Calcula a posição do flange após a atualização da entrada do sensor
# ax: incremento de posição em x
# ay: incremento de posição em y
# az: incremento de posição em z
# t: tempo
# speed: lista com as velocidades atuais
# position: lista com as posições atuais
def calculate_position_a(ax, ay, az, position: list):  # buscar incrementos de posição x, y e z
    new_position_x = position[0] + ax
    new_position_y = position[1] + ay
    new_position_z = position[2] + az
    # Segurança para não sair do espaço de trabalho
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
    # Output
    return new_position_x, new_position_y, new_position_z


# calculate flange position after joystick input updated (input value used as speed)
# gx: incremento de posição angular em x
# gy: incremento de posicão angular em y
# gz: incremento de posicão angular em z
# t: tempo
# angle: lista com os ângulos atuais
def calculate_position_g(gx, gy, gz, angle: list):
    new_angle_x = angle[0] + gx
    new_angle_y = angle[1] + gy
    new_angle_z = angle[2] + gz
    # Segurança para não sair do espaço de trabalho
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
    return new_angle_x, new_angle_y, new_angle_z


# IP do controlador (mudar para o IP do controlador)
ip = input("Endereço IP do controlador (mudar para o IP do controlador) - ")  # 192.168.2.66
conSuc, sock = ether.connectETController(ip)  # Conectar ao controlador

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

            # transparent transmission init
            suc, result, id = ether.sendCMD(sock, "transparent_transmission_init",
                                            {"lookahead": 200, "t": 20, "smoothness": 0.1})
            while True:
                # Para se virar-mos o sensor ao contrário ou accelerámos mt rápido
                if False:
                    suc, result, id = ether.sendCMD(sock, "stop")
                    suc, result, id = ether.sendCMD(sock, "tt_clear_servo_joint_buf", {"clear": 0})  #
                    break
                # get new position based on sensor key value and add it to tt buff
                x_now, y_now, z_now = calculate_position_a(ax, ay, az, [x_now, y_now, z_now])
                # get new angle based on sensor key value and add it to tt buff
                rx_now, ry_now, rz_now = calculate_position_g(gx, gy, gz, [rx_now, ry_now, rz_now])
                pose_now = [x_now, y_now, z_now, rx_now, ry_now, rz_now]
                suc, p_target, id = ether.sendCMD(sock, "inverseKinematic",{"targetPose": pose_now})
                suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", {"targetPos": p_target})
                time.sleep(0.02)
        suc, result, id = ether.sendCMD(sock, "stop")
        time.sleep(0.01)

ether.disconnectETController(sock)
serie.close_serial_port()