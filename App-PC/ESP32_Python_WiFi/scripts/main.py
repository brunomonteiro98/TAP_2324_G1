from gui import GUI
from wifi_communicator import WiFiCommunicator

def main():
    communicator = WiFiCommunicator(max_buffer_sz=128)  # 128 bytes
    gui = GUI(communicator=communicator) # Create the GUI
    gui.mainloop()  # Start the GUI

if __name__ == '__main__':
    main()
