import pygame, math, random

# with collisions, beautiful circle at c = 130, max_speed = 20
COEFFICIENT_OF_GRAVITY = 130
MAX_SPEED = 22
NON_ZERO = 0.0001
MIN_ACCEL = 0.05

class Planet:
	def __init__(self, pos, size, color):
		self.rect = pygame.Rect(pos, size)
		self.color = color
		self.radius = math.sqrt(((size[0]/2)**2)*2)
	
	def change_color(self):
		new_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		self.color = new_color

class Meteor:
	def __init__(self, pos, vel, size, color):
		self.rect = pygame.Rect(pos, size)
		self.vel = pygame.math.Vector2(vel)
		self.color = color
		self.radius = math.sqrt(((size[0]/2)**2)*2)

	def update_velocity_from_gravity(self, planet):
		# gravity
		y = planet.rect.centery - self.rect.centery
		x = planet.rect.centerx - self.rect.centerx
		if x == 0:
			x = NON_ZERO
		theta = math.atan(abs(y/x))
		dx = math.cos(theta)
		if self.rect.centerx < planet.rect.centerx:
			dx *= -1
		dy = math.sin(theta)
		if self.rect.centery < planet.rect.centery:
			dy *= -1
		gravity_factor = COEFFICIENT_OF_GRAVITY / pygame.Vector2(x, y).length()
		
		if gravity_factor < MIN_ACCEL:
			gravity_factor = MIN_ACCEL
		
		velocity = pygame.Vector2(dx, dy) * gravity_factor
		self.vel = self.vel - velocity
		if self.vel.length() > MAX_SPEED:
			self.vel.scale_to_length(MAX_SPEED)
		
		self.change_color()

	def update_velocity_from_collisions(self, planet):
		if self.rect.colliderect(planet.rect):
			# calculate normal vector 
			y = planet.rect.centery - self.rect.centery
			if y == 0:
				y = NON_ZERO
			x = planet.rect.centerx - self.rect.centerx
			if x == 0:
				x = NON_ZERO
			normal = pygame.Vector2(x , y)
			self.vel = self.vel.reflect(normal)
			# move the meteor to the edge of the planet
			normal.scale_to_length(planet.radius + self.radius)
			self.rect.centerx = planet.rect.centerx - normal[0]
			self.rect.centery = planet.rect.centery - normal[1]
			return True
		else:
			return False

			
	# scale color based on velocity
	def change_color(self):
		scalar = MAX_SPEED / 255
		speed = self.vel.length()
		z = int(speed / scalar)
		new_color = pygame.Color(z, z, z)
		self.color = new_color

		

class SolarSystem:
	def __init__(self, size):
		self.size = size
		self.meteors = []
		self.planets = []

	def add_planets(self, num, p_size, color):
		x_separator = self.size[0] / (num + 1)
		y_separator = self.size[1] / (num + 1)
		
		for i in range(num):
			x = (i + 1) * x_separator
			y = (i + 1) * y_separator
			planet = Planet((x, y), p_size, color)
			planet.rect.center = (x, y)
			self.planets.append(planet)

	# add meteors to the solar system randomly positioned
	def add_meteors(self, num, m_size, color):
		for i in range(num):
			x = random.randrange(100, 1800, 1)
			y = random.randrange(100, 1001, 900)
			dx, dy = 0, 0
			meteor = Meteor((x, y), (dx, dy), m_size, color)
			self.meteors.append(meteor)

	# return all objects for use in drawing		
	def get_objects(self):
		return self.meteors + self.planets

	# move all objects and 
	# calculate new velocities based on gravity for all meteors based on the sum
	# of the acceleration vectors from each planet and collisions with
	# boundaries and planets and other meteors
	def move_objects(self):
		for meteor in self.meteors:
			
			# move the object
			meteor.rect = meteor.rect.move(meteor.vel)

			# boundaries
			if meteor.rect.left < 0:
				meteor.rect.left = 0
				meteor.vel = meteor.vel.reflect((1,0))
			if meteor.rect.right > self.size[0]:
				meteor.rect.right = self.size[0]
				meteor.vel = meteor.vel.reflect((1,0))
			if meteor.rect.top < 0:
				meteor.rect.top = 0
				meteor.vel = meteor.vel.reflect((0,1))
			if meteor.rect.bottom > self.size[1]:
				meteor.rect.bottom = self.size[1]
				meteor.vel = meteor.vel.reflect((0,1))

			# gravity
			# planetary collisions
			for planet in self.planets:
				meteor.update_velocity_from_gravity(planet)
				if meteor.update_velocity_from_collisions(planet):
					planet.change_color()



