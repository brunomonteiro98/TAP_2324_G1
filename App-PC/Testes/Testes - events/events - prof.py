# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import threading
import time
import sys
import serial
import os
import msvcrt   # Para leitura do teclado sem pausa no programa
from vpython import *

# Web VPython 3.2
scene.width = scene.height = 500
scene.background = color.gray(0.8)
scene.range = 2.2
scene.caption = "Click to pick an object and make it red."
scene.append_to_caption("\nNote picking of individual curve segments.")
# box(pos=vector(-1, 0, 0), color=color.cyan, opacity=1)
# box(pos=vector(1, -1, 0), color=color.green)
# arrow(pos=vector(-1, -1.3, 0), color=color.orange)
cone_X = cone(pos=vector(1, 0, 0), axis=vector(1, 0, 0), color=color.red, size=vector(0.3, 0.2, 0.2))
cylinder_X = cylinder(pos=vector(0, 0, 0), axis=vector(1, 0, 0), color=color.red, size=vector(1, 0.1, 0.1))
cone_Y = cone(pos=vector(0, 0, 1), axis=vector(0, 0, 1), color=color.green, size=vector(0.2, 0.2, 0.2))
cylinder_Y = cylinder(pos=vector(0, 0, 0), axis=vector(-1, 0, 0), color=color.green, size=vector(1, 0.1, 0.1))
cylinder_Y.rotate(angle=pi/2, axis=vector(0, 1, 0))
cone_Z = cone(pos=vector(0, 1, 0), axis=vector(0, 1, 0), color=color.blue, size=vector(0.2, 0.2, 0.2))
cylinder_Z = cylinder(pos=vector(0, 0, 0), axis=vector(1, 0, 0), color=color.blue, size=vector(1, 0.1, 0.1))
cylinder_Z.rotate(angle=pi/2, axis=vector(0, 0, 1))
length = 0.3
fudge = 0.06 * length
xlabel = label(text="x", color=cone_X.color, pos=cone_X.pos + cone_X.axis + vector(0, fudge, 0), box=False)
ylabel = label(text="y", color=cone_Y.color, pos=cone_Y.pos + cone_Y.axis + vector(fudge, 0, 0), box=False)
zlabel = label(text="z", color=cone_Z.color, pos=cone_Z.pos + cone_Z.axis + vector(fudge, 0, 0), box=False)
AxisGroup = compound([cone_X, cylinder_X, cone_Y, cylinder_Y, cone_Z, cylinder_Z], origin=vec(0, 0, 0))

# sphere(pos=vector(-1.5, 1.5, 0), color=color.white, size=.4 * vector(3, 2, 1))
# square = curve(color=color.yellow, radius=.05)
# square.append(vector(0, 0, 0))
# square.append(pos=vector(0, 1, 0), color=color.cyan, radius=.1)
# square.append(vector(1, 1, 0))
# square.append(pos=vector(1, 0, 0), radius=.1)
# square.append(vector(0.3, -.3, 0))
# v0 = vertex(pos=vector(-.5, 1.2, 0), color=color.green)
# v1 = vertex(pos=vector(1, 1.2, 0), color=color.red)
# v2 = vertex(pos=vector(1, 2, 0), color=color.blue)
# v3 = vertex(pos=vector(-.5, 2, 0), color=color.yellow)
# quad(vs=[v0, v1, v2, v3])
# ring(pos=vector(-0.6, -1.3, 0), size=vector(0.2, 1, 1), color=color.green)
# extrusion(path=[vector(-1.8, -1.3, 0), vector(-1.4, -1.3, 0)],
# shape=shapes.circle(radius=.5, thickness=0.4), color=color.yellow)




counter = 0
data = ""

def Task1(ser):

    global data

    print("Inside Thread 1")
    time.sleep(2)
    while 1:

        if ser.in_waiting > 0:
            # Read one line of data
            data = ser.readline().decode('utf-8').rstrip()
            
            # Print the received data
            # print(data)
            # print("Thread 1 still going on")
        # time.sleep(0.01)


