import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
machine = pyttsx3.init()

# Function to speak back to the user
def talk(text):
    machine.say(text)
    machine.runAndWait()

# Function to listen for an instruction from the user
def input_instruction():
    global instruction
    try:
        with sr.Microphone() as origin:
            print("myassistant is listening....")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "myassistant" in instruction:
                instruction = instruction.replace('myassistant', "").strip()
                print(instruction)

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        instruction = ""
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        instruction = ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        instruction = ""
    return instruction

# Function to open a file based on voice command (Windows-specific)
def open_file(file_name):
    try:
        # This will open a file using the default application associated with its extension on Windows
        os.startfile(file_name)
    except Exception as e:
        talk(f"An error occurred: {e}")

# Main function to perform tasks based on user instruction
def play_myassistant():
    instruction = input_instruction()  # Call the function to get user input
    print(instruction)

    if "play" in instruction:
        video = instruction.replace('play', "").strip()
        talk(f"Playing {video}")
        pywhatkit.playonyt(video)

    elif 'open' in instruction:  # Detect 'open' command
        file_name = instruction.replace('open', "").strip()
        talk(f"Opening {file_name}")
        open_file(file_name)

    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + date)

    elif 'how are you' in instruction:
        talk('I am fine, how about you?')

    elif 'what is your name' in instruction:
        talk('I am your virtual assistant. What can I do for you today?')

    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        try:
            info = wikipedia.summary(human, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results for that. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("I couldn't find any information about that person.")

    else:
        talk("I didn't understand that. Please repeat.")

# Run the assistant
play_myassistant()
