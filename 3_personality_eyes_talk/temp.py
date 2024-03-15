import time
import threading

class Robot:
    def __init__(self):
        self.is_idle = True
        self.lock = threading.Lock()

    def move_arm(self):
        # Animation for moving arm
        with self.lock:
            print("Moving arm...")

    def turn_wheels(self):
        # Animation for turning wheels
        with self.lock:
            print("Turning wheels...")

    def talk(self, words):
        # Animation for talking
        with self.lock:
            print(f"Robot: {words}")

    def idle_animation(self):
        # Animation for idle state
        with self.lock:
            print("Idle animation...")

    def display_eyeballs(self):
        # Animation for displaying eyeballs
        with self.lock:
            print("Displaying eyeballs...")

    def perform_action(self, action, *args):
        if action == "move_arm":
            self.move_arm()
        elif action == "turn_wheels":
            self.turn_wheels()
        elif action == "talk":
            self.talk(*args)
        else:
            print("Unknown action")

    def action_thread(self, action, *args):
        thread = threading.Thread(target=self.perform_action, args=(action, *args))
        thread.start()

    def run(self):
        while True:
            if self.is_idle:
                self.idle_animation()
                self.display_eyeballs()
                time.sleep(2)  # Adjust the idle animation duration as needed
            else:
                # Example: Robot is asked to move arm and talk simultaneously
                self.action_thread("move_arm")
                self.action_thread("talk", "I'm performing multiple actions at once!")
                time.sleep(2)  # Adjust the duration between actions as needed
                self.is_idle = True  # Set robot to idle state after actions

if __name__ == "__main__":
    robot = Robot()
    robot.run()
