import speech_recognition as speech
from openai import OpenAI
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import json

class speechToText:
    
    def __init__(self, apiKeyGPT):
        self.client = OpenAI(api_key=apiKeyGPT)
        self.MODEL = "gpt-4o"
        
    def listenForText(self):
        r = speech.Recognizer()

        # Adjusts sound threshold for speech detection, 0.15 by default
        # Values between 0 and 1, lower values means faster adjustment but may miss words
        # r.recognizer_instance.dynamic_energy_adjustment_damping = 0.15

        # Min length of silence to register end of phrase
        # r.recognizer_instance.pause_threshold = 0.8

        # Adjusts for ambient noise, then waits for noise. After that, api call to convert stt

        while True:
            with speech.Microphone() as source:
                try:
                    r.adjust_for_ambient_noise(source, duration = 0.2)
                    audio = r.listen(source)
                    text = r.recognize_google(audio, language = 'en-US')
                    print(text)
                    if text.lower() == 'stop' or text.lower() == 'start':
                        print("Stop or start stated")

                    if self.isCommand(text):
                        print("This is a command")
                    else:
                        print("This is NOT a command")
                except speech.RequestError as e:
                    print('Error: Bad Request')
                
                except speech.UnknownValueError:
                    print("Did not hear")

    def isCommand(self, audioInput: str) -> bool:
        completion = self.client.chat.completions.create(
         model=self.MODEL,
         messages=[
           {"role": "system", "content": "You are a command detection bot"},
           {"role": "user", "content": 
            f"""You are a command detection bot and your purpose is to determine if the input, "{audioInput}",
            is a command, or a request. If the given sentence is a command or request, return "True", if not, then return
            "False" Do not include any additional text that is not specified here and only return exactly
            what is asked"""}
         ]
        )

        isCommand = completion.choices[0].message.content

        if isCommand.lower() == "true":
            return True
        elif isCommand.lower() == "false":
            return False
        else:
            raise Exception(f"GPT Returned: {isCommand}")
            
    def conversationBot(self, audioInput: str) -> str:
        completion = self.client.chat.completions.create(
         model=self.MODEL,
         messages=[
           {"role": "system", "content": "You are a friendly person"},
           {"role": "user", "content": 
            f"""You are a friendly person, and you're purpose is to generate a response to this, it can be laughter if it is a joke,
            or it can be an answer to a question, or it can be simply a response to a statement. The other person has said {audioInput}.
            Make sure you only use text"""}
         ]
        )
        response = completion.choices[0].message.content
        print(response)
        return response

if __name__ == "__main__":
    load_dotenv()
    stt = speechToText(apiKeyGPT=os.getenv("API_KEY"))
    stt.listenForText()
