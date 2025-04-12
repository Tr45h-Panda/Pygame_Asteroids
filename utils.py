import pygame

def load_image(filepath):
    """Load an image from the specified file path."""
    image = pygame.image.load(filepath)
    return image

def load_sound(filepath):
    """Load a sound from the specified file path."""
    sound = pygame.mixer.Sound(filepath)
    return sound

def check_collision(rect1, rect2):
    """Check if two rectangles collide."""
    return rect1.colliderect(rect2)

def reset_game_state():
    """Reset the game state to its initial conditions."""
    # Placeholder for resetting game variables
    pass

def draw_text(surface, text, position, font, color=(255, 255, 255)):
    """Draw text on the given surface at the specified position."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)