import tkinter
from tkinter import ttk
import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com

COLOR_NAMES = ["Blue", "Green", "Yellow", "Red"]


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    """ Constructs a GUI with stuff on it. """
    print("--------------------------------------------")
    print(" Follow a line")
    print("--------------------------------------------")
    # ev3.Sound.speak("Follow a line").wait()
    # robot = robo.Snatch3r()
    # dc = DataContainer()
    mqtt_client = com.MqttClient()
    root = tkinter.Tk()
    mqtt_client.connect_to_ev3()

    # ------------------------------------------------------------------
    #
    #   ** put a Frame on the window. **
    # ------------------------------------------------------------------
    frame1 = ttk.Frame(root, padding=100)
    frame1.grid()
    # ------------------------------------------------------------------
    #   ** put a Button on the Frame. **

    # ------------------------------------------------------------------
    # DONE: 5. After reading and understanding the m3e module,
    #   ** make your Button respond to a button-press **
    #   ** by printing   "Hello"  on the Console.     **
    # ------------------------------------------------------------------
    # go_forward_button['command'] = (lambda:
    #                                  print('Hello'))
    # ------------------------------------------------------------------
    # DONE: 6. After reading and understanding the m4e module,
    #   -- Put an Entry box on the Frame.
    #   -- Put a second Button on the Frame.
    #   -- Make this new Button, when pressed, print "Hello"
    #        on the Console if the current string in the Entry box
    #        is the string 'ok', but print "Goodbye" otherwise.
    # ------------------------------------------------------------------
    # canvas = tkinter.Canvas(frame1, background="lightgray", width=800, height=500)
    dingk = tkinter.PhotoImage(file = 'tinky.gif')
    Dipsy = tkinter.PhotoImage(file='disy.gif')
    lala = tkinter.PhotoImage(file='lala.gif')
    po = tkinter.PhotoImage(file='po.gif')
    # put gif image on canvas
    # pic's upper left corner (NW) on the canvas is at x=50 y=10
    # canvas.create_image(200, 150, image=img )
    # canvas.grid(columnspan=2)
    welcom = ttk.Label(frame1, text = 'welcome to Teletubbie land!')
    welcom.grid(row = 0,column =1)
    welcom1 = ttk.Label(frame1, text='Who do you want to wake up?')
    welcom1.grid(row=1, column=1)

    Ding = ttk.Button(frame1, text = 'baby', image = dingk)
    Ding.grid(row=1, column = 0)
    Ding['command'] = lambda: drive_to_color(mqtt_client, ev3.ColorSensor.COLOR_BLUE)

    Disy = ttk.Button(frame1, image =Dipsy)
    Disy.grid(row=1, column = 2)
    Disy['command'] = lambda : drive_to_color(mqtt_client, ev3.ColorSensor.COLOR_GREEN)

    Lala = ttk.Button(frame1, image=lala)
    Lala.grid(row=2, column=0)
    Lala['command'] = lambda : time_to(mqtt_client)

    Po = ttk.Button(frame1, image=po)
    Po.grid(row=2, column=2)
    Po['command'] = lambda : drive_to_color(mqtt_client, ev3.ColorSensor.COLOR_RED)

    root.mainloop()


def drive_to_color(mqtt_client, color):
    print("Find the teletubbie!")
    mqtt_client.send_message("drive_to_color", [color])

def time_to(mqtt_client):
    print("work!")
    mqtt_client.send_message("time_to_sleep ", )




        # TODO: 4. Call over a TA or instructor to sign your team's checkoff sheet.
        #
        # Observations you should make, the instance variable robot.color_sensor.color is always updating
        # to the color seen and that value is given to you as an int.

        # ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()

###########################
main()