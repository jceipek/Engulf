#!/usr/bin/python
## The equivalent of:
##  "Working with the Skeleton"
## in the OpenNI user guide.

"""
This shows how to identify when a new user is detected, look for a pose for
that user, calibrate the users when they are in the pose, and track them.

Specifically, it prints out the location of the users' head,
as they are tracked.
"""

from openni import *

class Kinect:
    def __init__(self):
        self.head_pos_conf = ((0,0,0), 0)
        self.hand_left_pos_conf = ((0,0,0), 0)
        self.hand_right_pos_conf = ((0,0,0), 0)

        # Pose to use to calibrate the user
        self.pose_to_use = 'Psi'

        self.ctx = Context()
        self.ctx.init()

        # Create the user generator
        self.user = UserGenerator()
        self.user.create(self.ctx)

        # Obtain the skeleton & pose detection capabilities
        self.skel_cap = self.user.skeleton_cap
        self.pose_cap = self.user.pose_detection_cap

        # Register them
        self.user.register_user_cb(self.new_user, self.lost_user)
        self.pose_cap.register_pose_detected_cb(self.pose_detected)
        self.skel_cap.register_c_start_cb(self.calibration_start)
        self.skel_cap.register_c_complete_cb(self.calibration_complete)

        # Set the profile
        self.skel_cap.set_profile(SKEL_PROFILE_ALL)

        # Start generating
        self.ctx.start_generating_all()
        print "0/4 Starting to detect users. Press Ctrl-C to exit."

    # Declare the callbacks
    def new_user(self, src, id):
        print "1/4 User {} detected. Looking for pose..." .format(id)
        self.pose_cap.start_detection(self.pose_to_use, id)

    def pose_detected(self, src, pose, id):
        print "2/4 Detected pose {} on user {}. Requesting calibration..." .format(pose,id)
        self.pose_cap.stop_detection(id)
        self.skel_cap.request_calibration(id, True)

    def calibration_start(self, src, id):
        print "3/4 Calibration started for user {}." .format(id)

    def calibration_complete(self, src, id, status):
        if status == CALIBRATION_STATUS_OK:
            print "4/4 User {} calibrated successfully! Starting to track." .format(id)
            self.skel_cap.start_tracking(id)
        else:
            print "ERR User {} failed to calibrate. Restarting process." .format(id)
            self.new_user(self.user, id)

    def lost_user(self, src, id):
        print "--- User {} lost." .format(id)



    def refresh(self):
        # Update to next frame
        self.ctx.wait_and_update_all()

        # Extract head position of each tracked user
        for id in self.user.users:
            if self.skel_cap.is_tracking(id):
                head = self.skel_cap.get_joint_position(id, SKEL_HEAD)
                hand_left = self.skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
                hand_right = self.skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
                print "  {}: hand_left at ({loc[0]}, {loc[1]}, {loc[2]}) [{conf}]" .format(id, loc=hand_left.point, conf=hand_left.confidence)
                
                self.head_pos = (head.point, head.confidence)
                self.hand_left_pos = (head.point, head.confidence)
                self.head_pos = (head.point, head.confidence)

                self.head_pos_conf = (head.point, head.confidence)
                self.hand_left_pos_conf = (hand_left.point, hand_left.confidence)
                self.hand_right_pos_conf = (hand_right.point, hand_right.confidence)

    def get_pos_from_window(self, window):
        return self.head_pos_conf, self.hand_left_pos_conf, self.hand_right_pos_conf