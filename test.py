# import paho.mqtt.client as mqtt


# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'test-client')
# client.username_pw_set('nfr-user', 'tGn8e9dDugV4@')
# client.connect('192.168.29.77')

# def on_mqtt_connect(client, userdata, flags, rc ,properties):
#     if rc == 0:
#         print('connected')
#     else:
#         print("not connected")


# def on_mqtt_disconnect(client, userdata, flags, rc ,properties):
#     print("mqtt disconnect")

# client.on_connect = on_mqtt_connect
# client.on_disconnect = on_mqtt_disconnect

# client.loop_forever()
import socket

def check_connection(ip_address, port):
    try:
        # Creating a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Setting a timeout for the connection attempt (adjust as needed)
        s.settimeout(3)  # Timeout set to 3 seconds
        
        # Attempting to connect to the IP address and port
        s.connect((ip_address, port))
        
        # Connection successful
        print(f"Connected to {ip_address}:{port}")
        return True
    except Exception as e:
        # Connection unsuccessful
        print(f"Failed to connect to {ip_address}:{port}. Error: {str(e)}")
        return False
    finally:
        # Always close the socket
        s.close()

# Example usage:
ip_address = '192.168.29.77'
port = 1883  # Change this to the port you want to test connectivity on
result = check_connection(ip_address, port)
print("Connection successful:", result)