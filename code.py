import time
import board
import keypad
import storage
import digitalio
from circuitPyHuskyLib import HuskyLensLibrary

## Commented out for Debugging, uncomment for final build
storage.remount("/", readonly = False)

## Functions

# CameraOperations:
def check_camera():
    global unlock_state
    
    results = hl.learned()
    if results: # if result not empty
        print(f"Detected face count: {len(results)}")
        unlock_state = not unlock_state
        if unlock_state:
            play_music()
    else:
        led.value = False

def learn_new_face():
    num = hl.learnedObjCount() + 1
    results = hl.learn(num)
    print(f"Learned new face number {num}")

def forget_faces():
    hl.forget()
    print("Faces cleared")

# CodeOperations:
def load_code_from_file(filename="passcode.txt"):
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except OSError:
        # File doesn't exist yet
        return None
    
def save_code_to_file(code, filename="passcode.txt"):
    with open(filename, "w") as file:
        file.write(code)

def load_door_time_from_file(filename="door_timer.txt"):
    try:
        with open(filename, "r") as file:
            return  file.read().strip()
    except OSError:
        # File doesn't exist yet
        return None
def save_door_timer_to_file(time, filename="door_timer.txt"):
    with open(filename, "w") as file:
        file.write(time)

# DoorOperations:
def open_door():
    print("Door Opening")
    polarity_switch.value = False
    main_power.value = True
    wait_function()
    main_power.value = False
    global door_state
    door_state = True
    print("Door Opened")

def close_door():
    print("Door Closing")
    polarity_switch.value = True
    main_power.value = True
    wait_function()
    main_power.value = False
    global door_state
    door_state = False
    print("Door Closed")

def success_buzz():
    buzzer.value = True
    time.sleep(.25)
    buzzer.value = False
    time.sleep(.25)
    buzzer.value = True
    time.sleep(.25)
    buzzer.value = False
    time.sleep(.25)
    buzzer.value = True
    time.sleep(1)
    buzzer.value = False

def failed_buzz():
    buzzer.value = True
    time.sleep(.3)
    buzzer.value = False
    time.sleep(.3)
    buzzer.value = True
    time.sleep(.3)
    buzzer.value = False

def play_music():
    print("Playing Music")
    music.value = False
    time.sleep(.25)
    music.value = True

def wait_function():
    print(f"Time: {door_timer}")
    for i in range(int(door_timer)):
        print(f".")
        led.value = not led.value
        time.sleep(1)

# KeypadOperations:
def scan_key():
    event = km.events.get()
    if event and event.pressed:
        print("Pressed:", keys[event.key_number])
        buzzer.value = True
        time.sleep(.1)
        buzzer.value = False
        return keys[event.key_number]
    return None

# DoorLogic:
def keypress_logic():
    global code
    global unlock_state
    
    last_key = scan_key()
    if last_key == '*' or last_key == '#':
        if code == mastercode and unlock_state:
            set_new_code()
        elif code == learn_face: #and unlock_state:
            learn_new_face()
        elif code == forget_face: #and unlock_state:
            forget_faces()
        elif code == door_timer_code: #and unlock_state:
            set_new_door_time()
        elif code == door_code:
            unlock_state = not unlock_state
            success_buzz()
        else:
            failed_buzz()
            
        code = ""
    elif last_key != None:
        code = code + last_key

def set_new_code():
    buzzer.value = True
    time.sleep(5)
    buzzer.value = False
    new_code = ""
    changing_code = True
    
    while changing_code:
        last_key = scan_key()
        if last_key == '*' or last_key == '#':
            if len(new_code) >= 3:
                save_code_to_file(new_code)
                changing_code = False
                door_code = load_code_from_file()
            else:
                buzzer.value = True
                time.sleep(.5)
                buzzer.value = False
                new_code = ""
        if last_key != None:
            new_code = new_code + last_key

def set_new_door_time():
    buzzer.value = True
    time.sleep(3)
    buzzer.value = False
    new_time = ""
    changing_code = True
    
    while changing_code:
        last_key = scan_key()
        if last_key == '*' or last_key == '#':
            if len(new_time) == 2:
                save_door_timer_to_file(new_time)
                changing_code = False
                new_time = load_door_time_from_file()
            else:
                failed_buzz()
                new_time = ""
        if last_key != None:
            new_time = new_time + last_key

## Pin setup
main_power = digitalio.DigitalInOut(board.GP12)
main_power.direction = digitalio.Direction.OUTPUT

buzzer = digitalio.DigitalInOut(board.GP10)
buzzer.direction = digitalio.Direction.OUTPUT

music = digitalio.DigitalInOut(board.GP26)
music.direction = digitalio.Direction.OUTPUT
music.value = True

polarity_switch = digitalio.DigitalInOut(board.GP28)
polarity_switch.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

## AI Camera
hl = HuskyLensLibrary('UART', TX=board.GP0, RX=board.GP1)

## Variables
door_timer = load_door_time_from_file()
print(f"Timeset: {door_timer}")
mastercode = "9876543210"
learn_face = "55555" # '5' Five times
forget_face = "666666" # '6' Six times
door_timer_code = "7777777"# '7' Seven times

unlock_state = False # True is unlocked, False is locked
door_state = False # True is open, False is closed
door_code = load_code_from_file()
print(f"Stored code:{door_code}")

code = ""

km = keypad.KeyMatrix(
   row_pins=(board.GP3, board.GP9, board.GP8, board.GP5),
   column_pins=(board.GP4, board.GP2, board.GP7)
)

# Key map
keys = [
   "1","2","3",
   "4","5","6",
   "7","8","9",
   "*","0","#"
]

# Main Function
while True:
    keypress_logic()
    
    # Check the AI Camera for the face
    check_camera()
    time.sleep(.25)
    #print(f"unlock_state: {unlock_state}, door_state: {door_state}")
    if unlock_state != door_state:
        if unlock_state:
            open_door()
        else:
            close_door()

