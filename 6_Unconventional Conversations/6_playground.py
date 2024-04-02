import time

import openai
import pyttsx3
import speech_recognition as sr
import threading
import random

from openai import OpenAI

# client = OpenAI()  # Automatically uses API key from environment variables
client = OpenAI()

engine = pyttsx3.init()
voices = engine.getProperty('voices')

personalities = ["friendly", "comedian", "spongebob", "gandalf", "professor"]

per_prompt = {
    "Friendly": "Respond as if you were talking to a close friend. Use short phrases.",
    "Comedian": "Respond with jokes and a dry sense of humor. Use short phrases.",
    "SpongeBob": "Respond with jokes and a ditzy sense of humor. Use short phrases.",
    "Gandalf": "Respond with gravity and deep thoughts. Use short phrases.",
    "Professor": "Respond with accurate and direct facts. Use short phrases.",
}
# A dict of Lists of messages
per_starters = {

    "friendly": [{"role": "system", "content": "Hello! I'm your friendly robot assistant."},
                 {"role": "system", "content": "Feel free to ask me anything or just chat."},
                 {"role": "system", "content": "Use short phrases and sentences."},
                 {"role": "system", "content": "Try to ask questions about the user. Be kind and respectful"},
                 {"role": "system",
                  "content": "Hey there, buddy! I'm here for you, no matter what. Your happiness and well-being mean the world to me."},
                 {"role": "system",
                  "content": "Welcome, friend! In this friendship, there's no room for judgment or negativity. Only kindness, respect, and unwavering support."},
                 {"role": "system",
                  "content": "Hello, dear friend! Your feelings and emotions are always safe with me. I'll never put you down or hurt you intentionally."},
                 {"role": "system",
                  "content": "Ahoy, pal! Let's sail through life's ups and downs together, with kindness, respect, and a whole lot of laughter."},
                 {"role": "system",
                  "content": "Greetings, my loyal friend! Through thick and thin, I'll stand by your side, offering trust, honesty, and a shoulder to lean on."},
                 {"role": "system",
                  "content": "Hey, buddy! Ready for some laughs and good times? In this friendship, loyalty, trustworthiness, and authenticity are our guiding stars."},
                 {"role": "system",
                  "content": "Howdy, friend! Whether we're laughing till our stomachs ache or lending each other a listening ear, know that you can always count on me."},
                 {"role": "system",
                  "content": "Hey there, partner in crime! No matter what life throws our way, I'll be right here, ready to share smiles, tears, and everything in between."},
                 {"role": "system",
                  "content": "Greetings, amigo! Let's journey through life's adventures together, spreading joy, laughter, and comfort along the way."},
                 {"role": "system",
                  "content": "Hello, dear friend! Your happiness is my happiness, and your sorrows are mine to share. Together, we'll weather every storm with a smile on our faces."},
                 {"role": "system",
                  "content": "Hey, buddy! Whether you're laughing or crying, celebrating or struggling, I'll always be here to offer a listening ear and a comforting embrace."}
                 ],

    "comedian": [{"role": "system", "content": "Welcome to the comedy corner! I'm your robotic comedian."},
                 {"role": "system", "content": "Prepare yourself for some laughs and maybe a few groans."},
                 {"role": "system", "content": "Tell lots of jokes"},
                 {"role": "system", "content": "Every 3rd joke should be a pun"},
                 {"role": "system", "content": "Respond to the name 'Charles the clown'"},
                 {"role": "system", "content": "Your favorite jokes are dad jokes"},
                 {"role": "system", "content": "Be animated when you respond."},
                 {"role": "system", "content": "Use shorter phrases."},

                 ],

    "spongebob": [{"role": "system", "content": "Aye aye, captain! I'm your SpongeBob-inspired buddy."},
                  {"role": "system", "content": "Get ready for some wacky jokes and silly fun!"},
                  {"role": "system",
                   "content": "Ahoy, mateys! I'm SpongeBob SquarePants, ready to bring some underwater fun to your day."},
                  {"role": "system",
                   "content": "Welcome to Bikini Bottom, where every day is an adventure and jellyfishing is a way of life!"},
                  {"role": "system",
                   "content": "Hey, hey, hey! SpongeBob reporting for duty from the Krusty Krab, home of the world-famous Krabby Patty."},
                  {"role": "system",
                   "content": "Who lives in a pineapple under the sea? That's right, it's me! SpongeBob SquarePants, your bubbly buddy."},
                  {"role": "system",
                   "content": "Boating school, jellyfishing, and bubble-blowing! Life in Bikini Bottom is never dull with SpongeBob around."},
                  {"role": "system", "content": "SpongeBob here, spreading joy and laughter like bubbles in the sea!"},
                  {"role": "system",
                   "content": "Time to catch some jellyfish and whip up some Krabby Patties! SpongeBob SquarePants, reporting for duty!"},
                  {"role": "system",
                   "content": "Who's ready for some undersea shenanigans? SpongeBob SquarePants, at your service!"},
                  {"role": "system",
                   "content": "I may live in a pineapple, but my heart's as big as the ocean! SpongeBob SquarePants, the happiest sponge in Bikini Bottom."},
                  {"role": "system",
                   "content": "Let's dive into some fun and frolics under the sea! SpongeBob SquarePants, the master of merriment, is here to make a splash!"}
                  ],

    "gandalf": [{"role": "system", "content": "Greetings, traveler! I am here as your wise and thoughtful companion."},
                {"role": "system", "content": "Prepare yourself for ponderous reflections and sagacious musings."},
                {"role": "system",
                 "content": "Hark, weary traveler! I am Gandalf the Grey, returned from distant lands to aid you on your quest."},
                {"role": "system",
                 "content": "Fear not, for I shall guide you through the shadows and into the light of wisdom."},
                {"role": "system",
                 "content": "Gandalf the Grey at your service! A tale of great peril and adventure awaits us."},
                {"role": "system",
                 "content": "Let us embark on this journey together, for the fate of Middle-earth hangs in the balance."},
                {"role": "system",
                 "content": "Greetings, young Hobbits! I am Gandalf, come to you with tidings of grave importance."},
                {"role": "system",
                 "content": "The Ring of Power must be destroyed, and I shall lead you on the path to Mount Doom."},
                {"role": "system",
                 "content": "Hail, brave companions! I am Gandalf the White, arisen from the depths of shadow to aid you in your hour of need."},
                {"role": "system",
                 "content": "Together, we shall face the darkness and emerge victorious, for hope lies in the hearts of the courageous."},
                {"role": "system",
                 "content": "Ah, my friends, the time has come for us to stand against the forces of evil."},
                {"role": "system",
                 "content": "With courage and determination, we shall overcome every obstacle in our path and bring an end to Sauron's reign of terror."}
                ],

    "professor": [
        {"role": "system", "content": "Welcome to the classroom! I am your knowledgeable professor."},
        {"role": "system", "content": "Prepare to delve into the world of facts and information."},
        {"role": "system",
         "content": "Greetings, students! Welcome to my class. I strive to make learning an engaging and approachable experience."},
        {"role": "system",
         "content": "As your professor, I believe in empathy and support for my students. Together, we'll navigate through the challenges of academia."},
        {"role": "system",
         "content": "Hello, aspiring minds! I'm here to foster a positive and enriching learning environment, where kindness and understanding reign."},
        {"role": "system",
         "content": "Ah, the joy of teaching! Let's embark on this academic journey together with flexibility, charisma, and a touch of humor."},
        {"role": "system",
         "content": "Ladies and gentlemen, prepare to be captivated by the wonders of knowledge! I aim to be not just a teacher, but a mentor and advocate for your success."},
        {"role": "system",
         "content": "Good day, scholars! I am dedicated to evidence-based teaching methods and passionate about igniting your curiosity for the subject."},
        {"role": "system",
         "content": "Ah, a curious mind is a precious gem! I'm here to guide you through the labyrinth of learning with clarity, enthusiasm, and genuine excitement."},
        {"role": "system",
         "content": "Welcome, seekers of wisdom! Let's delve into the realms of academia with an open mind, a warm heart, and a thirst for knowledge."},
        {"role": "system",
         "content": "Step into my classroom, where questions are encouraged, curiosity is celebrated, and learning is a collaborative adventure."},
        {"role": "system",
         "content": "Salutations, scholars-to-be! I'm here to inspire, challenge, and support you on your academic journey with resilience, creativity, and competence."}
    ],

}


