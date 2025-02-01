import speech_recognition as speech
from openai import OpenAI
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import json

class speechToText:
    

    def listenForText(self):
        BROKER = "mqtt.eclipseprojects.io" 
        PORT = 1883

        TOPIC = "robot_command"

        client = mqtt.Client()

        # Connect to the broker
        client.connect(BROKER, PORT, 60)
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
                    if self.isCommand(text):
                        print("This is a command")
                        result = client.publish(TOPIC, text)
                        status = result[0]
                        if status == 0:
                            print("Success")
                        else:
                            print("Failed")
                    else:
                        print("This is NOT a command")
                except speech.RequestError as e:
                    print('Error: Bad Request')
                
                except speech.UnknownValueError:
                    pass

    def isCommand(self, audioInput: str) -> bool:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("API_KEY"))
        MODEL="gpt-4o"
        completion = client.chat.completions.create(
         model=MODEL,
         messages=[
           {"role": "system", "content": "You are a command detection bot"},
           {"role": "user", "content": 
            f"""You are a command detection bot and your purpose is to determine if the input, {audioInput},
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

if __name__ == "__main__":
    stt = speechToText()
    stt.listenForText()
