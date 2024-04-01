from logger.logger import setup_applevel_logger
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os
import socket

load_dotenv()

logger = setup_applevel_logger(__name__,'logs.txt')


def generate_absolute_path(relative_path):
    current_directory = os.getcwd()
    absolute_path = os.path.abspath(os.path.join(current_directory, relative_path))
    return absolute_path

def publish_message(client: mqtt.Client, topic: str, message, qos=0):
    if not client:
        logger.error('Mqtt client is None')
        return
    try:
        client.publish(topic, str(json.dumps(message)), qos=qos)
        logger.info(f"Published: {message}")
    except Exception as e:
        logger.error(e)


def get_data_from_message(message):
    try:
        data_str = str(message.payload.decode("utf-8"))
        return json.loads(data_str)
    except Exception as e:
        logger.error(e)


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def check_and_create_file(file_path, initial_content=None):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            if initial_content:
                logger.info(f"Initial content: '{initial_content}'")
                file.write(initial_content)
        logger.info(f"File '{file_path}' created.")
    else:
        logger.info(f"File '{file_path}' already exists.")

def check_connection(ip_address, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip_address, port))
        logger.info(f"Connected to {ip_address}:{port}")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to {ip_address}:{port}. Error: {str(e)}")
        return False
    finally:
        s.close()


