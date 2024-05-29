# PSA 2024
# Authors: G2

import elite_json as ejson
import time
import keyboard
import serial
import threading

data = ""

# Thread 1
def Task1(read):

    global data

    print("Inside Thread 1")
    time.sleep(2)
    
    while 1:
        if read.in_waiting > 0:
            data = read.readline().decode('utf-8').rstrip()
            data = data.split(',')
            #print(data)
# Calculate positions based on increments
def calculate_position(position: list):
    
    new_position_x = position[0] - 0
    new_position_y = position[1] + 0
    new_position_z = position[2]   
    new_angle_x = position[3] + 6 * float(data[0])
    new_angle_y = position[4] + 6 * float(data[1])
    new_angle_z = position[5] + 6 * float(data[2])

    return new_position_x, new_position_y, new_position_z, new_angle_x, new_angle_y, new_angle_z

# Set robot communication
ROBOT_IP = "192.168.2.66"
conSuc, sock = ejson.connectETController(ROBOT_IP)

# Defines the reset position
Preset = [90, -90, 90, -180, 90, 180]

if conSuc:

    print("Connected")

    # Define the serial port and baud rate
    port = 'COM3'  # Replace with correct serial port
    baud_rate = 115200  # Replace with correct baud rate
    # Create a serial object
    read = serial.Serial(port, baud_rate)
    read.flushInput()  # Deletes any data from buffer
    t1 = threading.Thread(target = Task1, args=[read])
    print("Starting Thread 1")
    t1.start()

    # Get the servo status of the robotic arm
    suc, result, id = ejson.sendCMD(sock,"getServoStatus")

    if ( result == 0):
        suc, result , id = ejson.sendCMD(sock,"set_servo_status",{"status":1})
    
    # Get the coordinate system info
    suc, result , id = ejson.sendCMD(sock,"setCurrentCoord",{"coord_mode":2})

    start = input("Press s to start: ")
    while start.lower() != "s":                        # .lower to compare to both lower and uppercase characters 
        print("You´ve pressed the wrong key!")
        start = input("Press s to start: ")
    
    # Start main loop
    while True:

        suc, velo , id = ejson.sendCMD(sock, "setSpeed", {"value": 50})
        suc , result , id = ejson.sendCMD(sock , "get_transparent_transmission_state")

        if(result == 1):
            # Clear the transparent transmission cache
            suc , result , id = ejson.sendCMD(sock ,"tt_clear_servo_joint_buf")
            time.sleep (0.5)

        order = input("Press r to reset or i to initialize: ")
        while order.lower() not in ['r', 'i']:         # .lower to compare to both lower and uppercase characters
            print("You´ve pressed the wrong key!")
            order = input("Press r to reset or i to initialize: ")
            
        if order == "r":
            suc, speed , id = ejson.sendCMD(sock, "setSpeed", {"value": 100})
            suc, position, id = ejson.sendCMD(sock, "moveByJoint", {"targetPos": Preset, "speed": 75})

        else:
            # Get the current position information of the robot
            suc, v_origin, id = ejson.sendCMD(sock, "getRobotPose")
            x_now = v_origin[0]
            y_now = v_origin[1]
            z_now = v_origin[2]
            rx_now = v_origin[3]
            ry_now = v_origin[4]
            rz_now = v_origin[5]
            pose_now = []
            
            suc, result, id = ejson.sendCMD(sock, "transparent_transmission_init",{"lookahead": 400, "t": 10, "smoothness": 0.1, "response_enable":1})

            while True:
                x_now, y_now, z_now, rx_now, ry_now, rz_now = calculate_position(position=[x_now, y_now,z_now, rx_now, ry_now, rz_now])
                pose_now = [x_now, y_now,z_now, rx_now, ry_now, rz_now]
                #pose_now = calculate_position(position=[x_now, y_now,z_now, rx_now, ry_now, rz_now])
                vetor_formatado = ["{:.4f}".format(i) for i in pose_now]
                print(vetor_formatado)

                suc, p_target, id = ejson.sendCMD(sock, "inverseKinematic",{"targetPose": pose_now})

                suc, result, id = ejson.sendCMD(sock, "tt_put_servo_joint_to_buf", {"targetPos": p_target})

                suc, coord, id = ejson.sendCMD(sock,"getCurrentCoord")
                #print (coord)

                time.sleep(0.05)

                if keyboard.is_pressed('q'):  # if 'q' is pressed
                    print("The robot stopped ´cause you pressed 'q'!")
                    suc, result, id, = ejson.sendCMD(sock, "stop")
                    time.sleep(1)
                    break 
    else:
        print("Not connected")        