import RPi.GPIO as GPIO
import time
from logger.logger import setup_applevel_logger
from utils import publish_message
from topic import Topic


logger = setup_applevel_logger(__name__,'log.txt')


OUTPUT_PIN = 5
INPUT_PIN = 19

class DoorController:
    def __init__(self,mqtt_client,relay_room_no):
        self.OUTPUT_PIN = OUTPUT_PIN
        self.INPUT_PIN = INPUT_PIN
        self.mqtt_client = mqtt_client
        self.relay_room_no = relay_room_no
        self.previous_state = None

        self.check_interval = 1

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.OUTPUT_PIN, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def check_input_pin(self):
        return GPIO.input(self.INPUT_PIN) == GPIO.LOW
    
    def run(self):
        logger.debug('Door tracking activated')
        try:
            while True:
                current_state = self.check_input_pin()

                # intital value set
                if self.previous_state == None:
                    self.previous_state = current_state

                # we will only state the status to server if there is a change
                if current_state != self.previous_state:
                    logger.debug('Door state changed')
                    publish_message(
                        self.mqtt_client,
                        Topic.DOOR_STATUS,
                        {"relayRoomNo": self.relay_room_no, "isOpened": current_state},
                        qos=1,
                    )

                self.previous_state = current_state

                time.sleep(self.check_interval)

        except KeyboardInterrupt as err:
            logger.error(err)
