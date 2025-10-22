import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import geocoder

# -----------------------------
# 🔹 Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 155)  # Speed of speech
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)  # Female voice

# -----------------------------
# 🔹 Speak Function (Voice + Text)
def speak(text):
    print(f"FRIDAY 🎙️: {text}")
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# 🔹 Listen for User Voice Input
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎧 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🔍 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"🗣️ You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that. Please say that again.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is not available right now.")
        return ""

# -----------------------------
# 🔹 Weather Fetch
def get_weather():
    g = geocoder.ip('me')
    city = g.city or "your location"
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        weather = requests.get(url).text
        return f"The weather in {city} is {weather}."
    except:
        return "Sorry, I cannot fetch the weather right now."

# -----------------------------
# 🔹 Greeting
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Friday, your AI assistant. How can I help you?")

# -----------------------------
# 🔹 Process Commands
def process_command(command):
    if "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}")

    elif "date" in command:
        date_today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {date_today}")

    elif "weather" in command:
        speak(get_weather())

    elif "location" in command:
        g = geocoder.ip('me')
        city = g.city or "your area"
        country = g.country or "your country"
        speak(f"You are currently in {city}, {country}")

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            speak("Opening Google Chrome")
            os.startfile(chrome_path)
        else:
            speak("Chrome not found on this system.")

    elif "open prime video" in command:
        speak("Opening Amazon Prime Video")
        webbrowser.open("https://www.primevideo.com")

    elif "open control panel" in command:
        speak("Opening Control Panel")
        os.system("control")

    elif "exit" in command or "stop" in command or "quit" in command:
        speak("Goodbye Have a wonderful day!")
        exit()

    else:
        speak("Sorry, I can only handle basic commands like time, date, weather, location, Chrome, Prime Video, and Control Panel right now.")

# -----------------------------
# 🔹 Main Loop
def main():
    greet_user()
    while True:
        command = take_command()
        if command:
            process_command(command)

# -----------------------------
if __name__ == "__main__":
    main()

