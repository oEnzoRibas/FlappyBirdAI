import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((360, 540))
pygame.display.set_caption("Showcase Image")

# Load the image
image_path = os.path.join('media', 'Showcase', 'neat_run-show-case.gif')
image = pygame.image.load(image_path)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit the image onto the screen
    screen.blit(image, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()