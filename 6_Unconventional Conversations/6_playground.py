from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import concurrent.futures

client = OpenAI()  # Automatically uses API key from environment variables
engine = pyttsx3.init()

def chat_with_openai(prompt):
    response = client.completions.create(model="gpt-3.5-turbo-instruct",  # Adjust model name here
                                         prompt=prompt,
                                         temperature=0.7,
                                         max_tokens=150)
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
    engine.runAndWait()


if __name__ == "__main__":
    # Ask your Genie three questions
    print("-> Ask me three Questions <-")

    for x in range(1):
        user_input = talk_to()
        # if user_input.lower() == "exit":
        #     print("Goodbye!")
        # break
        prompt = f"You said: {user_input}\nAI says:"
        response = chat_with_openai(prompt)
        # output the responses
    print("-> That is all! <- ")

#TODO add in 5 personalities, shorten up the token response on Chat-GPT, import to Kore.py, switch to multithreading