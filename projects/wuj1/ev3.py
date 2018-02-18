"""
Constructor: Valentine (Jingwen WU)
Date: 2/17/2018
Title: CSSE120 Final Project
"""

import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com
import robot_controller as robo


class DataContainer(object):
    def __init__(self):
        self.running = True


def main():
    print('-------Final Project-----------')
    dc = DataContainer()
    btn = ev3.Button()

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # robot.loop_forever()

    btn.on_up = handle_up_button
    btn.on_down = handle_down_button

    while dc.running:
        btn.process()  # This command is VERY important when using button callbacks!
        time.sleep(0.01)  # A short delay is important to allow other things to happen.

    robot.loop_forever()


def handle_up_button(button_state):
    if button_state:
        print("Play Bing Bong song")
        ev3.Sound.play("/home/robot/csse120/assets/sounds/Bingbong.wav")


def handle_down_button(button_state):
    if button_state:
        print("Play Peppa Pig theme song")
        ev3.Sound.play("/home/robot/csse120/assets/sounds/peppa.wav")


main()
