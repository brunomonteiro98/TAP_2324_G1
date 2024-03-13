
from tkinter import ttk
import threading
import tkinter
from tkinter import *
from threading import Thread
import socket
import json
import time
import sys
import re

global entrya1
global entrya2
global aux



def connectETController(ip, port=8055):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        return (True, sock)
    except Exception as e:
        sock.close()
        return (False, None)


def disconnectETController(sock):
    if (sock):
        sock.close()
        sock = None
    else:
        sock = None

def sendCMD(sock, cmd, params=None, id=1):
    if (not params):
        params = []
    else:
        params = json.dumps(params)
    sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(cmd, params, id) + "\n"
    try:
        # print(sendStr)
        sock.sendall(bytes(sendStr, "utf-8"))
        ret = sock.recv(1024)
        jdata = json.loads(str(ret, "utf-8"))
        if ("result" in jdata.keys()):
            return (True, json.loads(jdata["result"]), jdata["id"])
        elif ("error" in jdata.keys()):
            return (False, jdata["error"], jdata["id"])
        else:
            return (False, None, None)
    except Exception as e:
        return (False, None, None)

def command1(event):
    #if entry1.get() == 'root' and entry2.get() == 'elite2014':
        top.destroy()
        c = classapp()
        c.defapp()

def command2():
    #if (entry1.get() == 'root' and entry2.get() == 'elite2014'):
        top.destroy()
        c = classapp()
        c.defapp()

def command3():
    c = classapp()
    c.defapp()

def ledClearalarm():
    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    if (conSuc):
        retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
        if (retstatus == True and resultstatus == 4):
            print("I have an error. Now my state is: Error State")
            clr = "green"
        else:
            print("Robot doesn't has any error")
            clr = "red"

def Clearalarm():
    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    # print(conSuc)
    if (conSuc):
        retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
        bstop0status, bstop0result, id = sendCMD(sock, "getInput", {"addr": 0})
        bstop1status, bstop1result, id = sendCMD(sock, "getInput", {"addr": 1})
        if (retstatus == True and bstop0status == True and bstop1status == True and resultstatus == 4 and bstop0result == 1 and bstop1result == 1):
            # Verificar Estado do Robo
            print("I have an error. Now my state is: Error State")
            while (resultstatus == 4 and bstop0result == 1 and bstop1result == 1):
                retclear, retstatus, id = sendCMD(sock, "ClearAlarm")
                time.sleep(0.5)
                retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
                if (resultstatus != 4):

                    if (resultstatus == 0):
                        print("I don't have any error. Now my state is: Stop State")
                    if (resultstatus == 1):
                        print("I don't have any error. Now my state is: Pause State")
                    if (resultstatus == 2):
                        print("I don't have any error. Now my state is: Emergency Stop State")
                    if (resultstatus == 3):
                        print("I don't have any error. Now my state is: Running State")
                    if (resultstatus == 4):
                        print("I don't have any error. Now my state is: Error State")
                    if (resultstatus == 5):
                        print("I don't have any error. Now my state is: Collision State")
        else:

            if (resultstatus == 0):
                print("I don't have any error. Now my state is: Stop State")
            if (resultstatus == 1):
                print("I don't have any error. Now my state is: Pause State")
            if (resultstatus == 2):
                print("I don't have any error. Now my state is: Emergency Stop State")
            if (resultstatus == 3):
                print("I don't have any error. Now my state is: Running State")
            if (resultstatus == 4):
                print("I don't have any error. Now my state is: Error State")
            if (resultstatus == 5):
                print("I don't have any error. Now my state is: Collision State")

    else:
        print("Connection Failed")
    disconnectETController(sock)

def Sync():
    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    if (conSuc):
        syncstatus, syncresult, id = sendCMD(sock, "getMotorStatus")
        retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
        bstop0status, bstop0result, id = sendCMD(sock, "getInput", {"addr": 0})
        bstop1status, bstop1result, id = sendCMD(sock, "getInput", {"addr": 1})
        if (retstatus == True and bstop0status == True and bstop1status == True and syncstatus == True and resultstatus != 4 and bstop0result == 1 and bstop1result == 1 and syncresult == 0):
            # Verificar Estado do Robo
            print("I'm not synchronized")

            while (syncresult== 0 and syncstatus== True):
                # Synchronize servo encoder data
                syncstatus, syncresult, id = sendCMD(sock, "syncMotorStatus")
                time.sleep(0.5)
                retstatus, resultstatus, id = sendCMD(sock, "getMotorStatus")
                if (syncresult == 1):
                    print("Now I'm ready and synchronized")
        else:
            print("I'm already sychronized")
    else:
        print("Connection Failed")
    disconnectETController(sock)

