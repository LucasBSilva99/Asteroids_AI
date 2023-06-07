import pygame
import constants
import math
from random import randint, uniform

class Asteroid():
    count = 0
    def __init__(self, position, radius_type):
        self.position = position
        self.vector, self.goal = self.generate_vector()
        self.radius_type = radius_type
        self.id = Asteroid.count
        Asteroid.count += 1
    
    def display(self, screen):
        pygame.draw.circle(screen, constants.WHITE, self.position, constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type], 1)

    def move_forward(self):
        self.position = [
            self.position[0] + self.vector[0],
            self.position[1] + self.vector[1]
            ]
    
    def __eq__(self, other):
        return self.id == other.id
    
    def border_intersect(self):
        return self.position[0] < 0 \
            or self.position[0] > constants.WIDTH \
            or self.position[1] < 0 \
            or self.position[1] > constants.HEIGHT

    def generate_vector(self):
        vector = [0, 0]
        if self.position[0] == 0:
            vector = [constants.WIDTH, randint(0, constants.HEIGHT)]
        elif self.position[0] == constants.WIDTH:
            vector = [0, randint(0, constants.HEIGHT)]
        elif self.position[1] == 0:
            vector = [randint(0, constants.WIDTH), constants.HEIGHT]
        elif self.position[1] == constants.HEIGHT:
            vector = [randint(0, constants.WIDTH), 0]
        else:
            vector = [randint(0, constants.WIDTH), randint(0, constants.HEIGHT)]
        return [
            uniform(constants.ASTEROID_MIN_SPEED, constants.ASTEROID_MAX_SPEED) * (vector[0] - self.position[0]),
            uniform(constants.ASTEROID_MIN_SPEED, constants.ASTEROID_MAX_SPEED) * (vector[1] - self.position[1])
            ], vector
    
    def collide_with_missile(self, missiles):
        for i in range(len(missiles)):
            if math.sqrt((missiles[i].position[0] - self.position[0]) ** 2 + (missiles[i].position[1] - self.position[1]) ** 2) < constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type] + constants.MISSILE_RADIUS:
                return i
        else:
            return None
    
    def take_damage(self, missile):
        if self.radius_type > 0:
            return [
                Asteroid([self.position[0] - constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type] / 2,  self.position[1] - constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type] / 2], self.radius_type - 1),
                Asteroid([self.position[0] + constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type] / 2,  self.position[1] + constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type] / 2], self.radius_type - 1)
                ]
        return []


    def collide_with_spaceship(self, spaceship):
        for i in range(len(spaceship.vertices)):
            mid_point = [
                (spaceship.vertices[i][0] + spaceship.vertices[(i + 1) % len(spaceship.vertices)][0]) / 2,
                (spaceship.vertices[i][1] + spaceship.vertices[(i + 1) % len(spaceship.vertices)][1]) / 2
                ]
            if math.sqrt((spaceship.vertices[i][0] - self.position[0]) ** 2 + (spaceship.vertices[i][1] - self.position[1]) ** 2) < constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type] \
                or math.sqrt((mid_point[0] - self.position[0]) ** 2 + (mid_point[1] - self.position[1]) ** 2) < constants.ASTEROID_POSSIBLE_RADIUS[self.radius_type]:
                return True
        return False