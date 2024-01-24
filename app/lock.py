import RPi.GPIO as GPIO
import time
from logger.logger import setup_applevel_logger


logger = setup_applevel_logger(__name__)

class LockController:
    def __init__(self):
        self.RELAY_PIN = 11
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        GPIO.output(self.RELAY_PIN, GPIO.LOW)

    def open(self):
        logger.debug("unlocked")
        GPIO.output(self.RELAY_PIN, GPIO.HIGH)

    def close(self):
        logger.debug("locked")
        GPIO.output(self.RELAY_PIN, GPIO.LOW)
