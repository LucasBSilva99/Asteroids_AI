import pygame
import constants
import math
from missile import Missile
import time
import numpy as np

class Spaceship():
    def __init__(self):
        self.vertices = [
            [constants.WIDTH / 2, (constants.HEIGHT / 2) + (constants.SPACESHIP_HEIGHT / 2)],
            [(constants.WIDTH / 2) - (constants.SPACESHIP_WIDTH / 2), (constants.HEIGHT / 2) - (constants.SPACESHIP_HEIGHT / 2)],
            [(constants.WIDTH / 2) + (constants.SPACESHIP_WIDTH / 2), (constants.HEIGHT / 2) - (constants.SPACESHIP_HEIGHT / 2)]
            ]
        self.vector = []
        self.center = [(constants.WIDTH / 2), (constants.HEIGHT / 2)]
        self.last_shoot_time = time.time() - constants.TIME_BETWEEN_SHOOTS
        self.angle = 270
    
    def display(self, screen):
        pygame.draw.polygon(screen, constants.WHITE, self.vertices, 1)
        if constants.DRAW_CENTER:
            pygame.draw.circle(screen, constants.RED, self.center, constants.CENTER_RADIUS)
    
    def rotate_right(self):
        self.angle -= constants.SPACESHIP_ROTATION_SPEED
        if self.angle < 0:
            self.angle += 360
        self.rotate(constants.SPACESHIP_ROTATION_SPEED)

    def rotate_left(self):
        self.angle += constants.SPACESHIP_ROTATION_SPEED
        if self.angle >= 360:
            self.angle -= 360
        self.rotate(-constants.SPACESHIP_ROTATION_SPEED)
    
    def move_forward(self):
        vector = [
            constants.SPACESHIP_SPEED * (self.vertices[0][0] - self.center[0]),
            constants.SPACESHIP_SPEED * (self.vertices[0][1] - self.center[1])
            ]
        self.vector = [(self.vertices[0][0] - self.center[0]),
                        (self.vertices[0][1] - self.center[1])]
        self.center = [
            self.center[0] + vector[0],
            self.center[1] + vector[1],
            ]
        for i in range(len(self.vertices)):
            self.vertices[i] = [
            self.vertices[i][0] + vector[0],
            self.vertices[i][1] + vector[1],
            ]
        self.border_intersect()

    def rotate(self, angle_turn):
        angle = math.radians(angle_turn)

        for i in range(len(self.vertices)):
            # Translate to center
            self.vertices[i] = [
                self.vertices[i][0] - self.center[0], 
                self.vertices[i][1] - self.center[1]
                ]
            # Rotate
            self.vertices[i] = [
                self.vertices[i][0] * math.cos(angle) - self.vertices[i][1] * math.sin(angle),
                self.vertices[i][0] * math.sin(angle) + self.vertices[i][1] * math.cos(angle)
                ]
            # Translate the same distance as before
            self.vertices[i] = self.vertices[i][0] + self.center[0], self.vertices[i][1] + self.center[1]
    
    def border_intersect(self):
        add_x = 0
        add_y = 0
        # Moving horizontally
        if self.center[0] < 0:
            add_x = constants.WIDTH
        elif self.center[0] > constants.WIDTH:
            add_x = -constants.WIDTH
        # Moving vertically
        if self.center[1] < 0:
            add_y = constants.HEIGHT
        elif self.center[1] > constants.HEIGHT:
            add_y = -constants.HEIGHT
        if add_x != 0 or add_y != 0:
            self.center[0] += add_x
            self.center[1] += add_y
            for i in range(len(self.vertices)):
                self.vertices[i][0] += add_x
                self.vertices[i][1] += add_y
    
    def shoot_missile(self):
        if time.time() - self.last_shoot_time >= constants.TIME_BETWEEN_SHOOTS:
            vector = [
                constants.MISSILE_SPEED * (self.vertices[0][0] - self.center[0]),
                constants.MISSILE_SPEED * (self.vertices[0][1] - self.center[1])
                ]
            self.last_shoot_time = time.time()
            return Missile(self.vertices[0], vector)
        return None

    def angle_asteroid(self, asteroid_vector):
        spaceship_vector = [
                (self.vertices[0][0] - self.center[0]),
                (self.vertices[0][1] - self.center[1])
                ]
        unit_spaceship_vector = spaceship_vector / np.linalg.norm(spaceship_vector)
        unit_asteroid_vector = asteroid_vector / np.linalg.norm(asteroid_vector)
        dot_product = np.dot(unit_spaceship_vector, unit_asteroid_vector)
        angle = np.arccos(dot_product)
        return math.degrees(angle)