import pygame
import constants

class Missile():
    def __init__(self, position, vector):
        self.position = position
        self.radius = constants.MISSILE_RADIUS
        self.vector  = vector
    
    def display(self, screen):
        pygame.draw.circle(screen, constants.WHITE, self.position, self.radius)

    def move_forward(self):
        self.position = [
            self.position[0] + self.vector[0],
            self.position[1] + self.vector[1]
            ]
    
    def border_intersect(self):
        return self.position[0] < 0 \
            or self.position[0] > constants.WIDTH \
            or self.position[1] < 0 \
            or self.position[1] > constants.HEIGHT