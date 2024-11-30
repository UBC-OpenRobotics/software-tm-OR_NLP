
"""this file listens to commands of a specific MQTT topic.
    This allows us to simulate or send commands to a robot
    or any MQTT subscriber listening to that topic."""



import paho.mqtt.client as mqtt
import json

# Constants
BROKER_ADDRESS = "localhost"  # Replace with an IP if the broker is remote
TOPIC = "robot_commands"

def on_message(client, userdata, msg):
    """
    Callback function triggered when a message is received.
    Args:
        client: The MQTT client instance.
        userdata: User-defined data passed to callbacks.
        msg: The MQTT message.
    """
    try:
        command = json.loads(msg.payload.decode())  # Decode and parse JSON payload
        print(f"Received command: {command}")
        
        # Process the command
        if command.get("command") == "talk":
            print(f"Robot says: {command.get('text', 'No text provided.')}")
        elif command.get("command") == "move":
            print(f"Robot moves {command.get('distance', 0)} meters.")
        elif command.get("command") == "turn":
            print(f"Robot turns {command.get('angle', 0)} degrees.")
        elif command.get("command") == "exit":
            print("Received exit command. Shutting down...")
            client.disconnect()  # Graceful shutdown
        else:
            print("Unknown command received.")
    except json.JSONDecodeError as e:
        print(f"Invalid message format: {e}")

def start_subscriber():
    """
    Starts the MQTT subscriber.
    """
    try:
        client = mqtt.Client()
        client.connect(BROKER_ADDRESS, 1883, 60)  # Connect to the MQTT broker
        client.subscribe(TOPIC)                  # Subscribe to the topic
        client.on_message = on_message           # Set the message callback
        print("Listening for commands...")
        client.loop_forever()                    # Block and listen for messages
    except Exception as e:
        print(f"Subscriber error: {e}")

if __name__ == "__main__":
    start_subscriber()

