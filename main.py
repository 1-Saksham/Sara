import speech_recognition as sr
import webbrowser
import pyttsx3
import dataLibrary
import time
import re

# Initialize recognizer and text-to-speech engine
recogniser = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak
def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Getting indices from string
def last_word(s):
    words = s.split()
    if len(words) > 0:
        return words[-1].lower()
    else:
        return None

def thirdlast_word(s):
    words = s.split()
    if len(words) > 0:
        return words[-3].lower()
    else:
        return None
    
def first_word(s):
    words = s.split()
    if len(words) > 0:
        return words[0].lower()
    else:
        return None

# POMODORO Function

def countdown_timer(seconds, end_message, notify):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02}:{secs:02}"

        if seconds == 1800:
          speak(f"{notify}")
        if seconds == 300:
          speak(f"Five minutes remaining!")

        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print(end_message)
    speak(end_message)

def pomodoro_timer(work_duration, break_duration):
    speak("Work session starting!!")
    print("Work Session:")
    countdown_timer(work_duration * 60, "Focus time is over! You can take a break now!", f"Keep going, thirty minutes remaining in the session!")
    print("Break Session:")
    countdown_timer(break_duration * 60, "Break is over, Do you want another session?")

    r = sr.Recognizer()
    print("Listening for response...")  
    try:
       with sr.Microphone() as source:
        audio = r.listen(source, timeout=3, phrase_time_limit=3)
        resp = r.recognize_google(audio)
                
        if "yes" in resp.lower():
          speak("Great, how long do you prefer it?")
          # Seeking time
          with sr.Microphone() as source:
            print("Listening for time. (eg. 50 and 10)")
            audio = r.listen(source)
            time = r.recognize_google(audio)
            print(time)
            i = extract_numbers(time)[0]
            j = extract_numbers(time)[1]
            pomodoro_timer(int(i),int(j))
        
        elif "no" in resp.lower() :
            speak("Alright, see you soon!")
            pomodoro_active= False

    except Exception as e:
        speak("I couldnt hear you, please reset the timer by saying the wake word")

# Extracting numbers
def extract_numbers(command):
    # Find all sequences of digits in the command
    numbers = re.findall(r'\d+', command)
    # Convert them to integers 
    return [int(num) for num in numbers]

# Addition
def get_sum(numList):
    sum = 0
    for i in numList:
        sum += i  
    return sum


# Function to process command

def doCommand(c):
    global pomodoro_active
    
    if "open" in c.lower():
        webbrowser.open(f"https://www.{last_word(c)}.com/")
    elif "show me pictures of" in c.lower():
        speak("There you go sir")
        webbrowser.open(f"https://www.google.com/search?sca_esv=53e1b9c4b6162517&sxsrf=ADLYWIIe_BIIHIbHIGlxulDwwA0k2yMlXg:1730054633258&q={c.lower().replace("show me pictures of", "").strip()}&udm=2&fbs=AEQNm0COtQ6qE5snXClm_cWqGTLX_jMP5V4l2v9LemFtanifXUj1LD6QCINf2Stcfc55fHi_K0iAiH4y_ML3L3eGQg5P-iuT1QvbjsxInYkhCPQm-sYLJdV1DOkMWHHkY-i7EY26LN80Qro5EB0XqKeI7nUYgY5Xid1OWpbGJmYhpmga0-Qmop9EJ7_jcU9M50Y1SyzUQzAFBPiUPo80VreD2GtlVqLYow&sa=X&ved=2ahUKEwiw2O3em6-JAxVeR2wGHVXJKWgQtKgLegQIGhAB&biw=1536&bih=730&dpr=1.25")
    elif "search" in c.lower():
        speak(f"searching for: {c.lower().replace('search', '').strip()}")
        webbrowser.open(f"https://www.google.com/search?q={c.lower().replace('search', '').strip()}")
    elif "play" in c.lower():
        song = dataLibrary.songs[c.lower().replace("play", "").strip()]
        webbrowser.open(song)
        speak(f"Playing {c.lower().replace('play', '').strip()}")
    elif "pomodoro" in c.lower():
        i = extract_numbers(c)[0]
        j = extract_numbers(c)[1]
        pomodoro_active = True
        pomodoro_timer(int(i), int(j))
        pomodoro_active = False  
    elif "atomic number of" in c.lower():
        ans = dataLibrary.atomicNumber[c.lower().replace("atomic number of","").strip()]
        speak(f"Atomic number of {c.lower().replace("atomic number of","").strip()} is {ans}")
        print(f"Atomic number of {c.lower().replace("atomic number of","").strip()} is {ans}")
    elif "atomic mass of" in c.lower():
        ans = dataLibrary.atomicMass[c.lower().replace("atomic mass of","").strip()]
        speak(f"Atomic mass of {c.lower().replace("atomic mass of","").strip()} is {ans} a m u ")
        print(f"Atomic mass of {c.lower().replace("atomic mass of","").strip()} is {ans} amu")
    elif "plus" in c.lower() or "add" in c.lower() or "sum of" in c.lower():
        numList = extract_numbers(c)
        ans = get_sum(numList)
        print(f"The sum of {extract_numbers(c)} is {ans}")
        speak(f"The sum of {extract_numbers(c)} is {ans}")

if __name__ == "__main__":
    speak("Glad to see you Sir, Saara is waiting for the wake word.")
    pomodoro_active = False 

    while True:
        if not pomodoro_active:
            # Seeking wake word
            r = sr.Recognizer()
            print("Decoding...")
            try:
                with sr.Microphone() as source:
                    print("Listening for wake word...")
                    audio = r.listen(source, timeout=2, phrase_time_limit=3)
                wake = r.recognize_google(audio)
                
                if "hello sara" in wake.lower():
                    speak("Yes sir")
                    
                    # Seeking commands
                    with sr.Microphone() as source:
                        print("Sara is activated!")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        print(command)
                        doCommand(command)
                elif "bhai sara" in wake.lower() or "bye sara" in wake.lower():
                    speak("Saara deactivated")
                    print("Sara deactivated")
                    exit()

            except Exception as e:
                print("Wake word not detected, access denied.")

