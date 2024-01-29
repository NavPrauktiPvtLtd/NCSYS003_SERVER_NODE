from pynput.keyboard import Listener, Key
from topic import Topic
from logger.logger import setup_applevel_logger
from utils import publish_message, read_json_file
from constants import OTP_FILE_PATH,ACTIVATION_CODE

logger = setup_applevel_logger(__name__)

OTP_LENGTH = 6

class KeypadController:
    def __init__(self,mqtt_client,relay_room_no,lock_controller):
        try:
            self.activation_code = ACTIVATION_CODE 
            self.keystrokes = ''
            self.activation_code_pressed = False
            self.relay_room_no = relay_room_no
            self.mqtt_client = mqtt_client
            self.otp_length = OTP_LENGTH
            self.otp_file_path = OTP_FILE_PATH 
            self.lock_controller = lock_controller
        except Exception as e: 
            logger.error(e)

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
        otp_file_data = read_json_file(self.otp_file_path)
        current_otp = otp_file_data["current_otp"]
        default_otp = otp_file_data["default_otp"]

        otp_matched = False 

        if current_otp == otp or default_otp == otp: 
            otp_matched = True
            

        if otp_matched:
            logger.debug(f"OTP matched : {otp}")
            logger.debug(f"Unlocking....")
            self.lock_controller.open()
        else:
            logger.debug(f"OTP not matched : {otp}")

        logger.debug(f"OTP: {otp} received")











