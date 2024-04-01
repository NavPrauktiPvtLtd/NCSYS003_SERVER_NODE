import RPi.GPIO as GPIO
from logger.logger import setup_applevel_logger
from constants import AUTO_LOCK_INTERVAL
from utils import publish_message
from topic import Topic
import time
logger = setup_applevel_logger(__name__,'logs.txt')

class LockController:
    def __init__(self,mqtt_client,relay_room_no):
        self.RELAY_PIN = 23
        self.mqtt_client = mqtt_client 
        self.relay_room_no = relay_room_no

        self.unlocked_seconds = 0 
        self.check_interval = 1
        self.auto_lock_interval = AUTO_LOCK_INTERVAL

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        GPIO.output(self.RELAY_PIN, GPIO.HIGH)

    def is_locked(self):
        return GPIO.input(self.RELAY_PIN) == GPIO.HIGH

    def open(self):
        try:
            # check if the lock is already opened
            if self.is_locked():
                logger.debug("unlocked")
                GPIO.output(self.RELAY_PIN, GPIO.LOW)
                publish_message(
                    self.mqtt_client,
                    Topic.LOCK_STATUS,
                    {"relayRoomNo": self.relay_room_no, "isSuccessful": True},
                    qos=1,
                )
            else:
                logger.debug("already locked")
        except Exception as e:
            logger.error(f"Error unlocking: {e}")

    def close(self):
        try:
            if not self.is_locked():
                logger.debug("locked")
                GPIO.output(self.RELAY_PIN, GPIO.HIGH)
                publish_message(
                self.mqtt_client,
                Topic.LOCK_STATUS,
                {"relayRoomNo": self.relay_room_no, "isSuccessful": False},
                qos=1,
                )
            else: 
                logger.debug("already unlocked")
        except Exception as e:
            logger.error(f"Error locking: {e}")


    
    def run(self):
        try:
            logger.debug('Lock Tracker activated')
            while True:

                if not self.is_locked():
                    self.unlocked_seconds = self.unlocked_seconds + self.check_interval
                    logger.debug(f"unlocked seconds : {self.unlocked_seconds}")

                
                if self.unlocked_seconds == int(self.auto_lock_interval):
                    logger.info(f'autolocking the lock.....')
                    self.close()
                    self.unlocked_seconds = 0 
                
                time.sleep(self.check_interval) 
        except KeyboardInterrupt as err:
            logger.error(err)


     