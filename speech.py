import pyaudio
import speech_recognition as sr

def main(source):
    audio = r.listen(source)
    user = r.recognize_whisper(audio)
    print(user)

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            main(source)