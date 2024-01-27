import RPi.GPIO as GPIO
import time
from logger.logger import setup_applevel_logger
from utils import publish_message
from topic import Topic
from constants import AUTO_LOCK_INTERVAL


logger = setup_applevel_logger(__name__)


OUTPUT_PIN = 5
INPUT_PIN = 19

class DoorController:
    def __init__(self,mqtt_client,relay_room_no):
        logger.debug('Tracking door state')
        self.OUTPUT_PIN = OUTPUT_PIN
        self.INPUT_PIN = INPUT_PIN
        self.mqtt_client = mqtt_client
        self.relay_room_no = relay_room_no
        self.previous_state = None

        self.unlocked_seconds = 0 
        self.check_interval = 1

        self.auto_lock_interval = AUTO_LOCK_INTERVAL

        self.RELAY_PIN = 23

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.OUTPUT_PIN, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        GPIO.output(self.RELAY_PIN, GPIO.LOW)

    def check_input_pin(self):
        return GPIO.input(self.INPUT_PIN) == GPIO.LOW
    
    def is_locked(self):
        return GPIO.input(self.RELAY_PIN) == GPIO.LOW

    def run(self):
        logger.debug('Tracking door state: r')
        try:
            while True:
                current_state = self.check_input_pin()

                logger.debug(f'is locked: {self.is_locked()}')
                
                

                if self.is_locked():
                    self.unlocked_seconds = self.unlocked_seconds + self.check_interval

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


                if self.unlocked_seconds == int(self.auto_lock_interval):
                    logger('Auto locking...........')
                    GPIO.output(self.RELAY_PIN, GPIO.LOW)
                    self.unlocked_seconds = 0

                time.sleep(self.check_interval)

        except KeyboardInterrupt as err:
            logger.error(err)
