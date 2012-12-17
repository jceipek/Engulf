import pyshiva as ps
import random
import math

kinect_support = False
kinect = None


if kinect_support:
    import openni
    from kinect_skel import Kinect
    kinect = Kinect()

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)

    def __rmul__(self, other):
        return Vector(self.x*other, self.y*other)

    def __div__(self, other):
        return Vector(self.x/other, self.y/other)

    def __getitem__(self, key):
        return (self.x,self.y)[key]

    def mag(self):
        return ((self.x)**2+(self.y)**2)**0.5

    def dir(self):
        m = self.mag()
        return Vector(self.x/m, self.y/m)

    def __repr__(self):
        return str((self.x,self.y))

class Player(ps.Group):
    def __init__(self, world):
        ps.Group.__init__(self,x=world.window.width/2, y=world.window.height/2)
        #ps.Circle.__init__(self, x=world.window.width/2, y=world.window.height/2,
        #                  radius = 10, color=(0.2,0,1,0.5),
        #                  stroke_color=(1,1,1,1), stroke_thickness=2)
        self.border = ps.Circle(0,0,50,color=(0,0,0,0),stroke_color=(1,1,1,1),stroke_thickness=2)
        self.max_border = ps.Circle(0,0,50,color=(0,0,0,0),stroke_color=(1,1,1,0.1),stroke_thickness=4)
        self.add(self.max_border)
        self.add(self.border)
        self.contents = ps.Group(0,0)
        self.add(self.contents)
        self.radius = 30
        self.curr_max_radius = 30
        self.min_radius = 20
        for i in range(10):
            self.add_unit()
        self.world = world
        self.goal = Vector(0,0)

    def add_unit(self):
        if len(self.contents) < 100:
            self.contents.add(ps.Circle(x=0, y=0, radius=5, color=(0.2,0,1,0.5)))

    def remove_unit(self):
        if len(self.contents) > 3:
            self.contents.remove(self.contents[0])

    def simulate(self, dt):
        self.x, self.y = self.goal

        if self.x-self.radius < 0:
            self.x = self.radius
        if self.y-self.radius < 0:
            self.y = self.radius
        if self.x+self.radius > self.world.window.width:
            self.x = self.world.window.width-self.radius
        if self.y+self.radius > self.world.window.height:
            self.y = self.world.window.height-self.radius

        t = self.world.window.s_since_open()
        k = 0.25

        self.radius = min(self.curr_max_radius, self.radius)

        #todo: control with kinect
        self.radius = self.curr_max_radius/2

        self.border.radius = self.radius+5
        self.max_border.radius = self.curr_max_radius+5

        for (i,c) in enumerate(self.contents):
            c.x = self.radius*math.cos(k*(t*10+i))*math.sin(t+i)
            c.y = self.radius*math.sin(k*(t*10+i))*math.sin(t+i)

    def found_food(self):
        self.curr_max_radius += 5
        for i in range(10):
            self.add_unit()

    def hit_enemy(self):
        self.curr_max_radius -= 5
        self.curr_max_radius = max(self.curr_max_radius,self.min_radius)
        self.remove_unit()

    def set_radius(self,value):
        self.radius = max(min(value,self.curr_max_radius), self.min_radius)


class Enemy(ps.Circle):
    def __init__(self, world):
        x = random.randint(0,world.window.width)
        y = random.randint(0,world.window.height)
        ps.Circle.__init__(self, x=x, y=y,
                           radius = 5, color=(1,0,0,1), 
                           stroke_color=(1,1,1,1), stroke_thickness=2)
        self.world = world
        self.goal = Vector(0,0)
        self.acceleration = Vector(0,0)
        self.terminal_accel = 5
        self.accel_factor = 0.2
        self.accel_factor = random.random()

    def simulate(self, dt):

        self.goal.x = self.world.player.x
        self.goal.y = self.world.player.y
        #for a in avoid:
        #   if a != self:
        #       self.acc_x += distance(a.x,a.y,self.x,self.y)*0.1
        curr = Vector(self.x, self.y)
        d =  self.goal-curr
        self.acceleration += d.dir()*self.accel_factor
        #scale = 10
        #curr += d.dir()*dt*scale*(d.mag()*0.1)
        #self.x, self.y = curr

        if self.acceleration.mag() > self.terminal_accel:
            self.acceleration = self.acceleration.dir()*self.terminal_accel

        if self.x < 0 and self.acceleration.x<0:
            self.acceleration.x *= -1
        if self.y < 0 and self.acceleration.y<0:
            self.acceleration.y *= -1
        if self.x > self.world.window.width and self.acceleration.x>0:
            self.acceleration.x *= -1
        if self.y > self.world.window.height and self.acceleration.y>0:
            self.acceleration.y *= -1

        curr += self.acceleration
        self.x, self.y = curr

        player = self.world.player
        player_pos = Vector(player.x, player.y)
        curr_pos = Vector(self.x, self.y)
        nearness = curr_pos - player_pos
        if nearness.mag() < self.radius+player.radius:
            player.hit_enemy()
            #self.world.window.remove(self)

