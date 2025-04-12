import pygame
import math
import random

class Asteroid:
    def __init__(self, x, y, size, player_size):
        """
        Initialize an asteroid.

        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param size: Size of the asteroid ('large', 'medium', 'small')
        :param player_size: Size of the player ship (used for scaling asteroid sizes)
        """
        self.x = x
        self.y = y
        self.size = size
        self.angle = random.uniform(0, 360)  # Random direction
        self.speed = random.uniform(*{"large": (0.1, 1.0), "medium": (0.1, 2.0), "small": (0.1, 3.0)}[size])

        # Scale asteroid radius based on player size
        size_scale = {"large": 2.4, "medium": 1.2, "small": 0.6}[size]
        self.radius = int(player_size * size_scale)

        # Randomly select a sprite variation for the asteroid
        variation = random.randint(1, 4)  # Assuming 3 variations per size
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