from evdev import InputDevice, ecodes, categorize
# from app.constants import EVENT_X

event_path1 = '/dev/input/by-id/usb-Cypress_Semiconductor_Composite_Device_Demo-event-kbd'
event_path2 = '/dev/input/by-id/usb-SINO_WEALTH_RK_Bluetooth_Keyboard-event-kbd'
 
keyboard1 = InputDevice(event_path1)
keyboard2 = InputDevice(event_path2)

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

    if shift_pressed and key == "KEY_3":  # Corrected the condition here
        keystrokes += '#'
        shift_pressed = False
        return

    if shift_pressed and key == "KEY_8":  # Corrected the condition here
        keystrokes += '*'
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

# Listen for events from both devices
for event1, event2 in zip(keyboard1.read_loop(), keyboard2.read_loop()):
# for event2 in keyboard2.read_loop():
    if event2.type == ecodes.EV_KEY:
        key_event = categorize(event2)
        if key_event.keystate == key_event.key_down:
            on_key_press(key_event.keycode)

    if event1.type == ecodes.EV_KEY:
        key_event = categorize(event1)
        if key_event.keystate == key_event.key_down:
            on_key_press(key_event.keycode)