def Task2():
    global counter
    while counter < 10:
        print("Inside Thread 2")
        print("I stopped Task 1 to start and execute Thread 2")
        counter = counter + 1
        print(counter)
        print("Thread 2 complete")
        time.sleep(1)

def read_input():
    if msvcrt.kbhit():
        # Read a single character
        char = msvcrt.getch()
        
        # Return the character as a string
        return char.decode('utf-8')
    
    return None


# Define rotations about the x, y, and z axes.
def Rx(v, angle):
    new_y = cos(angle) * v.y - sin(angle) * v.z
    new_z = sin(angle) * v.y + cos(angle) * v.z
    return vector(v.x, new_y, new_z)

def Ry(v, angle):
    new_x = cos(angle) * v.x + sin(angle) * v.z
    new_z = -sin(angle) * v.x + cos(angle) * v.z
    return vector(new_x, v.y, new_z)

def Rz(v, angle):
    new_x = cos(angle) * v.x - sin(angle) * v.y
    new_y = sin(angle) * v.x + cos(angle) * v.y
    # return vector(new_x, new_y, v.z)
    return vector(0.2, 0.9, v.z)


def Main():
    global counter, data
    old_roll = old_pitch = old_yaw = 0.0
    diff_roll = diff_pitch = diff_yaw = 0.0

    # Define the serial port and baud rate
    port = 'COM7'  # Replace with your actual serial port
    baud_rate = 115200  # Replace with your baud rate
    # Create a serial object
    ser = serial.Serial(port, baud_rate)
    t1 = threading.Thread(target = Task1, args=[ser])
    # t2 = threading.Thread(target = Task2, args=[])
    print("Starting Thread 1")
    t1.start()
    # print("Starting Thread 2")
    # t2.start()
    
    key = "None"
 
    while key != "q":
        # Read input continuously
        key = read_input()
        if key is not None:
            # Print the pressed key
            print("Pressed key:", key)
        
        # Perform other operations or exit the loop based on the input
        # ...

        # print("Main", counter)
        # print(key)
        # counter = counter + 1
        # Print the received data
        # print(data)
        # Split the values in an array with a separator character
        y = data.split(',')
        if y[0] == '':
            # print("Data: ", data)
            acc_x = 0.0
            acc_y = 0.0
            acc_z = 0.0
            roll = 0.0
            pitch = 0.0
            yaw = 0.0
        if y[0] != '':
            if y[0] == 'Linear:':
                acc_x = float(y[1])
                acc_y = float(y[2])
                acc_z = float(y[3])
            if y[0] == 'Orient:':
                roll = float(y[1])
                pitch = float(y[2])
                yaw = float(y[3])
            diff_roll = old_roll - roll
            old_roll = roll
            diff_pitch = old_pitch - pitch
            old_pitch = pitch
            diff_yaw = old_yaw - yaw
            old_yaw = yaw

        print("Acc x:", acc_x, "Acc y:", acc_y, "Acc z:", acc_y, "Roll:", roll, "Pitch:", pitch, "Yaw:", yaw)
        diff_roll = 0.01
        AxisGroup.rotate(angle=diff_roll * pi / 2, axis=vector(1, 1, 1))
        # AxisGroup.rotate(angle=diff_roll * pi / 180, axis=vector(0, 1, 0), origin=vector(0, 1, 0))
        # AxisGroup.rotate(angle=diff_pitch * pi / 180, axis=vector(0, 0, 1), origin=vector(0, 0, 1))
        # AxisGroup.rotate(angle=diff_yaw * pi / 180, axis=vector(1, 0, 0), origin=vector(1, 0, 0))
        # print(AxisGroup.axis.x, AxisGroup.axis.y, AxisGroup.axis.z)
        # cylinder_X.axis = Rz(cylinder_X.axis, pi / 400)
        # cylinder_X.axis = vector(0.9, 0.2, 0)
        AxisGroup.axis = vector(0.0, 0.0, 0.0)

        time.sleep(0.01)

    print("=== exiting ===")
    ser.close()

if __name__ == '__main__':
    
    Main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
