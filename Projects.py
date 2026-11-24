import pyttsx3

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

name = input("Enter your name: ")
speak(f"Nice to meet you, {name}!")

hobby = input("What is your hobby? ")
speak(f"{hobby} sounds fun, {name}!")

subject = input("What is your favourite subject? ")
speak(f"I like {subject} too!")

game = input("What game do you play? ")
speak(f"Wow, {game}! Have a great day, {name}.")