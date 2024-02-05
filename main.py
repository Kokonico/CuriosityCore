"""I'm Different."""

import os
import time

import pygame
import random
import time

vc_folder = "voicelines_Oracle"
first_voiceline = "Turret_turretstuckintube09.wav"

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(vc_folder, first_voiceline))
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# get all voice lines

voicelines = os.listdir(vc_folder)
# remove non-wav files
voicelines = [voiceline for voiceline in voicelines if voiceline.endswith(".wav")]

# say random voice lines

while True:
    # get random voice line
    voiceline = voicelines[random.randint(0, len(voicelines) - 1)]
    pygame.mixer.music.load(os.path.join(vc_folder, voiceline))
    # wait for the voice line to finish
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # wait for a random amount of time
    time.sleep(random.randint(1, 5))
