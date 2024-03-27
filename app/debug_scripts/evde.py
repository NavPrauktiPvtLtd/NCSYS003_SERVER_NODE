from evdev import InputDevice, ecodes, categorize
# from app.constants import EVENT_X

event_path = '/dev/input/by-path/pci-0000:01:00.0-usb-0:2:1.0-event-kbd'
 
keyboard = InputDevice(event_path)



shift_pressed = False 

keystrokes = ''

def on_key_press(key):
    print(key)
    global keystrokes, shift_pressed

    if key == "KEY_ENTER":
        if keystrokes == "#123#":
            print("CODE PRESSED")
        keystrokes = '' 

    if key == "KEY_LEFTSHIFT" or key == "KEY_RIGHTSHIFT":
         shift_pressed = True 
         return

    if shift_pressed and "KEY_3":
         keystrokes = keystrokes + '#'
         shift_pressed = False 
         return

    if shift_pressed and "KEY_8":
         keystrokes = keystrokes + '*'
         shift_pressed = False  
         return
    
    if key == "KEY_BACKSPACE":
        keystrokes = keystrokes[:-1]
        return
    
    if key == "KEY_1":
        keystrokes += '1'
    elif key == "KEY_2":
        keystrokes += '2'
    elif key == "KEY_3":
        keystrokes += '3'
    elif key == "KEY_4":
        keystrokes += '4'
    elif key == "KEY_5":
        keystrokes += '5'
    elif key == "KEY_6":
        keystrokes += '6'
    elif key == "KEY_7":
        keystrokes += '7'
    elif key == "KEY_8":
        keystrokes += '8'
    elif key == "KEY_9":
        keystrokes += '9'
    elif key == "KEY_0":
        keystrokes += '0'
    elif key == "KEY_DOT":
        keystrokes += '.'

    shift_pressed = False
    print(keystrokes)

# Listen for events
for event in keyboard.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keystate == key_event.key_down:
            # if key_event.keycode in target_keys:
                on_key_press(key_event.keycode)