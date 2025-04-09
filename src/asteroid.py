import pygame
import math
import random

class Asteroid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.angle = random.uniform(0, 360)  # Random direction
        self.speed = random.uniform(*{"large": (0.5, 1.5), "medium": (1.5, 3.0), "small": (0.5, 5.0)}[size])
        self.radius = {"large": 48, "medium": 24, "small": 12}[size]

        # Randomly select a sprite variation for the asteroid
        variation = random.randint(1, 2)  # Assuming 3 variations per size
        self.image = pygame.image.load(f"assets/{size}_asteroid_{variation:02}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # Scale to match radius

    def update(self):
        # Move the asteroid in the direction of its angle
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        # Wrap around screen edges
        self.x %= 800  # Assuming screen width is 800
        self.y %= 600  # Assuming screen height is 600

    def draw(self, screen):
        # Draw the asteroid sprite
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)