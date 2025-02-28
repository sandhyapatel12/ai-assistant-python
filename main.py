# Import necessary libraries
import speech_recognition as sr  # Used for speech-to-text conversion (recognizing voice)
import webbrowser  # Allows opening web pages in a browser
import pyttsx3  # Used for text-to-speech conversion (making the computer speak)
import musicLibrary
import requests
from google import genai
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Securely load API key (avoid hardcoding)
API_KEY = os.getenv("API_KEY")

recognizer = sr.Recognizer()  # Create an object for the speech recognizer
engine = pyttsx3.init()  # Create an object for the text-to-speech engine
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Function to make the computer speak
def speak(text):
    engine.say(text)  # Convert text into speech
    engine.runAndWait()  # Play the speech output

def aiProcess(command):
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=
       [
           {   "role": "system",
                "content": "You are a virtual assistant named jarvis skilled in gereral tasks like alexa and google cloud. give short response please"
           },
           {
            "role": "user",
            "content": command
            }
        ]      
    )

    return response.text    

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")  

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com") 

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com") 

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")     

    # work like (if i say to jarvis "play natural" then  first convert into lower and then create list like ["play" "natural"] and then take first index means "natural" and play natural song from youtube )
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]     
        webbrowser.open(link)  

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")  
        if r.status_code == 200:
            data = r.json()  #parse the json response
            articles = data.get('articles', [])  #extract the articles

            #print the headlines
            for articles in articles:
                speak(articles['title'])

    else:
        #let open ai handle the request
         output = aiProcess(c)
         speak(output)         
  

             
# Main program execution starts here
if __name__ == "__main__":  
    speak("Initializing Jarvis.............")  # Speak this text when the program starts
    while True:
        print("Recognizing...")  # This prints to indicate recognition is in progress
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Increase timeout

            word = recognizer.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes jarvis here")

                # listen for command   
                with sr.Microphone() as source:
                    print("jarvis active...")
                    # recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processCommand(command)



        except sr.WaitTimeoutError:
            print("Error: Listening timed out. No speech detected.")
        except sr.UnknownValueError:
            print("Error: Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error: Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
