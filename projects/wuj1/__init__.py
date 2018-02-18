"""
Constructor: Valentine (Jingwen WU)
Date: 2/17/2018
Title: CSSE120 Final Project
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


"""Digital Toy ---- Peppa Pig"""
# This digital toy has four different functions that children can play with.


class PenData(object):
    def __init__(self):
        self.color = 'gray'
        self.mouse_position_x = None
        self.mouse_position_y = None
        self.is_dragging = False


class DataContainer(object):
    def __init__(self):
        self.running = True


def main():
    pen_data = PenData()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Peppa Pig")

    # construct a main frame as the control panel
    main_frame = ttk.Frame(root, padding=25, relief='sunken')
    main_frame.grid()

    # import peppa pig picture and use it as a button
    # when click on the picture, it prints words
    peppa_pig = tkinter.PhotoImage(file='pegga.gif')
    frame_pic = ttk.Button(main_frame, image=peppa_pig)
    frame_pic.image = peppa_pig
    frame_pic.grid(row=0, column=1)
    frame_pic['command'] = lambda: print('Hi! I am Peppa Pig! \r\nCome and play with me!')

    # build label of description of this toy
    title = ttk.Label(main_frame, text=' Peppa Pig',width=10,relief='groove', padding =5)
    title.grid(row=1, column=1)
    description = ttk.Label(main_frame, text='I am a smart digital toy to help kids think and learn!', padding =8)
    description.grid(row=2, column=1)

    # create a function called drawing which let kids draw beautiful pictures on control panel
    drawing = ttk.Label(main_frame, text="Let's us draw some beautiful pictures!", relief='groove', padding =5)
    drawing.grid(row=3, column=0)
    instruction1 = "Drag the left mouse to draw."
    drawing1 = ttk.Label(main_frame, text=instruction1)
    drawing1.grid(row=4, column=0)
    # create a canvas to show drawing
    canvas = tkinter.Canvas(main_frame, background='lightgray')
    canvas.grid(row=5, column=0)
    canvas.bind('<B1-Motion>',
                lambda event: left_mouse_drag(event, pen_data))
    canvas.bind('<B1-ButtonRelease>',
                lambda event: left_mouse_release(pen_data))
    # create a button to flip the color of pen
    flip = ttk.Button(main_frame, text='Flip pen color')
    flip.grid(row=6, column=0)
    flip['command'] = lambda: flip_pen_color(pen_data)
    # create a another function for kids to play which is the singing mode
    singing = ttk.Label(main_frame, text="Let's sing songs!", relief='groove', padding=5)
    singing.grid(row=3, column=1)
    instruction2 = "Press buttons on robot to listen to songs.\r\n"
    instruction2 = instruction2 + "When press up button, you can hear Bing Bong song.\r\n"
    instruction2 = instruction2 + "When press down button, you can hear Peppa Pig them song."
    singing1 = ttk.Label(main_frame, text=instruction2)
    singing1.grid(row=5, column=1)

    # create the third mode for kids to play which is the driving mode
    # there are four buttons controlling the movement of Peppa Pig
    speed= 700
    driving = ttk.Label(main_frame, text="Let's drive!", relief='groove', padding =5)
    driving.grid(row=3, column=3)
    forward_button = ttk.Button(main_frame, text='Forward')
    forward_button.grid(row=4, column=2)
    forward_button['command'] = lambda: forward(mqtt_client, speed, speed)
    left_button = ttk.Button(main_frame, text='Left')
    left_button.grid(row=4, column=4)
    left_button['command'] = lambda: left(mqtt_client, speed, speed)
    right_button=ttk.Button(main_frame, text='Right')
    right_button.grid(row=5,column=4)
    right_button['command'] = lambda: right(mqtt_client, speed, speed)
    stop_button = ttk.Button(main_frame, text='Stop')
    stop_button.grid(row=5, column=2)
    stop_button['command'] = lambda: stop(mqtt_client)

    # control the fourth mode for kids to play which is the seeking mode
    finding = ttk.Label(main_frame, text="Let's find George!", relief='groove', padding=5)
    finding.grid(row=3, column=5)
    instruction3 = "      I am playing hide and seek with my brother George!  "
    finding1 = ttk.Label(main_frame, text=instruction3)
    finding1.grid(row=4, column=5)
    george = tkinter.PhotoImage(file='george.gif')
    george_pic = ttk.Button(main_frame, image=george)
    george_pic.image = george_pic
    george_pic.grid(row=5, column=5)
    george_pic['command'] = lambda: print('Hi! I am Goerge! \r\nLet us play hide and seek!')
    playing = ttk.Button(main_frame, text='Play hide-and-seek')
    playing.grid(row=6,column=5)
    playing['command'] = lambda: seek_george(mqtt_client)

    root.mainloop()


def forward(mqtt_client, left_speed, right_speed):
    print("move forward")
    mqtt_client.send_message("forward", [left_speed, right_speed])


def left(mqtt_client, left_speed, right_speed):
    print("move left")
    mqtt_client.send_message("left",[left_speed, right_speed])


def right(mqtt_client, left_speed, right_speed):
    print("move right")
    mqtt_client.send_message("right", [left_speed, right_speed])


def stop(mqtt_client):
    print("stop moving")
    mqtt_client.send_message("notforward")


def left_mouse_drag(event, data):
    canvas = event.widget
    if data.is_dragging:
        canvas.create_line(data.mouse_position_x, data.mouse_position_y,
                           event.x, event.y,
                           fill=data.color, width=3)
    else:
        data.is_dragging = True

    data.mouse_position_x = event.x
    data.mouse_position_y = event.y


def left_mouse_release(data):
    data.is_dragging = False


def flip_pen_color(data):
    if data.color == 'gray':
        data.color = 'pink'
    else:
        data.color = 'gray'


def seek_george(mqtt_client):
    print('Play hide-and-seek with George')
    mqtt_client.send_message("play")


main()


