# Hidden Door Lock Project

## How to Operate
The code to operate this lock will be stored on the device in the "passcode.txt" file. If you ever forget the code, simply plug the Pi into a computer, view the Pi as a device and read the contents of the file.

### To unlock and open the door:
- Have a registered face enter the camera's view

    OR

- Enter the passcode followed by the * or # keys

### To lock and close the door:
- Have a registered face enter the camera's view

    OR
- Press the * or # keys

### To Train the Face Detection
- While the door is unlocked and the desired face is in front of the camera:
  - Press "55555" (5 five times) and wait for a noise to indicate success

### To Forget All Faces
- While the door is unlocked:
  - Press "666666" (6 six times) and wait for a noise to indicate success
  
### To Reset the Door Code (MasterCode):
- Key in the code "987654321911"

## Hardware
- Pi Pico
- HuskyLens "AI" Tracker
- 3x4 - 7 Pin Keypad
- Armature
- DPDT Relay to invert polarity
- SPDT Relay to cut power

## Software Structure


## License
MIT: https://mit-license.org/

## Contact
For Software Visit: https://github.com/joshuapeterson4/Hidden-Door-Lock

Created by Josh Peterson(joshuapeterson2019@gmail.com)