def Servon():
    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    if (conSuc):
        syncstatus, syncresult, id = sendCMD(sock, "getMotorStatus")
        retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
        retservo, servoresult, id = sendCMD(sock, "getServoStatus")
        bstop0status, bstop0result, id = sendCMD(sock, "getInput", {"addr": 0})
        bstop1status, bstop1result, id = sendCMD(sock, "getInput", {"addr": 1})
        if (retstatus == True and bstop0status == True and bstop1status == True and retservo == True and syncstatus == True and resultstatus !=4 and bstop0result == 1 and bstop1result == 1 and syncresult == 1 and servoresult == 0):
            #Verificar Estado do Robo
            print("Servos are off")
            while (servoresult == 0 and retservo == True):
                #Turn On Servos
                retservo, servoresult, id = sendCMD(sock, "set_servo_status",{"status":1})
                time.sleep(0.5)
                retservo, servoresult, id = sendCMD(sock,"getServoStatus")
                if (servoresult == 1):
                    print("Now Servos are on")
        else:
            print("I already have Servos on")
    else:
        print("Connection Failed")
    disconnectETController(sock)

def ManualMode():
        global running
        aux = 1
        man = Tk()
        running = False

        man.title("Jog Mode")
        man.geometry("230x550")
        global ButtonXmin
        global ButtonXmax
        global ButtonYmin
        global ButtonYmax
        global ButtonZmin
        global ButtonZmax
        global ButtonRXmin
        global ButtonRXmax
        global ButtonRYmin
        global ButtonRYmax
        global ButtonRZmin
        global ButtonRZmax
        global t
        global ent1

        labl1 = Label(man, text='Choose Velocity:')
        ent1 = Entry(man)
        labl1.place(x=5, y=20)
        ent1.place(x=100, y=20)
        ButtonBack = Button(man, text="Back", command=lambda:[man.destroy(), command3()])
        ButtonBack.place(x=65, y=460, width=100, height=20)

        ButtonXmin = Button(man, text="X-")
        ButtonXmin.bind('<ButtonPress-1>',Jog0)
        ButtonXmin.bind('<ButtonRelease-1>', StopJog)
        ButtonXmin.place(x=60, y=80,width=50, height=50)

        ButtonXmax = Button(man, text="X+")
        ButtonXmax.bind('<ButtonPress-1>', Jog1)
        ButtonXmax.bind('<ButtonRelease-1>', StopJog)
        ButtonXmax.place(x=120, y=80, width=50, height=50)

        ButtonYmin = Button(man, text="Y-")
        ButtonYmin.bind('<ButtonPress-1>', Jog2)
        ButtonYmin.bind('<ButtonRelease-1>', StopJog)
        ButtonYmin.place(x=60, y=140, width=50, height=50)

        ButtonYmax = Button(man, text="Y+")
        ButtonYmax.bind('<ButtonPress-1>', Jog3)
        ButtonYmax.bind('<ButtonRelease-1>', StopJog)
        ButtonYmax.place(x=120, y=140, width=50, height=50)

        ButtonZmin = Button(man, text="Z-")
        ButtonZmin.bind('<ButtonPress-1>', Jog4)
        ButtonZmin.bind('<ButtonRelease-1>', StopJog)
        ButtonZmin.place(x=60, y=200, width=50, height=50)

        ButtonZmax = Button(man, text="Z+")
        ButtonZmax.bind('<ButtonPress-1>', Jog5)
        ButtonZmax.bind('<ButtonRelease-1>', StopJog)
        ButtonZmax.place(x=120, y=200, width=50, height=50)

        ButtonRXmin = Button(man, text="RX-")
        ButtonRXmin.bind('<ButtonPress-1>', Jog6)
        ButtonRXmin.bind('<ButtonRelease-1>', StopJog)
        ButtonRXmin.place(x=60, y=260, width=50, height=50)

        ButtonRXmax = Button(man, text="RX+")
        ButtonRXmax.bind('<ButtonPress-1>', Jog7)
        ButtonRXmax.bind('<ButtonRelease-1>', StopJog)
        ButtonRXmax.place(x=120, y=260, width=50, height=50)

        ButtonRYmin = Button(man, text="RY-")
        ButtonRYmin.bind('<ButtonPress-1>', Jog8)
        ButtonRYmin.bind('<ButtonRelease-1>', StopJog)
        ButtonRYmin.place(x=60, y=320, width=50, height=50)

        ButtonRYmax = Button(man, text="RY+")
        ButtonRYmax.bind('<ButtonPress-1>', Jog9)
        ButtonRYmax.bind('<ButtonRelease-1>', StopJog)
        ButtonRYmax.place(x=120, y=320, width=50, height=50)

        ButtonRZmin = Button(man, text="RZ-")
        ButtonRZmin.bind('<ButtonPress-1>', Jog10)
        ButtonRZmin.bind('<ButtonRelease-1>', StopJog)
        ButtonRZmin.place(x=60, y=380, width=50, height=50)

        ButtonRZmax = Button(man, text="RZ+")
        ButtonRZmax.bind('<ButtonPress-1>', Jog11)
        ButtonRZmax.bind('<ButtonRelease-1>', StopJog)
        ButtonRZmax.place(x=120, y=380, width=50, height=50)

        man.mainloop()




