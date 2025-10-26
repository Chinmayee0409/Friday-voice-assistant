import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import geocoder


# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)  # female if available
engine.setProperty('rate', 160)

def speak(text):
    print(f"FRIDAY 🎙️: {text}")
    engine.say(text)
    engine.runAndWait()


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


def get_weather(city=None):
    """Fetch weather for a given city, or current location if none provided."""
    if not city:
        g = geocoder.ip('me')
        city = g.city or "your location"
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        weather = requests.get(url).text
        return f"The weather in {city} is {weather}."
    except:
        return f"Sorry, I cannot fetch the weather for {city} right now."


def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Friday, your voice assistant. How can I help you?")


def process_command(command):
    if "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}")

    elif "date" in command:
        date_today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {date_today}")

    elif "weather" in command:
        # Detect if the user mentioned a city (e.g., "weather in Chennai")
        words = command.split()
        city = None
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city = " ".join(words[city_index:])  # Take words after "in" as city name

        speak(get_weather(city))

    elif "location" in command:
        g = geocoder.ip('me')
        city = g.city or "your area"
        country = g.country or "your country"
        speak(f"You are currently in {city}, {country}")

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            speak("Opening Google Chrome.")
            os.startfile(chrome_path)
        else:
            speak("Chrome not found on this system.")

    elif "open prime video" in command:
        speak("Opening Amazon Prime Video.")
        webbrowser.open("https://www.primevideo.com")

    elif "open control panel" in command:
        speak("Opening Control Panel.")
        os.system("control")

    elif "exit" in command or "stop" in command or "quit" in command:
        speak("Goodbye, Have a wonderful day!")
        exit()

    else:
        speak("Sorry, I can only handle basic commands right now.")


def main():
    greet_user()
    while True:
        command = take_command()
        if command:
            process_command(command)


if __name__ == "__main__":
    main()
