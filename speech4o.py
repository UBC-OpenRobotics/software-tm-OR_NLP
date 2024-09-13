import speech_recognition as sr

r = sr.Recognizer()

while(1):
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration = 0.2)
            audio = r.listen(source)
            print("Speak now:")
            text = r.recognize_google(audio, language = 'en-US', show_all = True)
            print(text)
        except sr.RequestError as e:
            print('Could not request results')
        
        except sr.UnknownValueError:
            print('unknown error occurred')
        