class Food(ps.Group):
    def __init__(self, world):
        self.world = world
        self.radius = 5
        x = random.randint(int(world.window.width*0.05),int(world.window.width*0.95))
        y = random.randint(int(world.window.height*0.05),int(world.window.height*0.95))
        ps.Group.__init__(self, x=x, y=y) 

        self.rect = ps.Rect(x=-self.radius,y=-self.radius,width=10,height=10, 
                            color=(0,1,0,1))
        self.call_to_action = ps.Rect(x=-self.radius*2,y=-self.radius*2,width=20,height=20,
                            color=(0,0,0,0),stroke_color=(0,1,0,1), stroke_thickness=1)
        self.add(self.rect)
        self.add(self.call_to_action)
        self.remove_me = False

    def simulate(self, dt):
        #self.call_to_action = ps.Rect(x=-self.radius*2,y=-self.radius*2,width=20,height=20,
        #                    color=(0,0,0,0),stroke_color=(0,1,0,1), stroke_thickness=1)

        t = self.world.window.s_since_open()
        side_length = abs(math.sin(t*5))*3.2+self.radius*3

        self.call_to_action.width = side_length
        self.call_to_action.height = side_length
        self.call_to_action.x = -side_length/2
        self.call_to_action.y = -side_length/2

        player = self.world.player
        player_pos = Vector(player.x, player.y)
        curr_pos = Vector(self.x, self.y)
        nearness = curr_pos - player_pos
        if nearness.mag() < self.radius+player.radius and not self.remove_me:
            self.color = (0,0,1)
            player.found_food()
            #self.world.add_new_food()
            self.remove_me = True

class World:
    def __init__(self, window):
        self.player = None
        self.enemies = []
        self.food = []
        self.window = window

    def add_player(self, player):
        self.player = player
        self.window.add(player)

    def add_new_enemy(self):
        e = Enemy(self)
        self.enemies.append(e)
        window.add(e)

    def add_new_food(self):
        e = Food(self)
        self.food.append(e)
        window.add(e)   

window = ps.Window("Engulf", width = 1024, height = 768)
world = World(window)

world.add_player(Player(world))

for i in range(10):
    world.add_new_enemy()

for i in range(3):
    world.add_new_food()

while window.is_open():
    t = window.s_since_refresh()
    
    x,y = (0,0)
    if not kinect:
        x,y = ps.get_mouse_pos()
    else:
        for person in kinect.people.values():
            hue = math.sin(round(person.head.point[2]/100))

            x = -(person.right_hand.point[0]+person.left_hand.point[0])/2.0-window.width/2.0
            y = (person.right_hand.point[1]+person.left_hand.point[1])/2.0+window.height/2.0
            #k = math.sin(round(person.head.point[0]/50))+0.01
            radius = math.sqrt((person.left_hand.point[0] - person.right_hand.point[0])**2 + (person.left_hand.point[1] - person.right_hand.point[1])**2)*0.002
            world.player.set_radius(radius)

    world.player.goal.x = x
    world.player.goal.y = y

    to_remove = list()
    for c in window:
        c.simulate(t)
    for e in world.food:
        if e.remove_me:
            to_remove.append(e)
    for e in to_remove:
        world.add_new_food()
        window.remove(e)
        world.food.remove(e)

    if kinect:
        kinect.refresh()
    window.refresh()