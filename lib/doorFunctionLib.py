import time
import board
import keypad
import storage
import digitalio
from circuitPyHuskyLib import HuskyLensLibrary

class CameraOperations:
    def check_camera():
        global unlock_state
        
        results = hl.blocks() # Get All type=BLOCK result
        
        if results: # if result not empty
            print(f"Detected face count: {len(results)}")
            unlock_state = not unlock_state
        else:
            led.value = False
class CodeOperations:
    # Load Passcode
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

class DoorOperations:
    def open_door():
        print("Door Opening")
        polarity_switch = False
        main_power = True
        wait_function(door_timer)
        main_power = False
        global door_state
        door_state = True
        print("Door Opened")
    
    def close_door():
        print("Door Closing")
        polarity_switch = True
        main_power = True
        wait_function(door_timer)
        main_power = False
        global door_state
        door_state = False
        print("Door Closed")
        
    def wait_function(wait):
        for i in range(wait):
            print(f".")
            led.value = not led.value
            buzzer.value = True
            time.sleep(.5)
            buzzer.value = False
            time.sleep(.5)

class KeypadOperations:
    def init_keypad():
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
    
    def scan_key():
        event = km.events.get()
        if event and event.pressed:
            print("Pressed:", keys[event.key_number])
            buzzer.value = True
            time.sleep(.1)
            buzzer.value = False
            return keys[event.key_number]
        return None

class DoorLogic:
    def keypress_logic():
        global code
        global unlock_state
        
        last_key = scan_key()
        if last_key == '*' or last_key == '#':
            if code == mastercode:
                set_new_code()
            #elif code == learn_face:
                
            elif code == door_code:
                unlock_state = not unlock_state
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
                    time.sleep(1)
                    buzzer.value = False
                    new_code = ""
            if last_key != None:
                new_code = new_code + last_key
