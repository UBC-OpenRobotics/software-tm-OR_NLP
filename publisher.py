
import paho.mqtt.client as mqtt
import json

# Constants
BROKER_ADDRESS = "localhost"  # Replace with the broker's IP if not local
TOPIC = "robot_commands"
VALID_COMMANDS = ["talk", "move", "turn", "exit"]

def publish_command(command: dict):
    """
    Publishes a command to the MQTT broker.
    Args:
        command (dict): Command to publish in JSON format.
    """
    try:
        client = mqtt.Client()
        client.connect(BROKER_ADDRESS, 1883, 60)
        client.publish(TOPIC, json.dumps(command))  # Convert dict to JSON string
        print(f"Published: {command}")
        client.disconnect()
    except Exception as e:
        print(f"Failed to publish command: {e}")

if __name__ == "__main__":
    print(f"Enter valid robot commands: {', '.join(VALID_COMMANDS)}")
    while True:
        command_type = input("Enter command type (talk, move, turn, exit): ").strip().lower()
        if command_type == "exit":
            publish_command({"command": "exit"})
            print("Exiting...")
            break
        elif command_type == "talk":
            text = input("Enter text for the robot to say: ").strip()
            if text:
                publish_command({"command": "talk", "text": text})
            else:
                print("Invalid input. Text cannot be empty.")
        elif command_type == "move":
            try:
                distance = float(input("Enter distance (meters): ").strip())
                if distance > 0:
                    publish_command({"command": "move", "distance": distance})
                else:
                    print("Distance must be positive.")
            except ValueError:
                print("Invalid input. Please enter a valid number for distance.")
        elif command_type == "turn":
            try:
                angle = float(input("Enter angle (degrees): ").strip())
                publish_command({"command": "turn", "angle": angle})
            except ValueError:
                print("Invalid input. Please enter a valid number for angle.")
        else:
            print(f"Invalid command. Valid commands are: {', '.join(VALID_COMMANDS)}")
