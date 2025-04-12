import pygame
import random
import sys
import math
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from spaceship import Spaceship
from fragment import Fragment

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


# Initialize level
level = 1
player = Player(WIDTH // 2, HEIGHT // 2)
lives = 3 # Player lives
score = 0 # Player score
spaceship_spawn_chance = 0.0001  # Chance to spawn a spaceship each frame
spaceship = None
respawn_timer = 0  # Time when the player can respawn (in milliseconds)
respawn_delay = 500  # Delay in milliseconds (e.g., 1 second)
grace_period = 1000  # Grace period in milliseconds (e.g., 2 seconds)
grace_timer = 0  # Time when the grace period ends
max_respawn_attempts = 10  # Maximum number of attempts to find a safe location



# Create Game objects 
bullets = []
asteroids = []
fragments = []


# Load the player ship sprite for the lives display
life_icon = pygame.image.load("assets/player_ship.png").convert_alpha()
life_icon = pygame.transform.scale(life_icon, (player.size, player.size))  # Scale down for the lives display

def spawn_asteroids(level):
    """Spawn large asteroids based on the current level, avoiding the player's safe zone."""
    safe_zone_radius = 150  # Define the radius of the safe zone around the player
    asteroids = []

    for _ in range(level * 3):  # Spawn asteroids based on the level
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            # Calculate the distance from the player's position
            distance_from_player = math.sqrt((x - player.x) ** 2 + (y - player.y) ** 2)
            if distance_from_player > safe_zone_radius:  # Ensure asteroid spawns outside the safe zone
                asteroids.append(Asteroid(x, y, "large", player.size))
                break

    return asteroids
asteroids = spawn_asteroids(level)


arcade_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)  # Font size 24

def draw_lives_and_score(screen, lives, icon, score):
    """Draw the remaining lives and the score in the top-left corner."""
    # Draw the score
    score_text = arcade_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))  # Draw the score at the top-left corner

    # Draw the lives below the score
    for i in range(lives):
        screen.blit(icon, (10 + i * (player.size + 5), 40))  # Offset each icon horizontally

def game_over_screen(screen, score):
    """Display the Game Over screen with the final score."""
    font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 74)  # Use a default font with size 74
    text = font.render("GAME OVER", True, WHITE)
    subtext = arcade_font.render("Press ESC to quit", True, WHITE)
    score_text = arcade_font.render(f"Final Score: {score}", True, WHITE)

    # Center the text on the screen
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    subtext_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # Display the text
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(subtext, subtext_rect)
    pygame.display.flip()

    # Wait for the player to press ESC
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False


def check_spawn_location(player, asteroids, safe_zone_radius=50):
    """Check if the player's respawn location is safe."""
    for asteroid in asteroids:
        distance = math.sqrt((player.x - asteroid.x) ** 2 + (player.y - asteroid.y) ** 2)
        if distance < safe_zone_radius + asteroid.radius:  # Unsafe if within the safe zone
            return False
    return True

