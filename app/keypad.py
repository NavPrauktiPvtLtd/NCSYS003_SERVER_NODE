from evdev import InputDevice, ecodes, categorize
from logger.logger import setup_applevel_logger
from utils import read_json_file,write_json_file
from constants import OTP_FILE_PATH,ACTIVATION_CODE,EVENT_X

logger = setup_applevel_logger(__name__,'log.txt')

OTP_LENGTH = 6

event_path = EVENT_X

keyboard = InputDevice(event_path)

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
        logger.debug("Keypad activated")
        for event in keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                        self.on_keypress(key_event.keycode)
    def clear(self):
        self.keystrokes = ''

    def on_keypress(self,key):
        logger.debug(f'key pressed {key}')
        if key == "KEY_ENTER":
            self.handle_enter_press()
            return 

        if key == "KEY_LEFTSHIFT" or key == "KEY_RIGHTSHIFT":
            self.shift_pressed = True 
            return

        if self.shift_pressed and key == "KEY_3":
            self.keystrokes = self.keystrokes + '#'
            self.shift_pressed = False 
            return

        if self.shift_pressed and key == "KEY_8":
            self.keystrokes = self.keystrokes + '*'
            self.shift_pressed = False  
            return
        
        if key == "KEY_BACKSPACE":
            self.handle_backspace_press()
            return
        
        if key == "KEY_1":
            self.keystrokes += '1'
        elif key == "KEY_2":
            self.keystrokes += '2'
        elif key == "KEY_3":
            self.keystrokes += '3'
        elif key == "KEY_4":
            self.keystrokes += '4'
        elif key == "KEY_5":
            self.keystrokes += '5'
        elif key == "KEY_6":
            self.keystrokes += '6'
        elif key == "KEY_7":
            self.keystrokes += '7'
        elif key == "KEY_8":
            self.keystrokes += '8'
        elif key == "KEY_9":
            self.keystrokes += '9'
        elif key == "KEY_0":
            self.keystrokes += '0'
        elif key == "KEY_DOT":
            self.keystrokes += '.'

        self.shift_pressed = False
        

    def handle_enter_press(self):
        logger.debug(f"Enter pressed: {self.keystrokes}")
        # check if activation code is already pressed and keystrokes matches the otp length
        if self.activation_code_pressed and len(self.keystrokes) == self.otp_length:
            # this means this is the otp
            self.handle_otp(self.keystrokes)
            self.clear()
            return
        # check if activation code is pressed 
        if self.keystrokes == self.activation_code:
            logger.debug(f"Activation code pressed")
            self.activation_code_pressed = True
            self.clear()
        else: 
            self.activation_code_pressed = False
        self.clear()

    def handle_backspace_press(self):
        # remove the last character from the string
        if self.keystrokes:
            result_string = self.keystrokes[:-1]
            self.keystrokes=result_string

    def handle_otp(self,otp):
        otp_file_data = read_json_file(self.otp_file_path)
        entry_otp = otp_file_data["entry_otp"]
        exit_otp = otp_file_data["exit_otp"]
        default_otp = otp_file_data["default_otp"]


        if entry_otp == otp: 
            logger.debug(f"OTP matched : {otp}")
            logger.debug(f"Unlocking....")
            self.lock_controller.open()
            previous_otp_data = read_json_file(OTP_FILE_PATH)
            if previous_otp_data:
                default_otp = previous_otp_data["default_otp"]
                exit_otp = previous_otp_data["exit_otp"]
            new_otp_data = {
                "exit_otp": exit_otp,
                "entry_otp": "",
                "default_otp": default_otp
            }
            logger.debug("clearing previous entry otp")
            write_json_file(OTP_FILE_PATH,new_otp_data)
            return 

        if exit_otp == otp: 
            logger.debug(f"OTP matched : {otp}")
            logger.debug(f"Unlocking....")
            self.lock_controller.open()
            previous_otp_data = read_json_file(OTP_FILE_PATH)
            if previous_otp_data:
                default_otp = previous_otp_data["default_otp"]
                entry_otp = previous_otp_data["entry_otp"]
            new_otp_data = {
                "exit_otp": "",
                "entry_otp": entry_otp,
                "default_otp": default_otp
            }
            logger.debug("clearing previous exit otp")
            write_json_file(OTP_FILE_PATH,new_otp_data)
            return 

        if default_otp == otp: 
            logger.debug(f"OTP matched : {otp}")
            logger.debug(f"Unlocking....")
            self.lock_controller.open()
            return

        logger.debug(f"Wrong otp received: {otp}")












