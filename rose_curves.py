#
# Colorful Rose Curves Demo
#

# Import the python module
from kinect_skel import Kinect
import pyshiva as ps
import math, random
import colorsys


kinect = Kinect()
w = ps.Window(title = "Colorful Rose Curves")

# Create 1000 circles with different colors
for i in range(300):
    r = random.random()
    a = abs(math.cos(i))*0.5
    radius = abs(math.sin(i))*25
    c = ps.Circle(x = 0, y = 0, radius = radius, color = (r,abs(math.sin(i)),1,0.1))
    w.add(c) # Add the circles to the window.

k = 0.25 # k is the type of rose curve
k = 0.123

t = 0

while w.is_open():
    head_pos_conf, hand_left_pos_conf, hand_right_pos_conf = kinect.get_pos_from_window(w)
    ((x,y,z),conf) = hand_left_pos_conf
    ((x_r,y_r,z_r),conf) = hand_right_pos_conf
    ((x_h,y_h,z_h),conf) = head_pos_conf
    t = w.s_since_open()*2 # Use a scaled time since program start as the parametric time value
    #radius = abs(math.sin(w.s_since_open()))
    #radius = min(z/-10.0,1)
    #t += y/abs(y+0.001)
    #radius = min(1-(z_r-500)/1000,1) # was good
    radius = math.sqrt((x_r - x)**2 + (y_r - y)**2)*0.002

    x_pos = ((1.0)*(0 - x))+(radius/2.0)+w.width/2.0
    y_pos = ((-1.0)*(0 - y))+(radius/2.0)+w.height/2.0

    #print radius
    #if radius < 0.01: # Every time the curve collapses...
    #    k = random.random() # Randomize the k value to change the type of the curve
    k = math.sin(round(x_h/50))+0.01
    # Place every circle along a rose curve, offset by its index

    for (i,c) in enumerate(w):
        ran = random.random()
        c.x = x_pos+radius*math.cos(k*(t+i))*math.sin(t+i)*w.width/2
        c.y = y_pos+radius*math.sin(k*(t+i))*math.sin(t+i)*w.height/2
        hue = math.sin(round(z_h/100))
        sat = 0.9 #math.sin(round(x/100))
        brt = 0.8 #math.sin(round(y/100))
        c.color.values = colorsys.hsv_to_rgb(hue,sat,brt)#(math.cos(t/10.0), math.sin(t/10.0), math.sin(ran*i)/2.0 + .5, 0.1)

    
    # Update the screen
    kinect.refresh()
    w.refresh()