# Main game loop
clock = pygame.time.Clock()
running = True
fragments = []  # List to store fragments
death_animation_timer = 0  # Timer for the death animation

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and respawn_timer == 0:  # Shoot bullet only if not respawning
                bullets.append(Bullet(player.x, player.y, -player.angle))  # Match bullet angle to ship's rotation

    # Update game objects
    if respawn_timer == 0 and current_time >= grace_timer:  # Only update the player if not respawning or in grace period
        player.update()
    for asteroid in asteroids:
        asteroid.update()
    bullets = [bullet for bullet in bullets if bullet.update()]  # Remove bullets that go off-screen

    if random.random() < spaceship_spawn_chance and spaceship is None:
        spaceship = Spaceship(WIDTH, HEIGHT)

    if spaceship:
        spaceship.update()
        if random.random() < 0.01:  # 1% chance per frame for the spaceship to shoot
            spaceship.shoot()

    new_asteroids = []
    # Unified Bullet-Asteroid Collision
    for bullet in bullets[:]:  # Iterate over a copy of the list to safely remove bullets
        for asteroid in asteroids[:]:  # Iterate over a copy of the list to safely remove asteroids
                distance = math.sqrt((bullet.x - asteroid.x) ** 2 + (bullet.y - asteroid.y) ** 2)
                if distance < asteroid.radius:  # Collision detected
                    bullets.remove(bullet)  # Remove the  bullet
                    if asteroid.size == "large":
                        score += 20
                        new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium", player.size))
                        new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium", player.size))
                    elif asteroid.size == "medium":
                        score += 50
                        new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "small", player.size))
                        new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "small", player.size))
                    elif asteroid.size == "small":
                        score += 100
                    asteroids.remove(asteroid)  # Remove the asteroid
                    break
    asteroids.extend(new_asteroids)        

    # Check for collisions between player and asteroids
    if lives > 0 and respawn_timer == 0 and current_time >= grace_timer:
        for asteroid in asteroids:
            distance = math.sqrt((player.x - asteroid.x) ** 2 + (player.y - asteroid.y) ** 2)
            if distance < asteroid.radius + player.size:  # Collision detected
                lives -= 1
                if lives == 0:
                    game_over_screen(screen, score)
                    running = False
                else:
                    # Trigger death animation
                    fragments = []
                    for i in range(10):  # Create 10 fragments
                        angle = i * (360 / 10)
                        fragments.append(Fragment(player.x, player.y, angle, player.size // 2, WHITE))
                    death_animation_timer = current_time + 1000  # 1 second for the death animation
                    respawn_timer = current_time + 1500  # Respawn after 1.5 seconds
                break

    # Player-Spaceship Collision
    if spaceship:
        distance = math.sqrt((player.x - spaceship.x) ** 2 + (player.y - spaceship.y) ** 2)
        if distance < player.size + 20:  # Collision detected with spaceship
            spaceship = None  # Remove the spaceship
            lives -= 1
            if lives == 0:
                game_over_screen(screen, score)
                running = False
            respawn_timer = current_time + respawn_delay  # Set the respawn timer

    # Player Bullet - Spaceship Collision
    if spaceship:
        for bullet in bullets[:]:  # Iterate over a copy of the bullets list
            distance = math.sqrt((bullet.x - spaceship.x) ** 2 + (bullet.y - spaceship.y) ** 2)
            if distance < 20:  # Assuming spaceship has a collision radius of 20
                bullets.remove(bullet)  # Remove the bullet
                spaceship = None  # Remove the spaceship
                score += 1000  # Award points for destroying the spaceship
                break  # Exit the loop after handling the collision

    # Player-Bullet Collision
    if spaceship:
        for bullet in spaceship.bullets[:]:  # Iterate over a copy of the list to safely remove bullets
            distance = math.sqrt((player.x - bullet.x) ** 2 + (player.y - bullet.y) ** 2)
            if distance < player.size:  # Collision detected
                spaceship.bullets.remove(bullet)  # Remove the bullet
                lives -= 1  # Decrease lives
                if lives == 0:
                    game_over_screen(screen, score)
                    running = False
                respawn_timer = current_time + respawn_delay  # Set the respawn timer

    # Spaceship-Asteroid Collision
    if spaceship:
        new_asteroids = []  # Clear the list of new asteroids
        for asteroid in asteroids[:]:  # Iterate over a copy of the asteroids list
            distance = math.sqrt((spaceship.x - asteroid.x) ** 2 + (spaceship.y - asteroid.y) ** 2)
            if distance < 20 + asteroid.radius:  # Collision detected
                spaceship = None  # Remove the spaceship
                if asteroid.size == "large":
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium", player.size))
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium", player.size))
                elif asteroid.size == "medium":
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "small", player.size))
                    new_asteroids.append(Asteroid(asteroid.x, asteroid.y, "small", player.size))
                asteroids.remove(asteroid)  # Remove the asteroid
                break
        asteroids.extend(new_asteroids)  # Add the new asteroids to the list
                

    # Handle player respawn
    if respawn_timer > 0:
        if current_time >= respawn_timer:  # Time to respawn
            for _ in range(max_respawn_attempts):
                if check_spawn_location(player, asteroids):
                    player.x, player.y = WIDTH // 2, HEIGHT // 2  # Respawn at the center
                    player.velocity_x, player.velocity_y = 0, 0  # Reset velocity
                    player.angle = -90  # Reset angle to face upward
                    respawn_timer = 0  # Reset the respawn timer
                    grace_timer = current_time + grace_period  # Start the grace period
                    break
            else:
                respawn_timer = current_time + respawn_delay  # Extend the respawn delay if no safe location is found
        else:
            # Reset the player's position immediately when the respawn timer starts
            player.x, player.y = WIDTH // 2, HEIGHT // 2
            player.velocity_x, player.velocity_y = 0, 0
            player.angle = -90

    # Check if all asteroids are destroyed
    if not asteroids:
        level += 1  # Increment level
        asteroids = spawn_asteroids(level)  # Spawn new asteroids

    # Clear the screen
    screen.fill(BLACK)

    # Update fragments
    for fragment in fragments[:]:
        fragment.update()
        if fragment.size < 1:  # Remove fragments that are too small
            fragments.remove(fragment)

    # Draw fragments
    for fragment in fragments:
        fragment.draw(screen)

    # Draw the player if not in death animation or respawn state
    if current_time >= death_animation_timer and respawn_timer == 0:
        player.draw(screen)

    for asteroid in asteroids:
        asteroid.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    if spaceship:
        spaceship.draw(screen)

    # Draw remaining lives and score
    draw_lives_and_score(screen, lives, life_icon, score)

    # Refresh the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()