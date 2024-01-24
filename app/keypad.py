from pynput.keyboard import Listener, Key
from logger.logger import setup_applevel_logger

logger = setup_applevel_logger(__name__)

class KeypadController:
    def __init__(self,mqtt_client):
        self.activation_code = '#123#'
        self.keystrokes = ''
        self.activation_code_pressed = False
        self.mqtt_client = mqtt_client
        self.otp_length = 6

    def run(self):
        logger.debug("listening for keystrokes.....")
        with Listener(on_press=self.on_keypress) as listener:
            listener.join()

    def clear(self):
        logger.debug("clearing keystrokes")
        self.keystrokes = ''

    def on_keypress(self,key):
        try:
            key = key.char
        except AttributeError:
            pass
        
        logger.debug(f"{key} is pressed")

        if key == Key.shift:
            return

        if key == Key.enter:
            self.handle_enter_press()
            return
        
        if key == Key.backspace:
            self.handle_backspace_press()
            return

        self.keystrokes = self.keystrokes + key
        

    def handle_enter_press(self):
        logger.debug(f"enter pressed with {self.keystrokes}")
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
        logger.debug(f"OTP: {otp} received")










