import pygame
import math

class Bullet:
    def __init__(self, x, y, angle, source="player"):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10  # Speed of the bullet
        self.source = source  # "player" or "spaceship"
        self.color = (255, 255, 255)  # White color
        self.radius = 2  # Size of the bullet

    def update(self):
        # Move the bullet in the direction of its angle
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        # Remove the bullet if it goes off-screen
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            return False  # Indicate that the bullet should be removed
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)