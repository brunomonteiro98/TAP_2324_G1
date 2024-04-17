import threading
import time
import keyboard

# Define events to signal keyboard presses
play_event = threading.Event()
stop_event = threading.Event()
record_event = threading.Event()
stop_record_event = threading.Event()

# Function to listen for keyboard presses
def keyboard_listener():
    while True:
        if keyboard.is_pressed("q"):  # Press 'q' to stop the program
            stop_event.set()
            break
        elif keyboard.is_pressed("p"):  # Press 'p' to play
            play_event.set()
            time.sleep(0.1)  # Sleep to avoid registering multiple events for one key press
            play_event.clear()
        elif keyboard.is_pressed("g"):  # Press 'g' to start recording
            record_event.set()
            time.sleep(0.1)
            record_event.clear()
        elif keyboard.is_pressed("h"):  # Press 'h' to stop recording
            stop_record_event.set()
            time.sleep(0.1)
            stop_record_event.clear()
        time.sleep(0.01)  # Check for key press every 0.01 seconds

# Function for normal mode
def normal_mode():
    print("Normal mode is running...")
    while not stop_event.is_set():
        # Your normal mode logic goes here
        time.sleep(1)

# Function for play mode
def play_mode():
    print("Play mode is running...")
    while not stop_event.is_set():
        # Your play mode logic goes here
        time.sleep(1)

# Function for recording
def record_mode():
    print("Recording mode is running...")
    while not stop_event.is_set():
        # Your recording logic goes here
        time.sleep(1)

# Start the keyboard listener in a separate thread
keyboard_thread = threading.Thread(target=keyboard_listener)
keyboard_thread.daemon = True
keyboard_thread.start()

# Start the main program loop
while not stop_event.is_set():
    if play_event.is_set():
        play_mode_thread = threading.Thread(target=play_mode)
        play_mode_thread.start()
    else:
        normal_mode_thread = threading.Thread(target=normal_mode)
        normal_mode_thread.start()

    if record_event.is_set():
        record_mode_thread = threading.Thread(target=record_mode)
        record_mode_thread.start()

    # Wait for keyboard events
    stop_event.wait()

print("Program stopped.")
