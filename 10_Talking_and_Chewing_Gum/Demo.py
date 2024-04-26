import time

from .. import Kore
import random
import Pose_Lib as Pl
import threading
import pyttsx3

text = "It is not the critic who counts; not the man who points out how the strong man stumbles, or where the doer of deeds could have done them better. The credit belongs to the man who is actually in the arena, whose face is marred by dust and sweat and blood; who strives valiantly; who errs, who comes short again and again, because there is no effort without error and shortcoming; but who does actually strive to do the deeds; who knows great enthusiasms, the great devotions; who spends himself in a worthy cause; who at the best knows in the end the triumph of high achievement, and who at the worst, if he fails, at least fails while daring greatly, so that his place shall never be with those cold and timid souls who neither know victory nor defeat."

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)


def speak_text(text):
    engine.say(text)


def pose():
    stop_flag = False
    random_pose_key = Pl.get_random_pose_key(Pl.all_poses)
    print("Random starter pose from 'all_poses': ", random_pose_key)
    startpose = Pl.all_poses.get(random_pose_key)
    kore.update(startpose)

    while not stop_flag:
        random_pose_key2 = Pl.get_random_pose_key(Pl.all_poses)
        print("Random starter pose from 'all_poses': ", random_pose_key2)
        endpose = Pl.all_poses.get(random_pose_key2)

        # random choice of transition
        random_number = random.randint(1, 3)
        if random_number == 1:  # Go direct
            kore.update(endpose)
            time.sleep(random.randint(1000, 3000))
            startpose = kore.send_values()
            continue
        elif random_number == 2:  # Go fivesteps
            steps: list = Pl.fiveStep(startpose, endpose)
            for s in steps:
                kore.update(s)
                time.sleep(50)
                startpose = kore.send_values()
            continue
        elif random_number == 3:  # Go back after a random amount of time
            kore.update(endpose)
            time.sleep(random.randint(1000, 5000))
            kore.update(startpose)
            continue
        else:
            continue



if __name__ == "__main__":
    kore = Kore()
    kore.update(kore.tango_default)
    #
    # ## threads: speaking thread and posing thread
    #
    # speechThread = threading.Thread(target=speak_text, args=(text,))
    #
    # poseThread = threading.Thread(target=pose, args=())
    #
    # # run both threads, but finish and exit when speech is done
    # speechThread.start()
    #
    # # dramatic pause
    # time.sleep(3000)
    #
    # poseThread.start()
    #
    # engine.runAndWait()     #after ending the speech, reset the funtions
    # print("\n\n---End of program---\n\n")
    # kore.update(kore.tango_default)

    # testing code
    print("Testing\n")
    kore.update(Pl.all_poses.get(Pl.get_random_pose_key(Pl.all_poses)))
