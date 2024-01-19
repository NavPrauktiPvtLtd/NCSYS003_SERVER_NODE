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

load_dotenv()

logger = setup_applevel_logger(__name__)


RELAY_ROOM_NO = os.getenv("RELAY_ROOM_NO")

MQTT_HOST = "192.168.29.77"

# MQTT_USERNAME = os.getenv("MQTT_USER")

# MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

if not RELAY_ROOM_NO:
    logger.error("Relay Room No not found")
    exit()

if not MQTT_HOST:
    logger.error("MQTT HOST not found")
    exit()

# if not MQTT_USERNAME:
#     logger.error("MQTT USERNAME not found")
#     exit()

# if not MQTT_PASSWORD:
#     logger.error("MQTT PASSWORD not found")
#     exit()


def format_topic_name(x):
    return f"{RELAY_ROOM_NO}-{x}"




class APP:
    def __init__(
        self, relay_room_no: str, mqtt_host: str
    ):
        self.client = None
        self.relay_room_no = relay_room_no
        self.mqtt_host = mqtt_host
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
        msgData = get_data_from_message(message)
        print(msgData)
        if msgData:
            logger.debug("received otp")
        else:
            logger.error("No msg data in set_lock_code message")

    
    def start_door_sim(self):
        door_sim(self.client,self.relay_room_no)


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
           
            self.client.loop_forever()
        except Exception as e:
            logger.error(e)
            time.sleep(1)
            self.start()


app = APP(RELAY_ROOM_NO, MQTT_HOST)

t1 = Thread(target=app.start)
t2 = Thread(target=app.start_door_sim)
t1.start()
t2.start()
