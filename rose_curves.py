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


hue = 0.0 
sat = 0.9 #math.sin(round(x/100))
brt = 0.8 #math.sin(round(y/100))

x_pos = w.width/2.0 
y_pos = w.height/2.0 

radius = 0.1

while w.is_open():
    for person in kinect.people.values():

        hue = math.sin(round(person.head.position[2]/100))

        x_pos = (person.right_hand.point[0]+person.left_hand.point[0])/2.0+w.width/2.0
        y_pos = (person.right_hand.point[1]+person.left_hand.point[1])/2.0+w.height/2.0
        k = math.sin(round(person.head.point[0]/50))+0.01
        radius = math.sqrt((person.left_hand.point[0] - person.right_hand.point[0])**2 + (person.left_hand.point[1] - person.right_hand.point[1])**2)*0.002

    t = w.s_since_open()*2 # Use a scaled time since program start as the parametric time value

    for (i,c) in enumerate(w):
        ran = random.random()
        c.x = x_pos+radius*math.cos(k*(t+i))*math.sin(t+i)*w.width/2
        c.y = y_pos+radius*math.sin(k*(t+i))*math.sin(t+i)*w.height/2
        c.color.values = colorsys.hsv_to_rgb(hue,sat,brt)#(math.cos(t/10.0), math.sin(t/10.0), math.sin(ran*i)/2.0 + .5, 0.1)

    # Update the screen
    kinect.refresh()
    w.refresh()