def Jog0(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=0
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
    main()

def Jog1(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=1
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
    main()

def Jog2(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=2
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
    main()

def Jog3(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=3
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
    main()

def Jog4(event):
    global running

    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=4
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
    main()

def Jog5(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=5
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()

def Jog6(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=6
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()

def Jog7(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=7
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()

def Jog8(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=8
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()

def Jog9(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=9
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()

def Jog10(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=10
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()

def Jog11(event):
    global running
    global bs
    running = True
    if len(ent1.get()) != 0:
        Jvel = int(ent1.get())
        ip = "192.168.1.63"
        bs=11
        conSuc, sock = connectETController(ip)
        if Jvel >= 0.05 and Jvel <= 100:
            if (conSuc):
                suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed":Jvel})
                time.sleep(0.2)
            disconnectETController(sock)

        else:
            print("Invalid Velocity Value")
        main()


def StopJog(event):
    global running
    running = False
    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    if (conSuc):
        suc, result, id = sendCMD(sock, "stop")
    disconnectETController(sock)

def AutomaticMode():
        aux = 1
        aut = Tk()

        global entrya1
        global entrya2
        global ButtonPlayRun
        aut.title("Automatic Mode")
        aut.geometry("550x300")
        ButtonPlayRun = Button(aut, text="Run",command=PlayProg).place(x=40,y=100,width=100,height=20)
        ButtonStop = Button(aut, text="Stop",command=StopProg).place(x=150, y=100, width=100, height=20)
        ButtonBack = Button(aut, text="Back" ,command=lambda: [aut.destroy(), command3()]).place(x=70, y=200, width=100, height=20)
        lbal1 = Label(aut, text='Choose Program:')
        entrya1 = Entry(aut)
        lbal2 = Label(aut, text='Velocity:')
        entrya2 = Entry(aut)

        lbal1.place(x=40, y=10)
        entrya1.place(x=140, y=10)
        lbal2.place(x=50, y=40)
        entrya2.place(x=140, y=40)





def PlayProg():

    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    jbi_filename = entrya1.get()
    speed = entrya2.get()
    speedint = int(speed)

    if (conSuc):
        checkJbistatus, checkJbiresult, id = sendCMD(sock, "checkJbiExist",{"filename":jbi_filename})
        syncstatus, syncresult, id = sendCMD(sock, "getMotorStatus")
        retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
        retservo, servoresult, id = sendCMD(sock, "getServoStatus")
        bstop0status, bstop0result, id = sendCMD(sock, "getInput", {"addr": 0})
        bstop1status, bstop1result, id = sendCMD(sock, "getInput", {"addr": 1})
        if (retstatus == True and bstop0status == True and bstop1status == True and retservo == True and checkJbistatus == True and syncstatus == True and resultstatus != 4 and bstop0result == 1 and bstop1result == 1 and syncresult == 1 and servoresult == 1 and checkJbiresult == 1):
            speedstatus, speedresult, id = sendCMD(sock, "setSpeed", {"value": speedint})
            if (speedresult == 1):
                runstatus, runresult, id = sendCMD(sock, "runJbi",{"filename":jbi_filename})
            else:
                print("Impossible Value")

        else:
            print("Program Not Found")

    else:
        print("Connection Failed")

    disconnectETController(sock)

def StopProg():

    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    if (conSuc):
        retstatus, resultstatus, id = sendCMD(sock, "getRobotState")
        if (resultstatus==3):
            stopstatus, stopresult, id = sendCMD(sock, "stop")
            print("Robot was stop successfully")
        else:
            print("I'm not running")
    else:
        print("Connection Failed")

def move_forward(arg):
    t = threading.current_thread()
    while getattr(t, "running",True) and (ButtonXmin.bind('<ButtonPress-1>', Jog0) or ButtonXmax.bind('<ButtonPress-1>', Jog1) or ButtonYmin.bind('<ButtonPress-1>', Jog2) or ButtonYmax.bind('<ButtonPress-1>', Jog3) or ButtonZmin.bind('<ButtonPress-1>', Jog4) or ButtonZmax.bind('<ButtonPress-1>', Jog5) or ButtonRXmin.bind('<ButtonPress-1>', Jog6) or ButtonRXmax.bind('<ButtonPress-1>', Jog7) or ButtonRYmin.bind('<ButtonPress-1>', Jog8) or ButtonRYmax.bind('<ButtonPress-1>', Jog9) or ButtonRZmin.bind('<ButtonPress-1>', Jog10) or ButtonRZmax.bind('<ButtonPress-1>', Jog11) ):
        if running == True:
            if len(ent1.get())!=0:
                Jvel = int(ent1.get())
                ip = "192.168.1.63"
                conSuc, sock = connectETController(ip)
                if Jvel >= 0.05 and Jvel <= 100:
                    if (conSuc):
                        suc, result, id = sendCMD(sock, "jog", {"index": bs, "speed": Jvel})
                        time.sleep(0.2)

                    disconnectETController(sock)

                else:
                    print("Invalid Velocity Value")
            else:
                print("Invalid Velocity Value")
        else:
            print("Jog Stopped")
            time.sleep(2)
            break



def main():
    t = threading.Thread(target=move_forward, args=("task",))
    t.start()
    time.sleep(0.2)

def SettingsMode():
    global cbs1
    global cbs2
    global cbs3
    global cbs4
    global cbs5
    global entry5s
    global cbs6
    global cbs6s
    global cbs7
    global cbs7s
    global cbs8
    global entry8s
    global cbs9
    global entry9s
    global cbs10
    global entry10s

    setts = Tk()
    setts.title("Settings")
    setts.geometry("400x650")

    labls1 = Label(setts, text='Choose Coord System:')
    cbs1 = ttk.Combobox(setts, values=("Joint", "World", "Tool", "User", "Cylinder"))
    labls1.place(x=5, y=20)
    cbs1.place(x=180, y=20)

    labls2 = Label(setts, text='Choose Cycle Mode:')
    cbs2 = ttk.Combobox(setts, values=("Single Step", "Single Cycle", "Continuous Cycle"))
    labls2.place(x=5, y=80)
    cbs2.place(x=180, y=80)

    labls3 = Label(setts, text='Choose User System:')
    cbs3 = ttk.Combobox(setts, values=("0","1","2","3","4","5","6","7"))
    labls3.place(x=5, y=140)
    cbs3.place(x=180, y=140)

    labls4 = Label(setts, text='Choose Tool System: ')
    cbs4 = ttk.Combobox(setts, values=("0","1","2","3","4","5","6","7"))
    labls4.place(x=5, y=200)
    cbs4.place(x=180, y=200)

    labls5 = Label(setts, text='Choose Analog Output :')
    cbs5 = ttk.Combobox(setts, values=("1","2","3","4","5"))
    labls5.place(x=5, y=260)
    cbs5.place(x=180, y=260)

    entry5s = Entry(setts)
    entry5s.place(x=350, y=260, width=40, height=20)

    labls6 = Label(setts, text='Choose Digital Output :')
    cbs6 = ttk.Combobox(setts, values=("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16",
                                       "17","18","19","48","49"))
    labls6.place(x=5, y=320)
    cbs6.place(x=180, y=320)

    cbs6s = ttk.Combobox(setts, values=("On", "Off"))
    cbs6s.place(x=350, y=320, width=40, height=20)

    labls7 = Label(setts, text='Choose Virtual Output :')
    cbs7 = ttk.Combobox(setts, values=[n for n in range(528,800,1)])
    labls7.place(x=5, y=380)
    cbs7.place(x=180, y=380)

    cbs7s = ttk.Combobox(setts, values=("On", "Off"))
    cbs7s.place(x=350, y=380, width=40, height=20)

    labls8 = Label(setts, text='Set System B variable value :')
    cbs8 = ttk.Combobox(setts, values=[n for n in range(000, 256, 1)])
    labls8.place(x=5, y=440)
    cbs8.place(x=180, y=440)

    entry8s = Entry(setts)
    entry8s.place(x=350, y=440, width=40, height=20)


    labls9 = Label(setts, text='Set System I variable value :')
    cbs9 = ttk.Combobox(setts, values=[n for n in range(000, 256, 1)])
    labls9.place(x=5, y=500)
    cbs9.place(x=180, y=500)

    entry9s = Entry(setts)
    entry9s.place(x=350, y=500, width=40, height=20)

    labls10 = Label(setts, text='Set System D variable value :')
    cbs10 = ttk.Combobox(setts, values=[n for n in range(000, 256, 1)])
    labls10.place(x=5, y=560)
    cbs10.place(x=180, y=560)

    entry10s = Entry(setts)
    entry10s.place(x=350, y=560, width=40, height=20)

    ButtonRet = Button(setts, text="Back", command=lambda: [setts.destroy(),command3()]).place(x=75, y=600, width=100, height=20)
    ButtonVal = Button(setts, text="Validate", command=validation).place(x=225, y=600, width=100, height=20)

def validation():
    global cs
    global Doit
    cs=cbs1.get()
    if cs == "Joint" and len(cbs1.get())!=0:
        cm = 0
        Doit = True
    elif cs == "World" and len(cbs1.get())!=0:
        cm = 1
        Doit = True
    elif cs == "Tool" and len(cbs1.get())!=0:
        cm = 2
        Doit = True
    elif cs == "User" and len(cbs1.get())!=0:
        cm = 3
        Doit = True
    elif cs == "Cylinder" and len(cbs1.get())!=0:
        cm = 4
        Doit = True
    elif len(cbs1.get())==0:
        Doit = False
    elif cs != "Joint" and cs !="World" and cs != "Tool" and cs !="User" and cs !="Cylinder" and len(cbs1.get())!=0:
        print("This value can't be use")
        Doit = False


    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, cmresult, cmid = sendCMD(sock, "getCurrentCoord")
            if (cmsuc == True and cm != cmresult):
                #Verificar se o robô está num sistema de coordenadas diferente
                print("Robot has a diferent system actually")
                while (cmsuc == True and cm != cmresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setCurrentCoord", {"coord_mode": cm})
                    time.sleep(0.5)
                    cmsuc, cmresult, cmid = sendCMD(sock, "getCurrentCoord")
                    if (cmsuc == True and cm == cmresult):
                        print("Robot coordinate system was changed successfully")
                        Doit = False
            elif (cmsuc == True and cm == cmresult):
                print("Robot already had this system coordinate")
                Doit = False
            else:
                print("Error getting current system coordinate")
                Doit = False
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global css
    css = cbs2.get()

    if css == "Single Step" and len(cbs2.get()) != 0:
        cms = 0
        Doit = True
    elif css == "Single Cycle" and len(cbs2.get()) != 0:
        cms = 1
        Doit = True
    elif css == "Continuous Cycle" and len(cbs2.get()) != 0:
        cms = 2
        Doit = True
    elif len(cbs2.get()) == 0:
        Doit = False
    elif css != "Single Step" and css !="Single Cycle" and css != "Continuous Cycle" and len(cbs2.get())!=0:
        print("This value can't be use")
        Doit = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, cmresult, cmid = sendCMD(sock, "getCycleMode")
            if (cmsuc == True and cms != cmresult):
                # Verificar se o robô está no cycle mode
                print("Robot has a diferent system actually")
                while (cmsuc == True and cms != cmresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setCycleMode", {"cycle_mode": cms})
                    time.sleep(0.5)
                    cmsuc, cmresult, cmid = sendCMD(sock, "getCycleMode")
                    if (cmsuc == True and cms == cmresult):
                        print("Robot coordinate system was changed successfully")
                        Doit = False
            elif (cmsuc == True and cms == cmresult):
                print("Robot already had this system coordinate")
                Doit = False
            else:
                print("Error getting current system coordinate")
                Doit = False
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global cus
    cus = cbs3.get()

    if cus == "0" and len(cbs3.get()) != 0:
        ucs = 0
        Doit = True
    elif cus == "1" and len(cbs3.get()) != 0:
        ucs = 1
        Doit = True
    elif cus == "2" and len(cbs3.get()) != 0:
        ucs = 2
        Doit = True
    elif cus == "3" and len(cbs3.get()) != 0:
        ucs = 3
        Doit = True
    elif cus == "4" and len(cbs3.get()) != 0:
        ucs = 4
        Doit = True
    elif cus == "5" and len(cbs3.get()) != 0:
        ucs = 5
        Doit = True
    elif cus == "6" and len(cbs3.get()) != 0:
        ucs = 6
        Doit = True
    elif cus == "7" and len(cbs3.get()) != 0:
        ucs = 7
        Doit = True
    elif len(cbs3.get()) == 0:
        Doit = False
    elif cus != "0" and cus != "1" and cus != "2" and cus != "3" and cus != "4" and css != "5" and css != "6" and css != "7" and len(cbs3.get())!=0:
        print("This value can't be use")
        Doit = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, cmresult, cmid = sendCMD(sock, "getUserNumber")
            if (cmsuc == True and ucs != cmresult):
                # Verificar se o robô está no cycle mode
                print("Robot has a diferent system actually")
                while (cmsuc == True and ucs != cmresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setUserNumber", {"user_num": ucs})
                    time.sleep(0.5)
                    cmsuc, cmresult, cmid = sendCMD(sock, "getUserNumber")
                    if (cmsuc == True and ucs == cmresult):
                        print("Robot coordinate system was changed successfully")
                        Doit = False
            elif (cmsuc == True and ucs == cmresult):
                print("Robot already had this system coordinate")
                Doit = False
            else:
                print("Error getting current system coordinate")
                Doit = False
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global cts
    cts = cbs4.get()

    if cts == "0" and len(cbs4.get()) != 0:
        tcs = 0
        Doit = True
    elif cts == "1" and len(cbs4.get()) != 0:
        tcs = 1
        Doit = True
    elif cts == "2" and len(cbs4.get()) != 0:
        tcs = 2
        Doit = True
    elif cts == "3" and len(cbs4.get()) != 0:
        tcs = 3
        Doit = True
    elif cts == "4" and len(cbs4.get()) != 0:
        tcs = 4
        Doit = True
    elif cts == "5" and len(cbs4.get()) != 0:
        tcs = 5
        Doit = True
    elif cts == "6" and len(cbs4.get()) != 0:
        tcs = 6
        Doit = True
    elif cts == "7" and len(cbs4.get()) != 0:
        tcs = 7
        Doit = True
    elif len(cbs4.get()) == 0:
        Doit = False
    elif cts != "0" and cts != "1" and cts != "2" and cts != "3" and cts != "4" and cts != "5" and cts != "6" and cts != "7" and len(cbs4.get()) != 0:
        print("This value can't be use")
        Doit = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, cmresult, cmid = sendCMD(sock, "getAutoRunToolNumber")
            if (cmsuc == True and tcs != cmresult):
                # Verificar se o robô está no cycle mode
                print("Robot has a diferent system actually")
                while (cmsuc == True and tcs != cmresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setAutoRunToolNumber", {"tool_num": tcs})
                    time.sleep(0.5)
                    cmsuc, cmresult, cmid = sendCMD(sock, "getAutoRunToolNumber")
                    if (cmsuc == True and tcs == cmresult):
                        print("Robot coordinate system was changed successfully")
                        Doit = False
            elif (cmsuc == True and tcs == cmresult):
                print("Robot already had this system coordinate")
                Doit = False
            else:
                print("Error getting current system coordinate")
                Doit = False
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global ao
    global aos
    ao = cbs5.get()

    if ao == "1" and len(cbs5.get()) != 0:
        aos = 0

        print("0")
    elif ao == "2" and len(cbs5.get()) != 0:
        aos = 1

        print("2")
    elif ao == "3" and len(cbs5.get()) != 0:
        aos = 2

        print("3")
    elif ao == "4" and len(cbs5.get()) != 0:
        aos = 3

        print("4")
    elif ao == "5" and len(cbs5.get()) != 0:
        aos = 4

        print("5")
    elif len(cbs5.get()) == 0:
        aos = 99
    elif ao != "1" and ao != "2" and ao != "3" and ao != "4" and ao != "5" and len(cbs5.get()) != 0:
        aos = 99
        print("This value can't be use")


    aov = entry5s.get()
    if aos >= 0 and aos <= 4 and len(entry5s.get())!=0:

        if aov.replace('.','',1).isdigit():
            aovf = float(aov)

            if aovf >= -10 and aovf <= 10:
                Doit = True
            else:
                print("Invalid Value")
                Doit = False

        else:
            print("Invalid Value")
            Doit = False

    else:
        Doit = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, sresult, sid = sendCMD(sock, "setAnalogOutput", {"addr": aos, "value":aovf})

            if (cmsuc == True):
                        print("Analog Output was changed successfully")
                        Doit = False
            else:
                print("Error writting on Analog Output")
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global do
    global dos
    global dov

    do = cbs6.get()

    if len(do) != 0:
        don = int(do)

        if ((don >= 0 and don <= 19) or don == 48 or don == 49):
            dovs = cbs6s.get()
            if dovs == "On":
                dov = 1
                Doit = True
            if dovs == "Off":
                dov = 0
                Doit = True
        elif len(cbs6s.get()) == 0 or len(cbs6.get() == 0):
            Doit = False
        elif ((don > 19 and don <= 47) or don >= 52) and len(cbs6s.get()) != 0:
            print("Invalid Value")
            Doit = False


    if Doit == True:
            ip = "192.168.1.63"
            conSuc, sock = connectETController(ip)
            if (conSuc):
                cmsuc, sresult, sid = sendCMD(sock, "setOutput",{"addr": don, "status": dov})
                time.sleep(0.5)
                if (cmsuc == True):
                    print("Digital Output was changed successfully")
                    Doit = False
                else:
                    print("Error writting on Digital Output")
                    print(cmsuc)
            else:
                print("Connection Failed")
                Doit = False

            disconnectETController(sock)

    global vdo
    global vdos
    global vdov
    vdo = cbs7.get()

    if len(vdo) != 0:
        vdon = int(vdo)

        if (vdon >= 528 and vdon <= 799):
            vdovs = cbs7s.get()
            if vdovs == "On":
                vdov = 1
                Doit = True
            if vdovs == "Off":
                vdov = 0
                Doit = True
        elif len(cbs7s.get()) == 0 or len(cbs7.get() == 0):
            Doit = False
        elif ((vdon > 0 and vdon <= 527) or vdon >= 800) and len(cbs7s.get()) != 0:
            print("Invalid Value")
            Doit = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, sresult, sid = sendCMD(sock, "getVirtualOutput", {"addr": vdon})
            if (cmsuc == True):
                while (cmsuc == True and vdov !=sresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setVirtualOutput", {"addr": vdon, "status":vdov})
                    time.sleep(0.5)
                    cmsuc, sresult, sid = sendCMD(sock, "getVirtualOutput", {"addr": vdon})
                print("Virtual Output was changed successfully")
                Doit = False
            else:
                print("Error writting on Virtual Output")
                print(cmsuc)
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global bv
    global bvs
    global bvsi


    bv = cbs8.get()



    if len(bv) != 0:
        bvn = int(bv)
        try:
            bvs = entry8s.get()
            bvsi =int(bvs)
            nf = True

        except:
            print("Invalid Value")
            nf = False

    else:
        nf = False

    if nf == True and bvn >= 0 and bvn <= 255 and len(cbs8.get()) != 0 and len(entry8s.get())!=0:

        if bvsi >= 0 and bvsi <= 2147483647 and len(entry8s.get())!=0:
            Doit = True
            nf = False

        else:
            print("Invalid Value1")
            Doit = False
            nf = False



    elif nf == True and (bvn < 0 or bvn > 255) and len(cbs8.get()) != 0 and len(entry8s.get())!=0:
        print("This value can't be use")
        Doit = False
        nf = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, sresult, sid = sendCMD(sock, "getSysVarB", {"addr": bvn})
            if (cmsuc == True):
                while (cmsuc == True and bvsi != sresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setSysVarB", {"addr": bvn, "value": bvsi})
                    time.sleep(0.5)
                    cmsuc, sresult, sid = sendCMD(sock, "getSysVarB", {"addr": bvn})
                print("System Variable B was changed successfully")
                Doit = False
            else:
                print("Error writting variable B")
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global iv
    global ivs
    global ivsi


    iv = cbs9.get()



    if len(iv) != 0:
        ivn = int(iv)
        try:
            ivs = entry8s.get()
            ivsi =int(ivs)
            nf = True

        except:
            print("Invalid Value")
            nf = False

    else:
        nf = False

    if nf == True and ivn >= 0 and ivn <= 255 and len(cbs9.get()) != 0 and len(entry9s.get())!=0:

        if ivsi >= 0 and ivsi <= 2147483647 and len(entry9s.get())!=0:
            Doit = True
            nf = False

        else:
            print("Invalid Value1")
            Doit = False
            nf = False



    elif nf == True and (ivn < 0 or ivn > 255) and len(cbs9.get()) != 0 and len(entry9s.get())!=0:
        print("This value can't be use")
        Doit = False
        nf = False

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, sresult, sid = sendCMD(sock, "getSysVarI", {"addr": ivn})
            if (cmsuc == True):
                while (cmsuc == True and ivsi != sresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setSysVarI", {"addr": ivn, "value": ivsi})
                    time.sleep(0.5)
                    cmsuc, sresult, sid = sendCMD(sock, "getSysVarI", {"addr": ivn})
                print("System Variable I was changed successfully")
                Doit = False
            else:
                print("Error writting variable I")
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

    global dv
    global dvs
    global dvsi

    dv = cbs10.get()

    if len(dv) != 0:
        dvn = int(dv)
        try:
            dvs = entry10s.get()
            dvsi = float(dvs)
            nf = True

        except:
            print("Invalid Value")
            nf = False

    else:
        nf = False

    if nf == True and dvn >= 0 and dvn <= 255 and len(entry10s.get())!=0:

            if dvsi >= -100000000 and dvsi <= 100000000:
                Doit = True
            else:
                print("Invalid Value")
                Doit = False

    else:
        Doit = False
        print("Invalid Value")

    if Doit == True:
        ip = "192.168.1.63"
        conSuc, sock = connectETController(ip)
        if (conSuc):
            cmsuc, sresult, sid = sendCMD(sock, "getSysVarD", {"addr": dvn})
            if (cmsuc == True):
                while (cmsuc == True and dvsi != sresult):
                    cmsuc, sresult, sid = sendCMD(sock, "setSysVarD", {"addr": dvn, "value": dvsi})
                    time.sleep(0.5)
                    cmsuc, sresult, sid = sendCMD(sock, "getSysVarD", {"addr": dvn})
                print("System Variable D was changed successfully")
                Doit = False
            else:
                print("Error writting variable D")
        else:
            print("Connection Failed")
            Doit = False

        disconnectETController(sock)

def ConfigurationMode():
    configs = Tk()
    configs.title("Configuration")
    configs.geometry("400x650")

    ip = "192.168.1.63"
    conSuc, sock = connectETController(ip)
    if (conSuc):
        cmsuc, sresult, sid = sendCMD(sock, "getRobotPos")
        if (cmsuc == True):
                cmsuc, sresult, sid = sendCMD(sock, "positiveKinematic", {"targetPos": sresult})
                rxcg = ' '.join([str(elem) for elem in sresult])
                print(rxcg)
        else:
            print("Error writting variable D")
    else:
        print("Connection Failed")
        Doit = False

    disconnectETController(sock)



    lCM1 = Label(configs, text='Choose Point System:')
    cCM1 = ttk.Combobox(configs, values=("P", "V"))
    lCM1.place(x=5, y=20)
    cCM1.place(x=180, y=20)

    lCM2 = Label(configs, text='Choose Cycle Mode:')
    cCM2 = ttk.Combobox(configs, values=("Single Step", "Single Cycle", "Continuous Cycle"))
    lCM2.place(x=5, y=80)
    cCM2.place(x=180, y=80)

    lCM3 = Label(configs, text='Choose User System:')
    cCM3 = ttk.Combobox(configs, values=("0", "1", "2", "3", "4", "5", "6", "7"))
    lCM3.place(x=5, y=140)
    cCM3.place(x=180, y=140)

    lCM4 = Label(configs, text='Choose Tool System: ')
    cCM4 = ttk.Combobox(configs, values=("0", "1", "2", "3", "4", "5", "6", "7"))
    lCM4.place(x=5, y=200)
    cCM4.place(x=180, y=200)

    ButtonBack = Button(configs, text="Back", command=lambda: [configs.destroy(), command3()]).place(x=75, y=600, width=100, height=20)


class classapp():

    def defapp(self):
        aux = 0
        app = Tk()
        app.title("Robot Interface")
        app.geometry("550x300")
        app.configure(background='white')

        ButtonCA = Button(app, text="Clear Alarm", command=Clearalarm).place(x=50, y=10, width=200, height=40)
        ButtonSync = Button(app, text="Sync Encoders", command=Sync).place(x=300, y=10, width=200, height=40)
        ButtonServo = Button(app, text="Enable Servos", command=Servon).place(x=50, y=60, width=200, height=40)
        ButtonManual = Button(app, text="Jog Mode", command=lambda: [app.destroy(), ManualMode()]).place(x=50, y=110, width=200, height=40)
        ButtonAutomatic = Button(app, text="Automatic Mode", command=lambda:[app.destroy(), AutomaticMode()]).place(x=300, y=60, width=200, height=40)
        ButtonSettings = Button(app, text="Settings", command=lambda:[app.destroy(), SettingsMode()]). place(x=300, y=110, width=200, height=40)
        ButtonConfiguration = Button(app, text="Configuration", command=lambda: [app.destroy(), ConfigurationMode()]).place(x=50, y=160, width=200, height=40)

        mainloop()

if __name__ == "__main__":
    top = Tk()


    top.geometry('300x150')
    top.title('Login')
    lbl1 = Label(top, text='Username:')
    entry1 = Entry(top)
    lbl2 = Label(top, text='Password:')
    entry2 = Entry(top, show="*")
    connectbutton = Button(top, text="Connect", command=command2)

    entry2.bind('<Return>', command1)
    lbl1.place(x=50,y=10)
    entry1.place(x=110,y=10)
    lbl2.place(x=50,y=40)
    entry2.place(x=110,y=40)
    connectbutton.place(x=110,y=70)

    top.mainloop()