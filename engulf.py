import pyshiva as ps
import random

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

class Player(ps.Circle):
	def __init__(self, world):
		ps.Circle.__init__(self, x=world.window.width/2, y=world.window.height/2,
			               radius = 10, color=(0.2,0,1,0.5),
			               stroke_color=(1,1,1,1), stroke_thickness=2)
		self.world = world
		self.goal = Vector(0,0)

	def simulate(self, dt):
		#curr = Vector(self.x, self.y)
		#d = self.goal-curr
		#scale = 1000
		#curr += d.dir()*dt*scale
		#self.x, self.y = curr
		self.x, self.y = self.goal

		if self.x-self.radius < 0:
			self.x = self.radius
		if self.y-self.radius < 0:
			self.y = self.radius
		if self.x+self.radius > self.world.window.width:
			self.x = self.world.window.width-self.radius
		if self.y+self.radius > self.world.window.height:
			self.y = self.world.window.height-self.radius

	def found_food(self):
		self.radius *= 1.1

	def hit_enemy(self):
		self.radius *= 0.9

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
		#	if a != self:
		#		self.acc_x += distance(a.x,a.y,self.x,self.y)*0.1
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



class Food(ps.Rect):
	def __init__(self, world):
		self.world = world
		x = random.randint(0,world.window.width)
		y = random.randint(0,world.window.height)
		ps.Rect.__init__(self, x=x, y=y, width=5,
			               height=5, color=(0,1,0,1), 
			               stroke_color=(1,1,1,1), stroke_thickness=1)

	def simulate(self, dt):
		player = self.world.player
		player_pos = Vector(player.x, player.y)
		curr_pos = Vector(self.x, self.y)
		nearness = curr_pos - player_pos
		if nearness.mag() < self.height/2+player.radius:
			self.color = (0,0,1)
			player.found_food()
			self.world.window.remove(self)

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

window = ps.Window("Engulf")
world = World(window)

world.add_player(Player(world))

for i in range(10):
	world.add_new_food()
	world.add_new_enemy()

while window.is_open():
	t = window.s_since_refresh()
	
	x,y = ps.get_mouse_pos()

	world.player.goal.x = x
	world.player.goal.y = y

	for c in window:
		c.simulate(t)

	window.refresh()

