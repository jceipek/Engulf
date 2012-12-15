from openni import *

class Kinect:
    def __init__(self):
        self.hand_start = (0,0,0)
        self.hand_loc = (0,0,0)

        self.context = Context()
        self.context.init()

        self.depth_generator = DepthGenerator()
        self.depth_generator.create(self.context)
        self.depth_generator.set_resolution_preset(RES_VGA)
        self.depth_generator.fps = 30

        self.gesture_generator = GestureGenerator()
        self.gesture_generator.create(self.context)
        self.gesture_generator.add_gesture('Wave')

        self.hands_generator = HandsGenerator()
        self.hands_generator.create(self.context)

        # Register the callbacks
        self.gesture_generator.register_gesture_cb(self.gesture_detected, self.gesture_progress)
        self.hands_generator.register_hand_cb(self.create, self.update, self.destroy)

        # Start generating
        self.context.start_generating_all()

    # Declare the callbacks
    # gesture
    def gesture_detected(self, src, gesture, id, end_point):
        print "Detected gesture:", gesture
        self.hands_generator.start_tracking(end_point)
    # gesture_detected

    def gesture_progress(self, src, gesture, point, progress): pass
    # gesture_progress

    def create(self, src, id, pos, time):
        print 'Create ', id, pos
        self.hand_start = (pos[0],pos[1],pos[2])
    # create

    def update(self, src, id, pos, time):
        print 'Update ', id, pos
        self.hand_loc = pos
        #circ.x = pos[0]*-1*0.5
        #circ.y = pos[1]*0.5
        self.hand_loc = (self.hand_start[0]-pos[0],
                         pos[1] - self.hand_start[1],
                         (self.hand_start[2]-pos[2])*0.3+100)
    # update

    def destroy(self, src, id, time):
        print 'Destroy ', id
    # destroy

    def refresh(self):
        self.context.wait_any_update_all()

    def get_pos_from_window(self, window):
        x = self.hand_loc[0] + window.width/2
        y = self.hand_loc[1] + window.width/2
        z = self.hand_loc[2]
        return x,y,z