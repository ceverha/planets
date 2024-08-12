import pygame, math, sys
import src.solar_system as solar

SCREEN_SIZE = (1920, 1080)

METEOR_SIZE = (8, 8)
NUM_METEORS = 500
METEOR_COLOR = pygame.Color(0, 255, 0)

BLACK = pygame.Color(0, 0, 0)

GRID_SIZE = 50

PLANET_SIZE = (100, 100)
NUM_PLANETS = 1
PLANET_COLOR = pygame.Color(0, 0, 255)

FRAME_RATE = 60

if __name__ == "__main__":
	
	pygame.init()
	
	screen = pygame.display.set_mode(SCREEN_SIZE)

	clock = pygame.time.Clock()

	# create solar system?
	solar_system = solar.SolarSystem(SCREEN_SIZE)

	# create moveable objects (meteors)
	solar_system.add_meteors(NUM_METEORS, METEOR_SIZE, METEOR_COLOR)
	# create objects with gravity (planets)
	solar_system.add_planets(NUM_PLANETS, PLANET_SIZE, PLANET_COLOR)
	# create background objects

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		# update positions of objects
		solar_system.move_objects()


		# clearing and drawing
		screen.fill(BLACK)
		for body in solar_system.get_objects():
			pygame.draw.circle(screen, body.color, body.rect.center, body.radius)

		pygame.display.flip()

		clock.tick(FRAME_RATE)
