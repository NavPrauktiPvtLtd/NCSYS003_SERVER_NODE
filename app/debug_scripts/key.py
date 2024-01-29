import keyboard

def listen_for_numbers_and_enter():
    numbers = set(map(str, range(10)))  # Set of numeric keys as strings

    def on_keypress(event):
        if event.event_type == keyboard.KEY_DOWN:  # Check for key press event
            key = event.name

            print(key)

            # key == 'enter':
            # print("Enter key pressed")

    # Set up the keyboard hook
    keyboard.hook(on_keypress)

    # Keep the script running
    keyboard.wait('esc')  # Wait for the 'esc' key to exit the script

# Run the function
listen_for_numbers_and_enter()