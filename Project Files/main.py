import speech_recognition as sr
from gtts import gTTS
import pygame
import webbrowser as web
import musicLibrary as music
import requests
import google.generativeai as genai
import os


NewsapiKey='a29ecb314a0046298af2b994bee4752b'
apiKey='AIzaSyCBPH6hkNxIyAQJN9v7y1y4PrlV3MlVCxY'


#speak function for trxt to speech
def speak(text):
    #converting the text to speech and saving in a temp mp3 file
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    #using pygame python module to play the mp3
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    #unloading so that the error does not occur
    pygame.mixer.music.unload()
    os.remove('temp.mp3')


#integrating ai for user demanded queries
def aiProcess(command):
    
    genai.configure(api_key=apiKey)

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"Give short responses based on {command}"
    )

    return response.text

#basic commands which we can process without ai
def processCommand(command):
    if 'open youtube' in command.lower():
        web.open('https://www.youtube.com')
    elif 'open facebook' in command.lower():
        web.open('https://www.facebook.com')
    elif 'open instagram' in command.lower():
        web.open('https://www.instagram.com')
    elif 'open amazon' in command.lower():
        web.open('https://www.amazon.com')
    elif 'open flipkart' in command.lower():
        web.open('https://www.flipkart.com')
    elif 'open vscode' in command.lower():
        web.open('https://www.vscode.com')
    elif 'open google' in command.lower():
        web.open('https://www.google.com')
    elif 'open chrome' in command.lower():
        web.open('https://www.chrome.com')
    elif 'open python' in command.lower():
        web.open('https://www.python.com')

    #playing of songs as per requests and playlist
    elif command.lower().startswith('play'):
        song=command.lower().split(' ')[1]
        link=music.musicLinks[song]
        web.open(link)
    
    #news integration for news fetching
    elif command.lower().startswith('top news'):
        

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NewsapiKey}"

        response = requests.get(url)

        data = response.json()

        for article in data["articles"]:
            news=(article["title"])
            speak(news)
    else:
        #if none will work we will send the command to process by ai
        output=aiProcess(command)
        speak(output)

#main function which will operate the functioning
if __name__=='__main__':
    #Initializing Jarvis
    speak('Initializing Jarvis...')
    r=sr.Recognizer()

    #To Make sure the listening function runs continously for the user we will use infinite loop
    while True:
        try:
            print('Listening...')
            
            #using microphone to take voice input from the user
            with sr.Microphone() as source:
                audio=r.listen(source,timeout=3,phrase_time_limit=2)
                print('Recognizing....')

            #converting this voice input to text for further proceeds
            word=r.recognize_google(audio)

            if 'jarvis' in word.lower():
                speak('ya')
                print('Jarvis Active....')

                #now if Jarvis got activated we will take command from the user
                with sr.Microphone() as source:
                    audio=r.listen(source)
                #converting the voice command to text for further proceeds
                command=r.recognize_google(audio)
                #function call for operating the command
                processCommand(command)
        #if the voice cannot be recognized we will show the error
        except Exception as e:
            print('Error,{0}'.format(e))
