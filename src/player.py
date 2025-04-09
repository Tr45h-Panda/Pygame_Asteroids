import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = -90  # Start with no rotation applied
        self.velocity_x = 0  # Horizontal velocity
        self.velocity_y = 0  # Vertical velocity
        self.size = 25  # Size of the ship (used for scaling)
        
        # Load the ship sprite
        self.original_image = pygame.image.load("assets/player_ship.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.size * 2, self.size * 2))  # Scale the sprite
        
        # Rotate the sprite to face right initially
        self.original_image = pygame.transform.rotate(self.original_image, -90)
        self.image = self.original_image  # Keep a reference to the rotated image

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.angle += 5  # Rotate left (counterclockwise)
        if keys[pygame.K_LEFT]:
            self.angle -= 5  # Rotate right (clockwise)
        if keys[pygame.K_UP]:  # Thrust forward
            thrust = 0.1  # Small thrust for fine control
            # Apply thrust in the direction of the ship's angle
            self.velocity_x += thrust * math.cos(math.radians(-self.angle))
            self.velocity_y -= thrust * math.sin(math.radians(-self.angle))
        if keys[pygame.K_DOWN]:  # Decelerate
            self.velocity_x *= 0.98  # Apply friction
            self.velocity_y *= 0.98

        # Update position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wrap around screen edges
        self.x %= 800  # Assuming screen width is 800
        self.y %= 600  # Assuming screen height is 600

    def draw(self, screen):
        # Rotate the original sprite based on the angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)