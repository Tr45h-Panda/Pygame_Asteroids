import pygame
import math
import random
from bullet import Bullet

class Spaceship:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Spawn at a random edge of the screen
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.x = random.randint(0, screen_width)
            self.y = 0
        elif edge == "bottom":
            self.x = random.randint(0, screen_width)
            self.y = screen_height
        elif edge == "left":
            self.x = 0
            self.y = random.randint(0, screen_height)
        elif edge == "right":
            self.x = screen_width
            self.y = random.randint(0, screen_height)

        # Velocity and acceleration
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

        # Time to change acceleration
        self.acceleration_change_timer = random.randint(60, 120)  # Frames until next acceleration change

        # Load spaceship sprite
        self.image = pygame.image.load("assets/spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 30))  # Scale to a reasonable size

        # Track bullets fired by the spaceship
        self.bullets = []

    def update(self):
        # Change acceleration periodically
        self.acceleration_change_timer -= 1
        if self.acceleration_change_timer <= 0:
            self.acceleration_change_timer = random.randint(60, 120)  # Reset timer
            angle = random.uniform(0, 360)  # Random direction
            magnitude = random.uniform(0.05, 0.2)  # Random acceleration magnitude
            self.acceleration_x = magnitude * math.cos(math.radians(angle))
            self.acceleration_y = -magnitude * math.sin(math.radians(angle))

        # Update velocity based on acceleration
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y

        # Limit the maximum speed
        max_speed = 3
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if speed > max_speed:
            scale = max_speed / speed
            self.velocity_x *= scale
            self.velocity_y *= scale

        # Update position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wrap around screen edges
        self.x %= self.screen_width
        self.y %= self.screen_height

        # Update bullets fired by the spaceship
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]

    def shoot(self):
        # Pick a random direction to shoot
        bullet_angle = random.uniform(0, 360)
        bullet = Bullet(self.x, self.y, bullet_angle)
        self.bullets.append(bullet)
        return bullet

    def draw(self, screen):
        # Draw the spaceship sprite
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)

        # Draw bullets fired by the spaceship
        for bullet in self.bullets:
            bullet.draw(screen)