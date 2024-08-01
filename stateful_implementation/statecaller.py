from gptcaller import prompt
from filebrowser import file_browser
import json
import os

# TODO: add next state to transition to
# TODO: for each state, make LLM choose from a set of options, and then transition to another state

class StateGenerator:
    # initialize object: set instructions and functions
    def __init__(self, ) -> None:
        # get the required files to start generating JSON
        # Generate state instructions
        # open file in read mode
        with open("Generate_State_Instructions.txt", "r") as file:
            self.state_instructions = file.read()

        # Functions
        with open("Functions.txt", "r") as file:
            text_tools = file.read()
            self.tools = json.loads(text_tools)
        
    # generate states  
    def generate_states(self, task_file_name: str):
        # this is just a os-agnostic way of doing tasks/chosen_file
        with open(os.path.join("tasks", task_file_name), "r") as key_file:
            task_instructions = key_file.read() 
         # construct messages for the prompt
        messages = [
            {"role": "system", "content": "You are an AI assistant helping to design a robot's decision-making process."},
            {"role": "user", "content": self.state_instructions},
            {"role": "user", "content": task_instructions},
            {"role": "user", "content": json.dumps(self.tools)}
        ]
        # prompt LLM w/ custom (prompt) instructions + task instructions to generate states 
        # prompt is fn in gptcaller.py
        response = prompt(messages)
        # print(response)
        # return the content of the response
        return response.choices[0].message.content
class StateMachine:
    def __init__(self, states, tools) -> None:
        self.states = states["states"]
        self.tools = tools

        self.current_state = self.states[2]
        self.observation_queue = []
        with open("State_Prompt.txt", "r") as prompt:
            self.prompt = prompt.read() # NOT USED CURRENTLY

    def run(self):
        # self.update_observation_queue()
        # observation = self.observation_queue.pop(0)
        tools = self.get_tools()
        description = self.current_state['description']
        instructions = self.current_state['instructions']
        states = self.current_state['next_states']

        messages = [
            {"role": "system", "content": f"""You are a robot butler. Your current situation is: {description}.
            You currently notice the following things about your surroundings:
            \"{""}\""

            You have a choice of functions to call. Afterwards, you must choose which state to transition to. Only transition to a state if you succeeded in completing all of the instructions:
             \"{states}\""""},
            {"role": "user", "content": f"""Here are your instructions:
            \"{instructions}\""""},
            {"role": "user", "content": "Here are the available functions you can call:"},
            {"role": "user", "content": json.dumps(self.tools)}]
        
        response = prompt(messages)
        # self.execute_function_call(response.choices[0].message, tools)
        return response.choices[0].message.content
        
    def update_observation_queue(self):
        # TODO: add external observations from robot to the queue for LLM to use
        pass
     
    def get_tools(self):
        def filter_for_tool(tool):
            return tool["function"]["name"] in self.current_state["functions"]

        return list(filter(filter_for_tool, self.tools))
    
    def execute_function_call(self, message, tools):
        # LLM executes external API calls here
        tool_calls = message.tool_calls
        if tool_calls:
            pass
        pass
        
if __name__ == "__main__":
    # read console input to choose the specific task file
    chosen_file = file_browser()   
    
    # initiate state generator object
    state_generator = StateGenerator()
    # get states based on selected file
    # states = state_generator.generate_states(chosen_file)
    # type(states)
    # states = json.loads(states)
    # print(states)
    
    with open("test_states.txt", "r") as file:
        states = json.load(file)
    
    # print(states)
    # create FSM based on generated states
    state_machine = StateMachine(states, state_generator.tools)
    # print("FSM created !!!!")
    selected_function = state_machine.run()
    print(selected_function)