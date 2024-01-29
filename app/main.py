import os
import time
import json

from threading import Thread

from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from topic import Topic
from logger.logger import setup_applevel_logger
from utils import get_data_from_message, publish_message
from simulator import door_sim
from keypad import KeypadController
from utils import read_json_file,write_json_file,generate_absolute_path
from constants import OTP_FILE_PATH,RELAY_ROOM_NO,MQTT_HOST
from door import DoorController
from lock import LockController

load_dotenv()

logger = setup_applevel_logger(__name__)

if not RELAY_ROOM_NO:
    logger.error("Relay Room No not found")
    exit()

if not MQTT_HOST:
    logger.error("MQTT HOST not found")
    exit()


def format_topic_name(x):
    return f"{RELAY_ROOM_NO}-{x}"

class APP:
    def __init__(
        self, relay_room_no, mqtt_host
    ):
        self.client = None
        self.relay_room_no = relay_room_no
        self.mqtt_host = mqtt_host
        self.door_controller = None 
        self.key_controller = None 
        self.lock_controller = None
        # self.mqtt_username = mqtt_username
        # self.mqtt_password = mqtt_password

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to broker")
            publish_message(
                client,
                Topic.NODE_STATE,
                {"relayRoomNo": self.relay_room_no, "isOnline": True},
                qos=1,
            )
            client.subscribe(format_topic_name(Topic.SET_LOCK_CODE))


        else:
            logger.error("Connection failed")

    def on_mqtt_disconnect(self, client, userdata, message):
        logger.info("Disconnected from the broker")

    def on_mqtt_message(self, client, userdata, message):
        logger.info(
            "Message received : " + str(message.payload) + " on " + message.topic
        )

    

    def on_receive_otp(self, client, userdata, message):
        try:
            msgData = get_data_from_message(message)
            if msgData:
                otp = msgData["otp"]

                logger.debug(f"received otp {otp}")

                if otp:
                    previous_otp_data = read_json_file(OTP_FILE_PATH)
                    if previous_otp_data:
                        default_otp = previous_otp_data["default_otp"]
                    new_otp_data = {
                        "current_otp": otp,
                        "default_otp": default_otp
                    }
                    write_json_file(OTP_FILE_PATH,new_otp_data)

            else:
                logger.error("No msg data in set_lock_code message")
        except Exception as err:
            logger.error(err)

    
    def door_state_tracker(self):
        if self.door_controller == None:
            logger.error("Door controller not initialize")
        else:
            self.door_controller.run()

    def start_keypad(self):
        if self.key_controller == None:
            logger.error("Keypad controller not initialize")
        else:
            self.key_controller.run()

    def lock_state_tracker(self):
        if self.lock_controller == None:
            logger.error("Lock controller not initialize")
        else:
            self.lock_controller.run()



    def start(self):
        try:
            self.client = mqtt.Client(self.relay_room_no)
            self.client.will_set(
                Topic.NODE_STATE,
                payload=str(
                    json.dumps({"relayRoomNo": self.relay_room_no, "isOnline": False})
                ),
                qos=2,
            )
            # self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
            self.client.connect(host=self.mqtt_host)
            self.client.on_connect = self.on_mqtt_connect
            self.client.on_disconnect = self.on_mqtt_disconnect
            self.client.on_message = self.on_mqtt_message
            self.client.message_callback_add(
                format_topic_name(Topic.SET_LOCK_CODE), self.on_receive_otp
            )
            self.door_controller = DoorController(self.client,self.relay_room_no)
            self.lock_controller = LockController(self.client,self.relay_room_no)
            self.key_controller = KeypadController(self.client,self.relay_room_no,self.lock_controller)
           
            self.client.loop_forever()
        except Exception as e:
            logger.error(e)
            time.sleep(1)
            self.start()


app = APP(RELAY_ROOM_NO, MQTT_HOST)

t1 = Thread(target=app.start)
t2 = Thread(target=app.door_state_tracker)
t3 = Thread(target=app.lock_state_tracker)
t4 = Thread(target=app.start_keypad)



t1.start()
time.sleep(5)
t2.start()
t3.start()
t4.start()