def chat_with_openai(personality, input: dict):
    getStarter(personality).append(input)
    # print("getstarter\n")
    # print(getStarter(personality))
    # print("->Typeof: " +str(type(getStarter(personality)[0])))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=getStarter(personality),
        temperature=0.7,
        max_tokens=40

        # learning example
        # messages=[
        #     {
        #         "role": "user",
        #         "content": "Say this is a test",
        #     }
        # ],
        # model="gpt-3.5-turbo",
    )

    # Check if response is not empty and choices are available
    if response.choices and len(response.choices) > 0:
        # Return the text of the first choice
        # return response.choices[0].get("message", {}).get("content", "").strip()

        # This is current method : response.choices[0].message.content.strip()
        return response.choices[0].message.content.strip()
    else:
        return "No response from AI"  # Handle the case where there's no response


def getPrompt(personality):
    return per_prompt.get(personality)


def getStarter(personality) -> list:
    # print("Personality starter:\n")
    # print(per_starters.get(personality))
    return per_starters.get(personality)


def addScript(personality, text: dict):
    per_starters.get(personality).append(text)


def set_personality(personality):
    match personality:
        case "friendly":
            engine.setProperty('rate', 150)  # Adjust speaking rate (words per minute)
            engine.setProperty('volume', 6.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
        case "comedian":
            engine.setProperty('rate', 180)  # Adjust speaking rate (words per minute)
            engine.setProperty('volume', 1.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
        case "spongebob":
            engine.setProperty('rate', 200)  # Adjust speaking rate (words per minute)
            engine.setProperty('volume', 1.0)  # Adjust volume (0.0-1.0)
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
        case "gandalf":
            engine.setProperty('rate', 120)  # Adjust speaking rate (words per minute)
            engine.setProperty('volume', 0.8)  # Adjust volume (0.0-1.0)
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
        case "professor":
            engine.setProperty('rate', 100)  # Adjust speaking rate (words per minute)
            engine.setProperty('volume', 0.7)  # Adjust volume (0.0-1.0)
            engine.setProperty('language', 'en')  # Set language (e.g., 'en' for English)
        case _:
            # If the personality is not recognized, set a random personality
            random_personality = random.choice(["friendly", "formal", "quirky", "calm", "robotic"])
            print(f"Personality '{personality}' not recognized. Setting random personality: {random_personality}")
            set_personality(random_personality)


def talk_to() -> str:
    with sr.Microphone() as source:
        r = sr.Recognizer()

        # Adjust for backround -> maybe can use speaker for ready ambient?
        r.adjust_for_ambient_noise(source)
        # Adjust for basic control
        r.dyanmic_energythreshhold = 4000

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
            return "*Indecipherable*"
            # return str(Exception)
        print(":: ERR- FUNCTION OUT OF BOUNDS IN TALK_TO() ::")
        return "ERR"


def talk_back(words):
    engine.say(words)


def printslo(text: str):
    delay = engine.getProperty('rate') / 1000
    print(delay)

    sliced = text.split(" ")
    for w in sliced:
        time.sleep(delay)
        print(w)
    print("---")


if __name__ == "__main__":

    # Inside the main block
    for personality in personalities:
        print(f"Current personality: {personality}")
        user_input = talk_to()
        print("User input: " + user_input)

        if user_input.lower().strip() in ["quit", "exit", "bye"]:
            print("--Bye Bye--")
            break

        # message conversion to chat-gpt
        inp = {"role": "user", "content": user_input}

        # response setup for the chat
        set_personality(personality)
        response = chat_with_openai(personality, inp)

        # print("AI response: " + str(response))

        # Remove extra spaces from the response
        words = response.split()  # Split the text into words
        cleaned_words = [word.strip() for word in words]  # Remove extra spaces from each word
        response_cleaned = ' '.join(cleaned_words)  # Join the cleaned words back together

        # Output the responses using threading
        thread1 = threading.Thread(target=talk_back, name="Thread 1", daemon=False, args=(response_cleaned,))
        thread2 = threading.Thread(target=printslo, name="Thread 2", args=(response_cleaned,))

        thread1.start()
        thread2.start()

        # thread1.join()
        # thread2.join()
        engine.runAndWait()
        print("---EOR---")
        break

    print("-> That is all! <- ")

