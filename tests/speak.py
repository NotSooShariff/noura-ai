import pyttsx3

def speak(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Set properties before adding anything to the queue
    engine.setProperty('rate', 150)  # Speed percent (can go from 0 to 200)
    engine.setProperty('volume', 1)  # Volume 0-1

    # Adding the text to the queue
    engine.say(text)

    # Run and wait until the speech is finished
    engine.runAndWait()

# Example usage
speak("Hello, how are you today?")
