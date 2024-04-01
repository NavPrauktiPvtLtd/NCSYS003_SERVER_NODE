import keyboard
from logger.logger import setup_applevel_logger
from utils import read_json_file,write_json_file
from constants import OTP_FILE_PATH,ACTIVATION_CODE

logger = setup_applevel_logger(__name__,'logs.txt')

OTP_LENGTH = 6

# class KeypadController:
#     def __init__(self,mqtt_client,relay_room_no,lock_controller):
#         try:
#             self.activation_code = ACTIVATION_CODE 
#             self.keystrokes = ''
#             self.activation_code_pressed = False
#             self.relay_room_no = relay_room_no
#             self.mqtt_client = mqtt_client
#             self.otp_length = OTP_LENGTH
#             self.otp_file_path = OTP_FILE_PATH 
#             self.lock_controller = lock_controller
#             self.shift_pressed = False
#         except Exception as e: 
#             logger.error(e)




#     def clear(self):
#         self.keystrokes = ''

#     def on_key_event(self,e):
#         key_pressed = ''
#         if e.event_type == keyboard.KEY_DOWN:
#             if e.name == 'shift':
#                 self.shift_pressed = True
#                 return
#             self.shift_pressed = False

#             if e.name == 'enter':
#                 self.handle_enter_press()
#                 return
#             if e.name == 'backspace':
#                 self.handle_backspace_press()
#                 return
           
#             if self.shift_pressed and e.name == '3':
#                 key_pressed = '#'
#             else:
#                 key_pressed = e.name

#         self.keystrokes = self.keystrokes + key_pressed
        
#     def run(self):
#         logger.debug("Keypad activated")
#         keyboard.hook(self.on_key_event)
#         keyboard.wait() 

#     def handle_enter_press(self):
#         logger.debug(f"Enter pressed: {self.keystrokes}")
#         # check if activation code is already pressed and ketstrokes matches the otp length
#         if self.activation_code_pressed and len(self.keystrokes) == self.otp_length:
#             # this means this is the otp
#             self.handle_otp(self.keystrokes)
#             self.clear()
#             return
#         # check if activation code is pressed 
#         if self.keystrokes == self.activation_code:
#             logger.debug(f"Activation code pressed")
#             self.activation_code_pressed = True
#             self.clear()
#         else: 
#             self.activation_code_pressed = False
#         self.clear()

#     def handle_backspace_press(self):
#         # remove the last character from the string
#         if self.keystrokes:
#             result_string = self.keystrokes[:-1]
#             self.keystrokes=result_string

    
#     def handle_otp(self,otp):
#         otp_file_data = read_json_file(self.otp_file_path)
#         entry_otp = otp_file_data["entry_otp"]
#         exit_otp = otp_file_data["exit_otp"]
#         default_otp = otp_file_data["default_otp"]


#         if entry_otp == otp: 
#             logger.debug(f"OTP matched : {otp}")
#             logger.debug(f"Unlocking....")
#             self.lock_controller.open()
#             previous_otp_data = read_json_file(OTP_FILE_PATH)
#             if previous_otp_data:
#                 default_otp = previous_otp_data["default_otp"]
#                 exit_otp = previous_otp_data["exit_otp"]
#             new_otp_data = {
#                 "exit_otp": exit_otp,
#                 "entry_otp": "",
#                 "default_otp": default_otp
#             }
#             logger.debug("clearing previous entry otp")
#             write_json_file(OTP_FILE_PATH,new_otp_data)
#             return 

#         if exit_otp == otp: 
#             logger.debug(f"OTP matched : {otp}")
#             logger.debug(f"Unlocking....")
#             self.lock_controller.open()
#             previous_otp_data = read_json_file(OTP_FILE_PATH)
#             if previous_otp_data:
#                 default_otp = previous_otp_data["default_otp"]
#                 entry_otp = previous_otp_data["entry_otp"]
#             new_otp_data = {
#                 "exit_otp": "",
#                 "entry_otp": entry_otp,
#                 "default_otp": default_otp
#             }
#             logger.debug("clearing previous exit otp")
#             write_json_file(OTP_FILE_PATH,new_otp_data)
#             return 

#         if default_otp == otp: 
#             logger.debug(f"OTP matched : {otp}")
#             logger.debug(f"Unlocking....")
#             self.lock_controller.open()
#             return

#         logger.debug(f"Wrong otp received: {otp}")





