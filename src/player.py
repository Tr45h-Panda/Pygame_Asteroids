import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Angle of the ship
        self.velocity_x = 0  # Horizontal velocity
        self.velocity_y = 0  # Vertical velocity
        self.color = (255, 255, 255)  # White color
        self.size = 10  # Size of the triangle ship

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5  # Rotate left
        if keys[pygame.K_RIGHT]:
            self.angle -= 5  # Rotate right
        if keys[pygame.K_UP]:  # Thrust forward
            # Apply thrust in the direction the ship is facing
            thrust = 0.1  # Small thrust for fine control
            self.velocity_x += thrust * math.cos(math.radians(self.angle))
            self.velocity_y -= thrust * math.sin(math.radians(self.angle))
        if keys[pygame.K_DOWN]:  # Decelerate
            # Gradually reduce velocity
            self.velocity_x *= 0.98  # Apply friction
            self.velocity_y *= 0.98

        # Update position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wrap around screen edges
        self.x %= 800  # Assuming screen width is 800
        self.y %= 600  # Assuming screen height is 600

    def draw(self, screen):
        # Draw the triangle ship
        tip_x = self.x + self.size * math.cos(math.radians(self.angle))
        tip_y = self.y - self.size * math.sin(math.radians(self.angle))
        left_x = self.x + self.size * math.cos(math.radians(self.angle + 120))
        left_y = self.y - self.size * math.sin(math.radians(self.angle + 120))
        right_x = self.x + self.size * math.cos(math.radians(self.angle - 120))
        right_y = self.y - self.size * math.sin(math.radians(self.angle - 120))

        pygame.draw.polygon(screen, self.color, [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)])