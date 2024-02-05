"""test file"""
import os
import time
import pygame
import random
import cv2
import numpy as np

current_target_index = 0

vc_folder = "voicelines_Curiosity"
first_voiceline = "Glados_escape_02_sphere_curiosity-01.wav"

lerp_factor = 0.1

# Define constants for movement and delay
MOVEMENT_DISTANCE = 500  # Distance to move
DELAY_BETWEEN_MOVES = 2000  # Delay in milliseconds

STATE_IDLE = 0
STATE_MOVING = 1

# Initialize the last move time
last_move_time = pygame.time.get_ticks()
last_state_change_time = pygame.time.get_ticks()
state = 0

idle_frames = 0
MAX_IDLE_FRAMES = 120

def get_next_position(current_x, current_y, state):
    if state == STATE_IDLE:
        # While idle, move towards a far point
        target_x, target_y = get_far_point(current_x, current_y, MOVEMENT_DISTANCE)
        return target_x, target_y
    elif state == STATE_MOVING:
        # Move in a straight line until a boundary is hit, then change the direction
        if current_x <= circle_radius:
            return current_x + speed, current_y
        elif current_x >= win_width - circle_radius:
            return current_x - speed, current_y
        elif current_y <= circle_radius:
            return current_x, current_y + speed
        elif current_y >= win_height - circle_radius:
            return current_x, current_y - speed
        else:
            return current_x, current_y



def get_far_point(current_x, current_y, radius):
    while True:
        target_x = random.uniform(radius, win_width - radius)
        target_y = random.uniform(radius, win_height - radius)
        yield target_x, target_y


# Initialize Pygame
pygame.init()

# Get screen resolution
infoObject = pygame.display.Info()
win_width, win_height = infoObject.current_w, infoObject.current_h

# Set the dimensions of the window
win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

# Define the color of the circle (RGB)
circle_color = (255, 255, 0)  # Yellow

# Define the initial position and size of the circle
circle_radius = 100
circle_x = win_width // 2
circle_y = win_height // 2

corners = [(circle_radius, circle_radius), (win_width - circle_radius, circle_radius),
           (circle_radius, win_height - circle_radius), (win_width - circle_radius, win_height - circle_radius)]

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

# Initialize the camera
cap = cv2.VideoCapture(0)

# Load the DNN model
net = cv2.dnn.readNetFromCaffe("models/deploy.prototxt", "models/res10_300x300_ssd_iter_140000.caffemodel")

# Initialize the target position to the current position of the circle
target_x, target_y = circle_x, circle_y

far_points_generator = get_far_point(circle_x, circle_y, circle_radius)

# Main game loop
running = True
while running:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Prepare the image for the deep learning network
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network and obtain the detections and predictions
    net.setInput(blob)
    detections = net.forward()

    # If a face is detected, calculate the position of the face
    face = False
    if len(detections) > 0:
        # We're making the assumption that each image has only ONE face, so find the bounding box with the largest
        # probability
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        # Ensure that the detection with the largest probability also means our minimum probability test (thus
        # helping filter out weak detections)
        if confidence > 0.4:
            face = True
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            target_x = win_width - int((startX + (endX - startX) / 2) * win_width / frame.shape[1])
            target_y = int((startY + (endY - startY) / 2) * win_height / frame.shape[0])
            path = None
        else:  # If no face is detected, keep circle in the same spot
            face = False
            target_x, target_y = circle_x, circle_y
    else:  # If no face is detected, keep circle in the same spot
        face = False
        target_x, target_y = circle_x, circle_y

    if not face:
        target_x, target_y = next(far_points_generator)

    # Update the position of the circle using lerp
    circle_x = circle_x + (target_x - circle_x) * lerp_factor
    circle_y = circle_y + (target_y - circle_y) * lerp_factor

    if face:
        circle_radius = 200
    else:
        circle_radius = 100

    # Fill the window with white color
    win.fill((0, 0, 0))

    # Draw the circle
    pygame.draw.circle(win, circle_color, (int(circle_x), int(circle_y)), circle_radius)

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

# Release the camera
cap.release()

# Quit Pygame
pygame.quit()
