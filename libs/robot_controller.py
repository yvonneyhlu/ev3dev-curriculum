"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3

import math
import time

MAX_SPEED = 900



class Snatch3r(object):


    def __init__(self):

        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.touch_sensor = ev3.TouchSensor()

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)

        assert self.arm_motor
        assert self.touch_sensor
        assert self.left_motor
        assert self.right_motor

    def drive_inches(self, length, speed_deg_per_second):
        self.left_motor.run_to_rel_pos(position_sp = length * 90, speed_sp = speed_deg_per_second, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp= length * 90, speed_sp=speed_deg_per_second,stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):

        self.left_motor.run_to_rel_pos(position_sp= - degrees_to_turn * 450 / 90 , speed_sp=turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp= degrees_to_turn * 450 / 90, speed_sp=turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 90
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=MAX_SPEED,
                                 stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def shutdown(self):
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()
