import pygame
import random
import sys
from player import Player
from asteroid import Asteroid
from bullet import Bullet
import math


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

# Create game objects
player = Player(WIDTH // 2, HEIGHT // 2)
asteroids = [Asteroid(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice(["large", "medium", "small"])) for _ in range(5)]
bullets = []

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Shoot bullet
                # Create a new bullet at the player's position and angle
                bullets.append(Bullet(player.x, player.y, player.angle))

    # Update game objects
    player.update()
    for asteroid in asteroids:
        asteroid.update()
    bullets = [bullet for bullet in bullets if bullet.update()]  # Remove bullets that go off-screen

    # Check for collisions between player and asteroids
    for asteroid in asteroids:
        distance = math.sqrt((player.x - asteroid.x) ** 2 + (player.y - asteroid.y) ** 2)
        if distance < asteroid.radius + player.size:  # Collision detected
            # Respawn player in the center
            player.x, player.y = WIDTH // 2, HEIGHT // 2
            player.velocity_x, player.velocity_y = 0, 0
            break

    # Check for collisions between bullets and asteroids
    new_asteroids = []
    for bullet in bullets:
        for asteroid in asteroids:
            distance = math.sqrt((bullet.x - asteroid.x) ** 2 + (bullet.y - asteroid.y) ** 2)
            if distance < asteroid.radius:  # Collision detected
                bullets.remove(bullet)  # Remove the bullet
                if asteroid.size == "large":
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium"))
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium"))
                elif asteroid.size == "medium":
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "small"))
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "small"))
                # Remove the asteroid
                asteroids.remove(asteroid)
                break
    asteroids.extend(new_asteroids)





    # Clear the screen
    screen.fill(BLACK)

    # Draw game objects
    player.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Refresh the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()