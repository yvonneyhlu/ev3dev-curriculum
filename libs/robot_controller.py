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

import time
import math

MAX_SPEED = 900


class Snatch3r(object):

    def __init__(self):

        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.touch_sensor = ev3.TouchSensor()

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        assert self.ir_sensor
        assert self.arm_motor
        assert self.touch_sensor
        assert self.left_motor
        assert self.right_motor
        assert self.color_sensor
        assert self.beacon_seeker
        assert self.pixy
        self.pixy.mode = "SIG1"

    def drive_inches(self, length, speed_deg_per_second):
        """this method is used to drive the robot by setting inches it need to drive"""
        self.left_motor.run_to_rel_pos(position_sp = length * 90, speed_sp = speed_deg_per_second, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp= length * 90, speed_sp=speed_deg_per_second,stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """this method is uesd to turn the robot by degrees"""
        self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 450 / 90 , speed_sp=turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 450 / 90, speed_sp=turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_calibration(self):
        """this method is uesd to calibrate the arm of robot"""
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=MAX_SPEED, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        """this method is used to move the arm up"""
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        """this method is used to move the arm down"""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def shutdown(self):
        """this method is used to shut down the robot"""
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def forward(self, left_speed, right_speed):
        """this method is used to drive the robot forward"""
        print('go forward')
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.run_forever(speed_sp=left_speed)

    def left(self, left_speed, right_speed):
        """this method is used to turn robot to the left"""
        print('go left')
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.run_forever(speed_sp=-left_speed)

    def right(self, left_speed, right_speed):
        """this method is used to turn robot to the right"""
        print('go right')
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(speed_sp=left_speed)

    def back(self, left_speed, right_speed):
        """this method is used to drive the robot backward"""
        print('go back')
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(speed_sp=-left_speed)

    def notforward(self):
        """this method is used to stop robot from moving"""
        self.left_motor.stop()
        self.right_motor.stop()

    def loop_forever(self):
        """this method is used to avoid letting the robot finish until the 'end' command"""
        self.running = True
        while self.running:
            time.sleep(0.1)

    def seek_beacon(self):
        """this method is used to seek beacon and drive toward it """
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.notforward()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance == 0:
                        print("You have found the beacon!")
                        self.forward(100,100)
                        time.sleep(0.03)
                        self.notforward()
                        time.sleep(0.01)

                        return True
                    if current_distance > 0:
                        print("drive forward")
                        self.forward(forward_speed, forward_speed)
                if math.fabs(current_heading) >= 2 and math.fabs(current_heading) < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        print("spin left")
                        self.left(turn_speed, turn_speed)
                    if current_heading > 0:
                        print("spin right")
                        self.right(turn_speed, turn_speed)
                if math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix", current_heading)
                    self.notforward()
                    time.sleep(0.01)

            time.sleep(0.2)
        print("Abandon ship!")
        self.notforward()
        return False

    def play(self):
        """this method is used to seek George and find him"""
        forward_speed = 400
        turn_speed = 200

        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("I can't find George")
                ev3.Sound.speak("I can't find George")
                self.notforward()
            else:
                if math.fabs(current_heading) < 2:
                    print("George is on the right. Distance: ", current_distance)
                    if current_distance == 0:

                        self.forward(100, 100)
                        time.sleep(0.03)
                        self.notforward()
                        time.sleep(0.01)
                        print("Find George!")
                        ev3.Sound.speak("I found George! Hooray!")
                        break
                    if current_distance > 0:
                        print("Keep moving")
                        self.forward(forward_speed, forward_speed)
                if math.fabs(current_heading) >= 2 and math.fabs(current_heading) < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        print("spin left")
                        self.left(turn_speed, turn_speed)
                    if current_heading > 0:
                        print("spin right")
                        self.right(turn_speed, turn_speed)
                if math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix", current_heading)
                    self.notforward()
                    time.sleep(0.01)

            time.sleep(0.2)
        print("Finish playing!")
        self.notforward()
