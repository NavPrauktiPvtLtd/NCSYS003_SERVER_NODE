import os
import time
import json


from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from topic import Topic
from logger.logger import setup_applevel_logger
from utils import get_data_from_message, publish_message


load_dotenv()

logger = setup_applevel_logger(__name__)


RELAY_ID = os.getenv("RELAY_ID")

MQTT_HOST = os.getenv("MQTT_HOST")

MQTT_USERNAME = os.getenv("MQTT_USER")

MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

if not RELAY_ID:
    logger.error("Relay Id not found")
    exit()

if not MQTT_HOST:
    logger.error("MQTT HOST not found")
    exit()

if not MQTT_USERNAME:
    logger.error("MQTT USERNAME not found")
    exit()

if not MQTT_PASSWORD:
    logger.error("MQTT PASSWORD not found")
    exit()


def format_topic_name(x):
    return f"{RELAY_ID}-{x}"




class APP:
    def __init__(
        self, relayId: str, mqtt_host: str, mqtt_username: str, mqtt_password: str
    ):
        self.client = None
        self.relayId = relayId
        self.mqtt_host = mqtt_host
        self.mqtt_username = mqtt_username
        self.mqtt_password = mqtt_password

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to broker")
            publish_message(
                client,
                Topic.NODE_STATE,
                {"relayId": self.relayId, "isOnline": True},
                qos=1,
            )
            client.subscribe(format_topic_name(Topic.SEND_OTP))

        else:
            logger.error("Connection failed")

    def on_mqtt_disconnect(self, client, userdata, message):
        logger.info("Disconnected from the broker")

    def on_mqtt_message(self, client, userdata, message):
        logger.info(
            "Message received : " + str(message.payload) + " on " + message.topic
        )

    

    def on_receive_otp(self, client, userdata, message):
        if not self.playlist_player:
            return
        self.terminate_all_active_media()
        msgData = get_data_from_message(message)
        print(msgData)
        if msgData:
            print("received otp")
        else:
            logger.error("No msg data in set_playlist message")





    def start(self):
        try:
            self.client = mqtt.Client(self.relayId)
            self.client.will_set(
                Topic.NODE_STATE,
                payload=str(
                    json.dumps({"relayId": self.relayId, "isOnline": False})
                ),
                qos=2,
            )
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
            self.client.connect(host=self.mqtt_host)
            self.client.on_connect = self.on_mqtt_connect
            self.client.on_disconnect = self.on_mqtt_disconnect
            self.client.on_message = self.on_mqtt_message
            self.client.message_callback_add(
                format_topic_name(Topic.SEND_OTP), self.on_receive_otp
            )
            
            self.client.loop_forever()
        except Exception as e:
            logger.error(e)
            time.sleep(1)
            self.start()


app = APP(RELAY_ID, MQTT_HOST, MQTT_USERNAME, MQTT_PASSWORD)
app.start()
