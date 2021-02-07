# Simple pygame program.
#
# See https://realpython.com/pygame-a-primer/
#
# Basic Game Design:
#  -The goal of the game is to avoid incoming obstacles:
#     -The player starts on the left side of the screen
#     -The obstacles enter randomly from the right and move left in a straight line
#  -The player can move left, right, up, or down to avoid the obstacles
#  -The player cannot move off the screen
#  -The game ends either wheh the player is hit by an obstacle or when the user quits the game

#------------------------------
# Imports
#------------------------------
import pygame  # Import the pygame library
import random  # Random number generation

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
   K_UP,       # UP Key
   K_DOWN,     # DOWN Key
   K_LEFT,     # LEFT Key
   K_RIGHT,    # RIGHT Key
   K_ESCAPE,   # ESC Key
   K_SPACE,    # Space Key
   K_KP_PLUS,  # Plus Key (numpad)
   K_KP_MINUS, # Minus Key (numpad)
   KEYDOWN,    # Keypress Event
   QUIT        # Quit Event
)

#------------------------------
# Constants
#------------------------------

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Test Object Coords
OBJ_Y = SCREEN_HEIGHT / 2
OBJ_X = SCREEN_WIDTH / 2

# Test Object Radius (pixels)
OBJ_RADIUS = 75

# Test Object Radius Resize Step
OBJ_RAD_STEP = 5

# Test Object Color
OBJ_R = 0
OBJ_G = 0
OBJ_B = 255

#------------------------------
# Core Logic
#------------------------------

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# The main game loop
while running:

   # Process all events in the event queue
   for event in pygame.event.get():
      # Did the user hit a key?
      if event.type == KEYDOWN:
         # Handle ESC keypress
         if event.key == K_ESCAPE:
            running = False
         # Handle UP keypress
         elif event.key == K_UP:
            OBJ_Y -= OBJ_RADIUS
         # Handle DOWN keypress
         elif event.key == K_DOWN:
            OBJ_Y += OBJ_RADIUS
         # Handle LEFT keypress
         elif event.key == K_LEFT:
            OBJ_X -= OBJ_RADIUS
         # Handle RIGHT keypress
         elif event.key == K_RIGHT:
            OBJ_X += OBJ_RADIUS
         # Handle SPACE keypress
         elif event.key == K_SPACE:
            # Set the RGB value of the object to a random value between 0 and 255
            OBJ_R = random.randint(0, 255)
            OBJ_G = random.randint(0, 255)
            OBJ_B = random.randint(0, 255)
         # Handle PLUS keypress
         elif event.key == K_KP_PLUS:
            OBJ_RADIUS += OBJ_RAD_STEP
         # Handle MINUS keypress
         elif event.key == K_KP_MINUS:
            if OBJ_RADIUS > OBJ_RAD_STEP:
               OBJ_RADIUS -= OBJ_RAD_STEP
      # Dis the user close the window?
      elif event.type == pygame.QUIT:
         running = False

   # Fill the background
   screen.fill((255, 255, 255))

   # Draw a solid blue circle in the center
   pygame.draw.circle(screen, (OBJ_R, OBJ_G, OBJ_B), (OBJ_X, OBJ_Y), OBJ_RADIUS)

   # Flip (redraw) the display
   pygame.display.flip()

# Done! Time to quit
pygame.quit()