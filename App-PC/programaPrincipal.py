# Importação das bibliotecas necessárias
import moduloEthernet as ether
import numpy
import time


# Calcula a posição do flange após a atualização da entrada do sensor (valor de entrada usado como aceleração)
def calculate_position_a(ax, ay, az, t, speed: list, position: list):  # buscar velocidades sensor e usar acelerações ou
    # usar velocidades apenas
    new_speed_x = speed[0] + 300 * ax * t  # usar "-" ou "+" para inverter o sentido da aceleração
    new_speed_y = speed[1] + 300 * ay * t
    new_speed_z = speed[2] + 300 * az * t
    new_position_x = position[0] + new_speed_x * t
    new_position_y = position[1] + new_speed_y * t
    new_position_z = position[2] + new_speed_z * t
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
    return new_position_x, new_position_y, new_position_z, speed_x, speed_y, speed_z


# calculate flange position after joystick input updated (input value used as speed)
# gx: velocidade angular em x
# gy: velocidade angular em y
# gz: velocidade angular em z
# t: tempo
# angle: lista com os ângulos atuais
def calculate_position_g(gx, gy, gz, t, angle: list):
    new_angle_x = angle[0] + gx * t
    new_angle_y = angle[1] + gy * t
    new_angle_z = angle[2] + gz * t
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
ip = "192.168.2.66"
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
                x_now, y_now, z_now, speed_x, speed_y, speed_z = calculate_position_a(ax, ay, az, 0.05,
                                                                                      [speed_x, speed_y, speed_z],
                                                                                      [x_now, y_now, z_now])
                # get new angle based on joystick key value and add it to tt buff
                rx_now, ry_now, rz_now = calculate_position_g(gx, gy, gz, 0.05, [rx_now, ry_now, rz_now])
                pose_now = [x_now, y_now, z_now, rx_now, ry_now, rz_now]
                suc, p_target, id = ether.sendCMD(sock, "inverseKinematic",
                                                  {"targetPose": pose_now})
                suc, result, id = ether.sendCMD(sock, "tt_put_servo_joint_to_buf", {"targetPos": p_target})
                time.sleep(0.02)
        suc, result, id = ether.sendCMD(sock, "stop")
        time.sleep(0.01)

ether.disconnectETController(sock)
