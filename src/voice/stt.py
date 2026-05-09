import os
import sys
import threading

old_stderr = None


def _silence_alsa():
    global old_stderr
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, "w")


def _restore_stderr():
    global old_stderr
    if old_stderr is not None:
        sys.stderr.close()
        sys.stderr = old_stderr


_silence_alsa()
import speech_recognition as sr
_restore_stderr()

recognizer = sr.Recognizer()

WAKE_WORDS = ["arthur", "author"]


def _detect_wake(text):
    lower = text.lower()
    for word in WAKE_WORDS:
        idx = lower.find(word)
        if idx != -1:
            after = text[idx + len(word):]
            return after.strip().lstrip(",:")
    return None


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = 1000
        recognizer.pause_threshold = 0.8

        while True:
            print("Listening for 'Arthur'...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"STT error: {e}")
                continue

            command = _detect_wake(text)
            if command is not None:
                if command:
                    print(f"You: {command}")
                    return command
                else:
                    print("Arthur? What do you need?")
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        command = recognizer.recognize_google(audio)
                        print(f"You: {command}")
                        return command
                    except (sr.UnknownValueError, sr.WaitTimeoutError):
                        continue
