#!/usr/bin/python

"""
Copyright (c) 2012 Julian Ceipek.
Heavily based on jmendeth's PyOpenNI skeleton.py example.

------------------------------------------------------------------------------
This file is part of Engulf.

Engulf is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Engulf is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Engulf.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------------

An object-oriented adaptation of jmendeth's PyOpenNI skeleton.py example
for easy integration with PyShiva.

Usage:
k = Kinect() # Create a new connection to the Kinect for skeleton tracking

k.refresh() # Call this in the main application loop

k.people # A dictionary of ids to Person objects that each contain skeletal information.

"""

from openni import *

class PosConfNode:
    def __init__(self, pos, conf):
        self.point = pos
        self.confidence = conf


class Person:
    def __init__(self, ident):
        self.identifier = ident
        self.left_hand = PosConfNode((0,0,0),0)
        self.right_hand = PosConfNode((0,0,0),0)
        self.head = PosConfNode((0,0,0),0)

class Kinect:
    def __init__(self):
        self.people = dict()

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
        self.people[id] = Person(id)

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
        del self.people[id]

    def refresh(self):
        # Update to next frame
        self.ctx.wait_and_update_all()

        # Extract head position of each tracked user
        for id in self.user.users:
            if self.skel_cap.is_tracking(id):
                # Point , Confidence
                joint = self.skel_cap.get_joint_position(id, SKEL_HEAD)
                self.people[id].head = joint

                joint = self.skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
                self.people[id].right_hand = joint

                joint = self.skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
                self.people[id].left_hand = joint

    def get_people(self):
        return self.people