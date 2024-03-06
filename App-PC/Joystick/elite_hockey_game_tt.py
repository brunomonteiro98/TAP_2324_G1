from hockey_joystick import *
import elite_json as ejson
import time


# calculate flange position after joystick input updated (input value used as acceleration)
def calculate_position(key_x, key_y, t, speed: list, position: list):
    new_speed_x = speed[0] + 300*key_x*t
    new_speed_y = speed[1] - 300*key_y*t
    new_position_x = position[0] + new_speed_x*t
    new_position_y = position[1] + new_speed_y*t
    return new_speed_x, new_speed_y, new_position_x, new_position_y


# calculate flange position after joystick input updated (input value used as speed)
def calculate_position2(key_x, key_y, t, position: list):
    new_position_x = position[0] + key_x*t*300
    new_position_y = position[1] - key_y*t*300
    if new_position_y <= -500:
        new_position_y = -500
    if new_position_y >= 500:
        new_position_y = 500
    return new_position_x, new_position_y


ip = "192.168.1.200"
conSuc, sock = ejson.connectETController(ip)

if conSuc:
    # set up joystick
    num_of_joysticks = joystick_init()
    joystick1 = Joystick(0)
    # start the game's main loop
    while True:
        axis_x, axis_y, buttonA, buttonB, leftStart, rightStart = joystick1.get_buttons()
        # game starts if button LB is pressed
        if leftStart:
            time.sleep(0.01)
            # obtain robot's original position and joint angle
            suc, v_origin, id = ejson.sendCMD(sock, "getRobotPose")
            suc, p_origin, id = ejson.sendCMD(sock, "getRobotPos")
            x_now = v_origin[0]
            y_now = v_origin[1]
            speed_x = 0
            speed_y = 0
            pose_now = []

            # transparent transmission init
            suc, result, id = ejson.sendCMD(sock, "transparent_transmission_init",
                                      {"lookahead": 200, "t": 20, "smoothness": 0.1})
            while True:
                # get joystick key values
                axis_x, axis_y, buttonA, buttonB, leftExit, rightExit = joystick1.get_buttons()
                # stops the game if button RB is pressed
                if rightExit:
                    suc, result, id = ejson.sendCMD(sock, "stop")
                    suc, result, id = ejson.sendCMD(sock, "tt_clear_servo_joint_buf", {"clear": 0})
                    break
                # get new position based on joystick key value and add it to tt buff
                x_now, y_now = calculate_position2(axis_x, axis_y, 0.05, [x_now, y_now])
                pose_now = [x_now, y_now, v_origin[2], v_origin[3], v_origin[4], v_origin[5]]
                suc, p_target, id = ejson.sendCMD(sock, "inverseKinematic",
                                                {"targetPose": pose_now})
                suc, result, id = ejson.sendCMD(sock, "tt_put_servo_joint_to_buf", {"targetPos": p_target})
                time.sleep(0.02)
        suc, result, id = ejson.sendCMD(sock, "stop")
        time.sleep(0.01)

ejson.disconnectETController(sock)
