from pynput.keyboard import Listener, Key
from logger.logger import setup_applevel_logger

logger = setup_applevel_logger(__name__)

    
# def handle_backspace(input_string):
#     if input_string:
#         result_string = input_string[:-1]
#         return result_string
#     else:
#         return ''


# activation_code = '#123#'

# keystrokes = ''

# listening_otp = False

# def handle_code(code):
#     global listening_otp
#     if listening_otp == True: 
#         print(f'Otp received: {code}')
#         listening_otp = False
#         return 

#     if code == activation_code:
#         print('activation code pressed.... Listening for OTP')
#         listening_otp = True
#         return


# def show(key):
#     try:
#         key = key.char
#     except AttributeError:
#         pass

#     global keystrokes
#     if key == Key.shift:
#         return

#     if key == Key.enter:
#         handle_code(keystrokes)
#         keystrokes = ''
#         return
    
#     if key == Key.backspace:
#         # remove the last char from the global var 
#         keystrokes = handle_backspace(keystrokes)
#         print(keystrokes)
#         return

#     keystrokes = keystrokes + key
#     print(keystrokes)






class KEYPAD_LOCK:
    def __init__(self,mqtt_client,debug=True):
        self.activation_code = '#123#'
        self.keystrokes = ''
        self.activation_code_pressed = False
        self.mqtt_client = mqtt_client
        self.otp_length = 6
        self.debug = debug


    def run(self):
        self.debug_logger("listening for keystrokes.....")
        with Listener(on_press=self.on_keypress) as listener:
            listener.join()

    def debug_logger(self,message):
        if self.debug:
            print(message)

    def clear(self):
        self.debug_logger("clearing keystrokes")
        self.keystrokes = ''

    def on_keypress(self,key):
        try:
            key = key.char
        except AttributeError:
            pass
        
        self.debug_logger(f"{key} is pressed")

        if key == Key.shift:
            return

        if key == Key.enter:
            self.handle_enter_press()
            return
        
        if key == Key.backspace:
            self.handle_backspace_press()
            return

        self.keystrokes = self.keystrokes + key
        pass

    def handle_enter_press(self):
        self.debug_logger(f"enter pressed with {self.keystrokes}")
        # check if activation code is already pressed and ketstrokes matches the otp length
        if self.activation_code_pressed and len(self.keystrokes) == self.otp_length:
            # this means this is the otp
            self.handle_otp(self.keystrokes)
            self.clear()
            return
        # check if activation code is pressed 
        if self.keystrokes == self.activation_code:
            self.activation_code_pressed = True
            self.clear()
        else: 
            self.activation_code_pressed = False
        self.clear()

    def handle_backspace_press(self):
        # remove the last character from the string
        if self.keystrokes:
            result_string = self.keystrokes[:-1]
            return result_string
        else:
            return ''

    def handle_otp(self,otp):
        self.debug_logger(f"OTP: {otp} received")
        pass




