from asteroid import Asteroid
import constants
import math
from random import randint
import pygame
from spaceship import Spaceship

class Game():
    def __init__(self):
        self.asteroids = []
        self.missiles = []
        self.spaceship = Spaceship()
        self.score = 0
        self.running = True
    
    def display(self, screen):
        screen.fill(constants.BLACK)

         # Display spaceship
        self.spaceship.display(screen)

        # Display missiles
        for i in range(len(self.missiles)):
            self.missiles[i].display(screen)

        # Display asteroids
        for i in range(len(self.asteroids)):
            self.asteroids[i].display(screen)
        
        # Display score
        font = pygame.font.Font(None, 40)
        text = font.render('Score: ' + str(self.score), 1, constants.WHITE)
        screen.blit(text, (10, 10))
    
    def update(self, closest_asteroids):
        fitness = 0.0
        # Update missiles
        i = 0
        while i < len(self.missiles):
            self.missiles[i].move_forward()
            if self.missiles[i].border_intersect():
                self.missiles.pop(i)
                fitness -= 0.5
            else:
                i += 1
        # Update asteroids
        # self.spawn_asteroids()
        i = 0
        while i < len(self.asteroids):
            self.asteroids[i].move_forward()
            if self.asteroids[i].border_intersect():
                self.asteroids.pop(i)
            else:
                if self.asteroids[i].collide_with_spaceship(self.spaceship):
                    fitness -= 100.0
                    self.running = False
                collision = self.asteroids[i].collide_with_missile(self.missiles)
                if collision != None:
                    fitness += 1.0
                    if self.asteroids[i] in closest_asteroids:
                        fitness += 10.0
                    missile_hit = self.missiles.pop(collision)
                    asteroid_hit = self.asteroids.pop(i)
                    self.asteroids += asteroid_hit.take_damage(missile_hit)
                    self.score += 1
                else:
                    i += 1
        return fitness
    
    def key_pressed(self, events, keys):
        # Keys pressed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.rotate_left()
                if event.key == pygame.K_RIGHT:
                    self.spaceship.rotate_right()
                if event.key == pygame.K_SPACE:
                    missile = self.spaceship.shoot_missile()
                    if missile != None:
                        self.missiles.append(missile)
                if event.type == pygame.QUIT:
                    pygame.quit()
        if keys[pygame.K_UP]:
            self.spaceship.move_forward()
        if keys[pygame.K_LEFT]:
            self.spaceship.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.spaceship.rotate_right()
    
    def spawn_asteroids(self):
        required_asteroids = constants.NUM_ASTEROIDS - len(self.asteroids)
        if required_asteroids > 0:
            for _ in range(required_asteroids):
                radius_type = randint(0, len(constants.ASTEROID_POSSIBLE_RADIUS) - 1)
                while True:
                    possible_start_positions = [
                        [0, randint(0, constants.HEIGHT)],
                        [constants.WIDTH, randint(0, constants.HEIGHT)],
                        [randint(0, constants.WIDTH), 0],
                        [randint(0, constants.WIDTH), constants.HEIGHT]
                        ]
                    position = possible_start_positions[randint(0, len(possible_start_positions) - 1)]
                    if math.sqrt((position[0] - self.spaceship.center[0]) ** 2 + (position[1] - self.spaceship.center[1]) ** 2) >= constants.DISTANCE_TO_SPAWN:
                        self.asteroids.append(Asteroid(position, radius_type))
                        break
    
    def move(self, net_output, gen):
        if net_output[0] > 0.95:
            self.spaceship.move_forward()
        if net_output[1] > 0.95:
            self.spaceship.rotate_left()
        if net_output[2] > 0.95:
            self.spaceship.rotate_right()
        if net_output[3] > 0.95 and gen >= constants.SHOOT_GEN:
            missile = self.spaceship.shoot_missile()
            if missile != None:
                self.missiles.append(missile)

        
