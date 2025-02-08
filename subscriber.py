
"""this file listens to commands of a specific MQTT topic.
    This allows us to simulate or send commands to a robot
    or any MQTT subscriber listening to that topic."""



import paho.mqtt.client as mqtt
import json
from stateful_implementation import StateMachine  # Import FSM class

# Constants
BROKER_ADDRESS = "localhost"
TOPIC = "robot_commands"

def on_message(client, userdata, msg):
    """Receives MQTT commands and forwards them to the FSM."""
    try:
        command = json.loads(msg.payload.decode())
        print(f"Received command: {command}")

        # Forward command to FSM
        process_command_in_fsm(command)

    except json.JSONDecodeError as e:
        print(f"Invalid message format: {e}")

def process_command_in_fsm(command):
    """Passes the command to the FSM for execution."""
    fsm = StateMachine.load_existing_fsm()  # Load or initialize FSM
    fsm.process_command(command)  # FSM handles the command

def start_subscriber():
    """Starts the MQTT subscriber and listens for commands."""
    try:
        client = mqtt.Client()
        client.connect(BROKER_ADDRESS, 1883, 60)
        client.subscribe(TOPIC)
        client.on_message = on_message
        print("Listening for commands...")
        client.loop_forever()
    except Exception as e:
        print(f"Subscriber error: {e}")

if __name__ == "__main__":
    start_subscriber()
