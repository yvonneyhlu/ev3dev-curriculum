import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time
COLOR_NAMES = ["Blue", "Green", "Yellow", "Red"]

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
     # Calls a function that has a while True: loop within it to avoid letting the program end.
    ev3.Sound.speak("welcome to teletubbie land")
    # robot.arm_calibration()
    dc = DataContainer()
    btn = ev3.Button()
    btn.on_up = handle_button_up
    btn.on_backspace = handle_button_back
    while dc.running:

        btn.process()
        time.sleep(0.02)
    robot.loop_forever()


def handle_button_up(button_state):
    if button_state:
        robot = robo.Snatch3r()
        robot.forward(600, 600)


def handle_button_back(button_state):
    if button_state:
        robot = robo.Snatch3r()
        robot.notforward()


main()