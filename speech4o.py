import speech_recognition as speech

class speechToText:
    def convertToText():
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
                    break
                except speech.RequestError as e:
                    print('Error: Bad Request')
                
                except speech.UnknownValueError:
                    print('Error: Value Unknown')
    def isCommand(self, audioInput: str):
        pass


        