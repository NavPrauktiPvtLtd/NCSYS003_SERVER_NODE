from dotenv import load_dotenv
import os

load_dotenv()

# OTP_FILE_PATH = generate_absolute_path('app/otp.json')
OTP_FILE_PATH = '/home/pi/nfr/NCSYS003_SERVER_NODE/app/otp.json'

RELAY_ROOM_NO = os.getenv("RELAY_ROOM_NO")

MQTT_HOST = os.getenv("MQTT_HOST")

MQTT_USERNAME = os.getenv("MQTT_USERNAME")

MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

ACTIVATION_CODE = os.getenv("ACTIVATION_CODE")

AUTO_LOCK_INTERVAL = os.getenv("AUTO_LOCK_INTERVAL")

DEFAULT_OTP = os.getenv("DEFAULT_OTP")

KEYBOARD_1_EVENT_X = os.getenv("KEYBOARD_1_EVENT_X")

KEYBOARD_2_EVENT_X = os.getenv("KEYBOARD_2_EVENT_X")