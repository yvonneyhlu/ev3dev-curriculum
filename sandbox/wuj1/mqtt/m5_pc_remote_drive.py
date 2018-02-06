#!/usr/bin/env python3
"""
This module is the mini-project for the MQTT unit.  This module will be running on your PC and communicating with the
m5_ev3_remote_drive.py module that is running on your EV3 (you have to write that module too, but it's easier).
Only the Tkinter GUI has been made for you.  You will need to implement all of the MQTT communication.  The goal is to
have a program running on your computer that can control the EV3.

You will need to have the following features:
  -- Clickable drive direction buttons to drive forward (up), backwards (down), left, right, and stop (space)
    -- Keyboard shortcut keys that behave the same as clicking the buttons (this has already been wired up for you)
  -- An entry box for the left and right drive motor speeds.
    -- If both become set to 900 all of the drive direction buttons will go fast, for example forward goes 900 900
    -- If both become set to 300 all of the drive direction buttons will go slower, for example reverse goes -300 -300
    -- If 500 then left does -500 500, which causes the robot to spin left (use half speed -250 250 if too fast)
    -- If set differently to say 600 left, 300 right the robot will drive and arc, for example forward goes 600 300
  -- In addition to the drive features there needs to be a clickable button for Arm Up and Arm Down
    -- There also need to be keyboard shortcut for Arm Up (u) and Arm Down (j).  Arm calibration is not required.

  -- Finally you need 2 buttons for ending your program:
    -- Quit, which stops only this program and allows the EV3 program to keep running
    -- Exit, which sends a shutdown message to the EV3, then ends it's own program as well.

You can start by running the code to see the GUI, but don't expect button clicks to do anything useful yet.

Authors: David Fisher and Jingwen Wu.
"""  # Done: 1. PUT YOUR NAME IN THE ABOVE LINE.

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    # Done: 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    # Done: 3. Implement the callbacks for the drive buttons. Set both the click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: forward(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Up>', lambda event: forward(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))


    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: left(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Left>', lambda event: left(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    # left_button and '<Left>' key

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: right(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Right>', lambda event: right(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))
    # right_button and '<Right>' key

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: back(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Down>', lambda event: back(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# Done: 4. Implement the functions for the drive button callbacks.

def forward(mqtt_client, left_speed, right_speed):
    print("move forward")
    mqtt_client.send_message("forward", [left_speed, right_speed])


def left(mqtt_client, left_speed, right_speed):
    print("move left")
    mqtt_client.send_message("left",[left_speed, right_speed])


def right(mqtt_client, left_speed, right_speed):
    print("move right")
    mqtt_client.send_message("right", [left_speed, right_speed])


def back(mqtt_client, left_speed, right_speed):
    print("go back")
    mqtt_client.send_message("back", [left_speed, right_speed])


def stop(mqtt_client):
    print("stop moving")
    mqtt_client.send_message("stop")


# TODO: 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
