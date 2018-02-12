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
        assert self.pixy.connected

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
        print('goodbye')
        self.left_motor.stop()
        self.right_motor.stop()

    def loop_forever(self):
        """this method is used to avoid letting the robot finish until the 'end' command"""
        self.running = True
        while self.running:
            time.sleep(0.1)

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

        Type hints:
          :type robot: robo.Snatch3r
          :rtype: bool
        """

        # Done: 2. Create a BeaconSeeker object on channel 1.

        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # Done: 3. Use the beacon_seeker object to get the current heading and distance.
            current_heading = self.beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = self.beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.notforward()
            else:
                # Done: 4. Implement the following strategy to find the beacon.
                # If the absolute value of the current_heading is less than 2, you are on the right heading.
                #     If the current_distance is 0 return from this function, you have found the beacon!  return True
                #     If the current_distance is greater than 0 drive straight forward (forward_speed, forward_speed)
                # If the absolute value of the current_heading is NOT less than 2 but IS less than 10, you need to spin
                #     If the current_heading is less than 0 turn left (-turn_speed, turn_speed)
                #     If the current_heading is greater than 0 turn right  (turn_speed, -turn_speed)
                # If the absolute value of current_heading is greater than 10, then stop and print Heading too far off
                #
                # Using that plan you should find the beacon if the beacon is in range.  If the beacon is not in range your
                # robot should just sit still until the beacon is placed into view.  It is recommended that you always print
                # something each pass through the loop to help you debug what is going on.  Examples:
                #    print("On the right heading. Distance: ", current_distance)
                #    print("Adjusting heading: ", current_heading)
                #    print("Heading is too far off to fix: ", current_heading)

                # Here is some code to help get you started

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

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.notforward()
        return False
