import RPi.GPIO as GPIO
import time

output = 3
input_pin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(output, GPIO.OUT)
GPIO.output(output, GPIO.HIGH)
time.sleep(1)

GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def check_input_pin():
    # print(GPIO.input(input_pin))
    # print(GPIO.input(output))
    # print(GPIO.HIGH)
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


# import RPi.GPIO as GPIO
# import time

# OUTPUT_PIN = 3
# INPUT_PIN = 5

# def setup_gpio():
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BOARD)

#     GPIO.setup(OUTPUT_PIN, GPIO.OUT)
#     GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# def unlock_door():
#     GPIO.output(OUTPUT_PIN, GPIO.LOW)

# def lock_door():
#     GPIO.output(OUTPUT_PIN, GPIO.HIGH)

# def check_input_pin():
#     return GPIO.input(INPUT_PIN) == GPIO.LOW

# def main():
#     try:
#         setup_gpio()

#         while True:
#             lock_door()
#             status = check_input_pin()

#             if status:
#                 print("Door locked")
#             else:
#                 unlock_door()
#                 print("Unlocked")

#             time.sleep(0.5)

#     except KeyboardInterrupt:
#         print("Stopped")
#     finally:
#         GPIO.cleanup()

# if __name__ == "__main__":
#     main()