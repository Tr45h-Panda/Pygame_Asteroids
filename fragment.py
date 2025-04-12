import pygame
import math
import random


class Fragment:
    def __init__(self, x, y, angle, size, color):
        self.x = x
        self.y = y
        self.angle = angle  # Direction of movement
        self.size = size  # Size of the fragment
        self.color = color  # Color of the fragment
        self.velocity_x = math.cos(math.radians(angle)) * random.uniform(1, 3)  # Slower movement
        self.velocity_y = math.sin(math.radians(angle)) * random.uniform(1, 3)
        self.rotation = random.uniform(-2, 2)  # Slower rotation speed

    def update(self):
        # Move the fragment
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.size *= 0.97  # Shrink more slowly

    def draw(self, screen):
        # Draw the fragment as a triangle
        points = [
            (self.x + self.size * math.cos(math.radians(self.angle)),
             self.y + self.size * math.sin(math.radians(self.angle))),
            (self.x + self.size * math.cos(math.radians(self.angle + 120)),
             self.y + self.size * math.sin(math.radians(self.angle + 120))),
            (self.x + self.size * math.cos(math.radians(self.angle + 240)),
             self.y + self.size * math.sin(math.radians(self.angle + 240))),
        ]
        pygame.draw.polygon(screen, self.color, points)