from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import threading
import random

client = OpenAI()  # Automatically uses API key from environment variables
engine = pyttsx3.init()


def chat_with_openai(prompt):
    response = client.completions.create(model="gpt-3.5-turbo-instruct",  # Adjust model name here
                                         prompt=prompt,
                                         temperature=0.7,
                                         max_tokens=10)
    return response.choices[0].text.strip()


def talk_to() -> str:
    with sr.Microphone() as source:
        r = sr.Recognizer()

        # Adjust for backround -> maybe can use speaker for ready ambient?
        r.adjust_for_ambient_noise(source)
        # Adjust for basic control
        r.dyanmic_energythreshhold = 3000

        try:
            print("***listening***")
            # this is the recorded sound
            audio = r.listen(source)
            print("***Got audio***")
            # this is what the robot hears
            word = r.recognize_google(audio)
            print(word)
            return str(word)
        except sr.UnknownValueError:
            print("***Don't know that word***")
            return str(Exception)
        print(":: ERR- FUNCTION OUT OF BOUNDS IN TALK_TO() ::")
        return "ERR"


def talk_back(words):
    engine.say(words)


def set_personality(personality):
    match personality:
        case "friendly":
            engine.setProperty('rate', 150)  # Adjust speaking rate (words per minute)
            engine.setProperty('pitch', 200)  # Adjust voice pitch (50-400)
            engine.setProperty('volume', 6.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')  # Set voice type
            engine.setProperty('word_gap', 15)  # Set gap between words in milliseconds
            engine.setProperty('sentence_gap', 200)  # Set gap between sentences in milliseconds
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
            engine.say("<emphasis level='strong'>Hello</emphasis>")  # Add emphasis or pronunciation markup
        case "comedian":
            engine.setProperty('rate', 180)  # Adjust speaking rate (words per minute)
            engine.setProperty('pitch', 220)  # Adjust voice pitch (50-400)
            engine.setProperty('volume', 1.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Bad News')  # Set voice type
            engine.setProperty('word_gap', 15)  # Set gap between words in milliseconds
            engine.setProperty('sentence_gap', 200)  # Set gap between sentences in milliseconds
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
            engine.say(
                "Why did the chicken cross the road? To get to the other side!")  # Add emphasis or pronunciation markup
        case "spongebob":
            engine.setProperty('rate', 170)  # Adjust speaking rate (words per minute)
            engine.setProperty('pitch', 250)  # Adjust voice pitch (50-400)
            engine.setProperty('volume', 1.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Bad News')  # Set voice type
            engine.setProperty('word_gap', 20)  # Set gap between words in milliseconds
            engine.setProperty('sentence_gap', 250)  # Set gap between sentences in milliseconds
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
            engine.say("Hey, I'm ready for some fun!")  # Add emphasis or pronunciation markup

        case "gandalf":
            engine.setProperty('rate', 120)  # Adjust speaking rate (words per minute)
            engine.setProperty('pitch', 80)  # Adjust voice pitch (50-400)
            engine.setProperty('volume', 1.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Ralph')  # Set voice type
            engine.setProperty('word_gap', 30)  # Set gap between words in milliseconds
            engine.setProperty('sentence_gap', 400)  # Set gap between sentences in milliseconds
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
            engine.say("You shall not pass!")  # Add emphasis or pronunciation markup
        case "professor":
            engine.setProperty('rate', 140)  # Adjust speaking rate (words per minute)
            engine.setProperty('pitch', 150)  # Adjust voice pitch (50-400)
            engine.setProperty('volume', 1.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Victoria')  # Set voice type
            engine.setProperty('word_gap', 20)  # Set gap between words in milliseconds
            engine.setProperty('sentence_gap', 250)  # Set gap between sentences in milliseconds
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
            engine.say("Ah, yes! Let me tell you about the fascinating world of quantum physics! Did you know that particles can exist in multiple states simultaneously?")
        case _:
            # If the personality is not recognized, set a random personality
            random_personality = random.choice(["friendly", "formal", "quirky", "calm", "robotic"])
            print(f"Personality '{personality}' not recognized. Setting random personality: {random_personality}")
            set_personality(random_personality)


if __name__ == "__main__":
    # List of personalities
    personalities = ["friendly", "comedian", "spongebob", "gandalf", "professor"]

    # Ask your Genie three questions
    print("-> Ask me three Questions <-")

    # Inside the main block
    for personality in personalities:
        print(f"Current personality: {personality}")
        set_personality(personality)

        for x in range(1):  # Ask three questions for each personality
            user_input = talk_to()
            prompt = f"You said: {user_input}\nAI says:"
            response = chat_with_openai(prompt)

            # Remove extra spaces from the response
            words = response.split()  # Split the text into words
            cleaned_words = [word.strip() for word in words]  # Remove extra spaces from each word
            response_cleaned = ' '.join(cleaned_words)  # Join the cleaned words back together

            # Output the responses using threading
            thread1 = threading.Thread(target=talk_back, name="Thread 1", args=(response_cleaned,))
            thread2 = threading.Thread(target=print, name="Thread 2", args=(response,))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()
            print("after")

    print("-> That is all! <- ")


# TODO add in 5 personalities, import to Kore.py
