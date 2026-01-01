import time
import board
import storage
import digitalio
import doorFunctionLib
from circuitPyHuskyLib import HuskyLensLibrary

# Commented out for Debugging, uncomment for final build
#storage.remount("/", readonly = False)

# Pin setup
main_power = digitalio.DigitalInOut(board.GP12)
main_power.direction = digitalio.Direction.OUTPUT

buzzer = digitalio.DigitalInOut(board.GP10)
buzzer.direction = digitalio.Direction.OUTPUT

polarity_switch = digitalio.DigitalInOut(board.GP28)
polarity_switch.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# AI Camera
hl = HuskyLensLibrary('UART', TX=board.GP0, RX=board.GP1)

# Variables
door_timer = 12
mastercode = "9876543210"
learn_face = "55555"
unlock_state = False # True is unlocked, False is locked
door_state = False # True is open, False is closed
door_code = load_code_from_file()
print("Stored code:", door_code)
code = ""

# Functions

# Main Function
while True:
    keypress_logic()
    
    #Check the AI Camera for the face
    check_camera()
    time.sleep(.25)
    #print(f"unlock_state: {unlock_state}, door_state: {door_state}")
    if unlock_state != door_state:
        if unlock_state:
            open_door()
        else:
            close_door()
