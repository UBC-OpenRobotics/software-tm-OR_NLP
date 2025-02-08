from gptcaller import prompt
from filebrowser import file_browser
import json

# TODO: add next state to transition to
# TODO: for each state, make LLM choose from a set of options, and then transition to another state

class StateGenerator:
    def __init__(self, ) -> None:
        # get the required files to start generating JSON
        # Generate state instructions
        with open("Generate_State_Instructions.txt", "r") as file:
            self.state_instructions = file.read()

        # Functions
        with open("Functions.txt", "r") as file:
            text_tools = file.read()
            self.tools = json.loads(text_tools)
        
    
    def generate_states(self, task_file_name: str):
        # import txt from instruction file
        with open(task_file_name, "r") as file:
            task_instructions = file.read() 
        return prompt(self.state_instructions + task_instructions + self.tools).choices[0].message.content

class StateMachine:
    def __init__(self, states, tools) -> None:
        self.states = states["states"]
        self.tools = tools

        self.current_state = states[0]
        self.observation_queue = []
        with open("State_Prompt.txt", "r") as prompt:
            self.prompt = prompt.read()
            
        # Initialize MQTT
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(BROKER_ADDRESS, 1883, 60)
        self.client.subscribe(TOPIC)
        
    def on_message(self, client, userdata, msg):
        """Receives MQTT messages and processes them."""
        try:
            command = json.loads(msg.payload.decode())
            print(f"FSM received command: {command}")
            self.process_command(command)
        except json.JSONDecodeError:
            print("FSM: Invalid command format")

    def process_command(self, command):
        """Handles a command and determines the correct state transition."""
        command_type = command.get("command")

        if command_type == "talk":
            print(f"FSM: Robot says '{command.get('text', 'No text provided.')}'")
            self.transition_state("Talking")
        elif command_type == "move":
            print(f"FSM: Robot moves {command.get('distance', 0)} meters.")
            self.transition_state("Moving")
        elif command_type == "turn":
            print(f"FSM: Robot turns {command.get('angle', 0)} degrees.")
            self.transition_state("Turning")
        elif command_type == "exit":
            print("FSM: Received exit command. Shutting down...")
            self.client.disconnect()
        else:
            print("FSM: Unknown command received.")

    def transition_state(self, new_state_name):
        """Transitions FSM to a new state if valid."""
        for state in self.states:
            if state["name"] == new_state_name:
                print(f"FSM: Transitioning to {new_state_name}")
                self.current_state = state
                self.execute_function_call()
                return
        print(f"FSM: Cannot transition to unknown state '{new_state_name}'")

    def execute_function_call(self):
        """Executes functions associated with the current state."""
        functions = self.current_state.get("functions", [])
        if functions:
            print(f"FSM: Executing functions {functions} for state '{self.current_state['name']}'")
        else:
            print(f"FSM: No functions to execute for state '{self.current_state['name']}'")


#     def run(self):
#         self.update_observation_queue()
#         observation = self.observation_queue.pop(0)
#         tools = self.get_tools()
#         description = self.current_state['description']
#         instructions = self.current_state['instructions']
#         states = self.current_state['next_states']

#         messages = []
#         messages.append({"role": "system", "content": f"""You are a robot butler. Your current situation is: {description}.
#         You currently notice the following things about your surroundings:
#         \"{observation}\""

#         You have a choice of functions to call. Afterwards, you must choose which state to transition to. Only transition to a state if you succeeded in completing all of the instructions:
#         \"{states}\""""})
#         messages.append({"role": "user", "content": f"""Here are your instructions:
#                          \"{instructions}\""""})
        
#         response = prompt(messages, tools)

#         self.execute_function_call(response.choices[0].message, tools)
        
#     def update_observation_queue(self):
#         # TODO: add external observations from robot to the queue for LLM to use
#         pass
     
#     def get_tools(self):
#         def filter_for_tool(tool):
#             return tool["function"]["name"] in self.current_state["functions"]

#         return list(filter(filter_for_tool, self.tools))
    
#     def execute_function_call(self, message, tools):
#         # LLM executes external API calls here
#         tool_calls = message.tool_calls
#         if tool_calls:
#             pass
#         pass
        
# if __name__ == "__main__":
#     # read console input to choose the specific task file
#     chosen_file = file_browser()   

#     with open("test_states.txt", "r") as file:
#         states = json.load(file)

#     state_generator = StateGenerator()
#     #states = state_generator.generate_states(chosen_file)
#     state_machine = StateMachine(states, state_generator.tools)
#     state_machine.run()

    def update_observation_queue(self):
        """Updates observations (currently empty, but can be linked to sensors or MQTT)."""
        if not self.observation_queue:
            self.observation_queue.append("No new observations")

    def run(self):
        """Starts the FSM and listens for MQTT messages continuously."""
        print("FSM: Running and listening for commands...")
        self.client.loop_forever()

    @staticmethod
    def load_existing_fsm():
        """Loads FSM states from a file."""
        with open("test_states.txt", "r") as file:
            states = json.load(file)
        return StateMachine(states, [])

if __name__ == "__main__":
    fsm = StateMachine.load_existing_fsm()
    fsm.run()
