from openai import OpenAI
# from gpt4all import GPT4All
# LOCAL_LLM = False

# if LOCAL_LLM:
#     client = GPT4All(model_name="mistral-7b-openorca.gguf2.Q4_0.gguf", device="gpu")
# else:
with open("./OPEN_AI_KEY.txt", "r") as key_file:
    OPEN_AI_KEY = key_file.read().strip()
client = OpenAI(api_key=OPEN_AI_KEY)


GPT_MODEL = "gpt-4"

def prompt(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice
        )
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

# def prompt(prompt: str):
#     return client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#     )

# def prompt_json(prompt: str):
#     return client.chat.completions.create(
#         model="gpt-4",
#         response_format={"type": "json_object"},
#         messages=[{"role": "user", "content": prompt}],
#     )

# # TODO make prompt_function, which will return function call
# def prompt_function(prompt: str, tools):
#     messages = [{"role": "user", "content": prompt}]
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto"
#     )
#     response_message = response.choices[0].message
#     tool_calls = response_message.tool_calls
#     if tool_calls:
#         available_functions = {
#             # TODO
#             "name of function": prompt
#         }
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_to_call = available_functions[function_name]
#             function_args = json.loads(tool_call.function.arguments)