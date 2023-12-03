from openai import OpenAI
from abc import ABC, abstractmethod
import json

class ParameterInfo:
    def __init__(self, name: str, parameter_type: str, description: str):
        self.name = name
        self.type = parameter_type
        self.description = description

    def get_json(self) -> dict[str: str]:
        return {"type": self.type, "description": self.description}

class Parameters:
    def __init__(self, parameters: list[ParameterInfo]) -> None:
        self.parameters = parameters

    def get_json(self) -> dict[str: str | dict]:
        properties = {x.name: x.get_json for x in self.parameters}
        return {"type": "object", "properties": properties}

class Tool:
    def __init__(self, name: str, description: str, parameters: Parameters) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters

    def get_json(self) -> dict[str: str | dict]:
        return {"type": "function", "function": {"name": self.name, "description": self.description, "parameters": self.parameters.get_json()}}

class RobotLM(ABC):
    @abstractmethod
    def __init__(self, instructions: str) -> None:
        pass

    @abstractmethod
    def chat(self, message) -> str:
        pass

    @abstractmethod
    def chat_with_function(self, message, tools) -> str:
        pass

class OpenAIChat(RobotLM):
    def __init__(self, instructions: str, model: str, functions: dict, api_key: str = None):
        super().__init__(instructions)
        self.messages = [
            {
                "role": "system",
                "content": instructions
            }
        ]
        if api_key is None:
            raise Exception("No API key specified")
        self.client = OpenAI(api_key)
        self.model = model
        self.available_functions = functions

    def chat(self, message) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages = self.messages
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": response['choices'][0]['message']['content']
            }
        )
        return response['choices'][0]['message']

    def chat_with_function(self, message, tools: list[Tool]) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        response = self.client.chat.completions.create(
            model=self.model,
            temperature = 0,
            messages = self.messages,
            tools = [tool.get_json() for tool in tools],
            tool_choice = "auto"
        )
        response_message = response['choices'][0]['message']
        tool_calls = response_message.tool_calls
        if tool_calls:
            self.messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response
                    }
                )
            second_response = self.client.chat.completions.create(
                model = self.model,
                messages = self.messages
            )
            return second_response[0]['choices']['message']
        else:
            return response_message


