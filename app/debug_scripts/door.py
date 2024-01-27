import RPi.GPIO as GPIO
import time

output = 5
input_pin = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(output, GPIO.OUT)
GPIO.output(output, GPIO.HIGH)
time.sleep(1)

GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def check_input_pin():
    print(GPIO.input(input_pin))
    print(GPIO.input(output))
    print(GPIO.HIGH)
    # if GPIO.input(input_pin) == GPIO.HIGH:
    #     print("unlocked")
        # GPIO.output(output, GPIO.LOW)
    if GPIO.input(input_pin) == GPIO.LOW:
            
        GPIO.output(output, GPIO.HIGH)
        return 1
    else:
        return 0 

try:
    while True:
        GPIO.setup(input_pin, GPIO.IN)  # Set the input pin as input GPIO
        GPIO.output(output, GPIO.LOW)
        status=check_input_pin()
        if(status):
            print("door_locked")
        else:
            print("unlocked")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("stopped")
finally:
    GPIO.cleanup()

check_input_pin()