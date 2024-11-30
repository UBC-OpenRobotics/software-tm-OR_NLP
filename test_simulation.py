import time
from publisher import publish_command  # Assuming the publisher script is named `publisher.py`

# Simulated commands
commands = [
    {"command": "talk", "text": "Hello!"},
    {"command": "move", "distance": 3.5},
    {"command": "turn", "angle": 90},
    {"command": "exit"}
]

print("Starting automated command testing...")
for cmd in commands:
    publish_command(cmd)
    time.sleep(1)  # Simulate a delay between commands
print("Test completed.")
