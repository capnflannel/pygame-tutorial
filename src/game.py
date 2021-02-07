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

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:

   # Did the user click the window close button?
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

   # Fill the background
   screen.fill((255, 255, 255))

   # Draw a solid blue circle in the center
   pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

   # Flip (redraw) the display
   pygame.display.flip()

# Done! Time to quit
pygame.quit()