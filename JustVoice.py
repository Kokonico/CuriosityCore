import os
import time
import pygame
import random

vc_folder = "voicelines_Curiosity"
first_voiceline = "Glados_escape_02_sphere_curiosity-01.wav"

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))

# Define the color of the circle (RGB)
circle_color = (255, 255, 0)  # Yellow

# Define the initial position and size of the circle
circle_radius = 100
circle_x = win_width // 2
circle_y = win_height // 2

# Define the speed of the circle
speed = 10

# Initialize the mixer
pygame.mixer.init()

# Load the first audio file
pygame.mixer.music.load(os.path.join(vc_folder, first_voiceline))

# Play the first audio file
pygame.mixer.music.play()

# Get all voice lines
voicelines = os.listdir(vc_folder)

# Remove non-wav files
voicelines = [voiceline for voiceline in voicelines if voiceline.endswith(".wav")]

# Define the target position
target_x = random.randint(circle_radius, win_width - circle_radius)
target_y = random.randint(circle_radius, win_height - circle_radius)

# Main game loop
# Main game loop
running = True
while running:
    # Fill the window with black color
    win.fill((0, 0, 0))

    # Draw the circle
    pygame.draw.circle(win, circle_color, (circle_x, circle_y), circle_radius)

    # Update the position of the circle
    if pygame.mixer.music.get_busy():
        if abs(circle_x - target_x) > speed:
            circle_x += speed if circle_x < target_x else -speed
        if abs(circle_y - target_y) > speed:
            circle_y += speed if circle_y < target_y else -speed

    # Make sure the circle doesn't go off the screen
    if circle_x - circle_radius < 0:
        circle_x = circle_radius
    if circle_x + circle_radius > win_width:
        circle_x = win_width - circle_radius
    if circle_y - circle_radius < 0:
        circle_y = circle_radius
    if circle_y + circle_radius > win_height:
        circle_y = win_height - circle_radius

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If the voiceline has finished playing, start a new one
    if not pygame.mixer.music.get_busy():
        # Get random voice line
        voiceline = voicelines[random.randint(0, len(voicelines) - 1)]
        pygame.mixer.music.load(os.path.join(vc_folder, voiceline))
        pygame.mixer.music.play()

        # Set a new target position
        target_x = random.randint(circle_radius, win_width - circle_radius)
        target_y = random.randint(circle_radius, win_height - circle_radius)

# Quit Pygame
pygame.quit()