
from pynput.keyboard import Key, Listener
import paho.mqtt.client as mqtt
from topic import Topic
from utils import publish_message
from logger.logger import setup_applevel_logger
import re
 
logger = setup_applevel_logger(__name__,'log.txt')

# q - open door
# w - close door 
# a - lock 
# s - unlock



def show(key,client,relay_room_no):

    if str(key) == "'q'":
        logger.info("Sending door open")
        publish_message(
            client,
            Topic.DOOR_STATUS,
            {"relayRoomNo": relay_room_no, "isOpened": True},
            qos=1,
        )

    if str(key) == "'w'":
        publish_message(
            client,
            Topic.DOOR_STATUS,
            {"relayRoomNo": relay_room_no, "isOpened": False},
            qos=1,
        )

    if str(key) == "'a'":
        publish_message(
            client,
            Topic.LOCK_STATUS,
            {"relayRoomNo": relay_room_no, "isSuccessful": True},
            qos=1,
        )


    if str(key) == "'s'":
        publish_message(
            client,
            Topic.LOCK_STATUS,
            {"relayRoomNo": relay_room_no, "isSuccessful": False},
            qos=1,
        )
    
    


def door_sim(client,relay_room_no):
    logger.info("Door simulator started")
    # Collect all event until released
    with Listener(on_press=lambda key: show(key, client,relay_room_no)) as listener:
    # with Listener(on_press = show) as listener: 
        listener.join()

    