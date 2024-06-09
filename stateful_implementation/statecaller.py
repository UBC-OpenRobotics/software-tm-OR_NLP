# from gptcaller import prompt
from filebrowser import file_browser
import json

# TODO: add next state to transition to
# TODO: for each state, make LLM choose from a set of options, and then transition to another state

class StateGenerator:
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
        
    # generate states through  
    def generate_states(self, task_file_name: str):
        with open(task_file_name, "r") as file:
            task_instructions = file.read() 
        # prompt LLM w/ custom instructions + task instructions to generate states 
        return prompt(self.state_instructions + task_instructions + self.tools).choices[0].message.content

class StateMachine:
    def __init__(self, states, tools) -> None:
        self.states = states["states"]
        self.tools = tools

        self.current_state = states[0]
        self.observation_queue = []
        with open("State_Prompt.txt", "r") as prompt:
            self.prompt = prompt.read()

    def run(self):
        self.update_observation_queue()
        observation = self.observation_queue.pop(0)
        tools = self.get_tools()
        description = self.current_state['description']
        instructions = self.current_state['instructions']
        states = self.current_state['next_states']

        messages = []
        messages.append({"role": "system", "content": f"""You are a robot butler. Your current situation is: {description}.
        You currently notice the following things about your surroundings:
        \"{observation}\""

        You have a choice of functions to call. Afterwards, you must choose which state to transition to. Only transition to a state if you succeeded in completing all of the instructions:
        \"{states}\""""})
        messages.append({"role": "user", "content": f"""Here are your instructions:
                         \"{instructions}\""""})
        
        response = prompt(messages, tools)

        self.execute_function_call(response.choices[0].message, tools)
        
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

    with open("test_states.txt", "r") as file:
        states = json.load(file)

    # initiate state generator object
    state_generator = StateGenerator()
    # get states based on selected file
    states = state_generator.generate_states(chosen_file)
    state_machine = StateMachine(states, state_generator.tools)
    # state_machine.run()