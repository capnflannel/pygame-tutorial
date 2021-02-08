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
   RLEACCEL,   # Accelerated rendering parameter for non-accelerated displays
   K_UP,       # UP Key
   K_DOWN,     # DOWN Key
   K_LEFT,     # LEFT Key
   K_RIGHT,    # RIGHT Key
   K_ESCAPE,   # ESC Key
   K_SPACE,    # Space Key
   K_w,        # W Key
   K_s,        # S Key
   K_a,        # A Key
   K_d,        # D Key
   KEYDOWN,    # Keypress Event
   QUIT        # Quit Event
)

#------------------------------
# Defines
#------------------------------

# Define constants for the screen width and height
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Test Object Move Step
OBJ_MOVE_STEP = 10

# Locations of graphical assets, relative to project top level directory
PLANE1  = "assets/plane1.png"
PLANE2  = "assets/plane2.png"
PLANE3  = "assets/plane3.png"
PLANE4  = "assets/plane4.png"
MISSILE = "assets/missile.png"
CLOUD1  = "assets/cloud1.png"
CLOUD2  = "assets/cloud2.png"
CLOUD3  = "assets/cloud3.png"

# Player Class
class Player(pygame.sprite.Sprite):
   def __init__(self):
      super(Player, self).__init__()
      self.surf = pygame.image.load(PLANE1).convert()
      self.surf.set_colorkey((255, 255, 255), RLEACCEL)
      self.rect = self.surf.get_rect()

   # Move the Player based on user input
   def update(self, pressed_keys):
      if pressed_keys[K_UP] | pressed_keys[K_w]:
         self.rect.move_ip(0, -OBJ_MOVE_STEP)
      if pressed_keys[K_DOWN] | pressed_keys[K_s]:
         self.rect.move_ip(0, OBJ_MOVE_STEP)
      if pressed_keys[K_LEFT] | pressed_keys[K_a]:
         self.rect.move_ip(-OBJ_MOVE_STEP, 0)
      if pressed_keys[K_RIGHT] | pressed_keys[K_d]:
         self.rect.move_ip(OBJ_MOVE_STEP, 0)

      # Keep the Player on the screen
      if self.rect.left <= 0:
         self.rect.left = 0
      if self.rect.right >= SCREEN_WIDTH:
         self.rect.right = SCREEN_WIDTH
      if self.rect.top <= 0:
         self.rect.top = 0
      if self.rect.bottom >= SCREEN_HEIGHT:
         self.rect.bottom = SCREEN_HEIGHT

# Enemy Class
class Enemy(pygame.sprite.Sprite):
   def __init__(self):
      super(Enemy, self).__init__()
      self.surf = pygame.image.load(MISSILE).convert()
      self.surf.set_colorkey((255, 255, 255), RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
         )
      )
      self.speed = random.randint(5, 20)

   # Move the sprite based on speed
   # Remove the sprite when it passed the left edge of the screen
   def update(self):
      self.rect.move_ip(-self.speed, 0)
      if self.rect.right < 0:
         self.kill()

# Cloud Class
class Cloud(pygame.sprite.Sprite):
   def __init__(self):
      super(Cloud, self).__init__()
      self.surf = pygame.image.load(CLOUD1).convert()
      self.surf.set_colorkey((255, 255, 255), RLEACCEL)
      # The starting position is randomly generated
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
         )
      )

   # Move the cloud based on constant speed
   # Remove the cloud when it passes the left edge of the screen
   def update(self):
      self.rect.move_ip(-5, 0)
      if self.rect.right < 0:
         self.kill()

#------------------------------
# Core Logic
#------------------------------

# Initialize pygame
pygame.init()

# Setup the clock for deterministic framerate
clock = pygame.time.Clock()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding new enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Create a custom event for adding a new cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate the player object
player = Player()

# Create Groups to hold enemy sprites and all sprited
# - enemies is used for collision detection and postition updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Add the player to the all_sprites Group
all_sprites.add(player)

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
      # Did the user close the window?
      elif event.type == pygame.QUIT:
         running = False
      # Add a new enemy?
      elif event.type == ADDENEMY:
         # Create the new enemy and add it to the sprite groups
         new_enemy = Enemy()
         enemies.add(new_enemy)
         all_sprites.add(new_enemy)
      # Add a new cloud?
      elif event.type == ADDCLOUD:
         # Create the new cloud and add it to the sprite groups
         new_cloud = Cloud()
         clouds.add(new_cloud)
         all_sprites.add(new_cloud)

   # Get all the keys currently pressed
   pressed_keys = pygame.key.get_pressed()

   # Update the player sprite based on user input
   player.update(pressed_keys)

   # Update enemy positions
   enemies.update()

   # Update cloud positions
   clouds.update()

   # Fill the background
   screen.fill((135, 206, 250))

   # Draw all sprites to the screen
   for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)

   # Check for a collision between the Player and all enemies
   if pygame.sprite.spritecollideany(player, enemies):
      # If so, remove the player and stop the game loop
      player.kill()
      running = False

   # Flip (redraw) the display
   pygame.display.flip()

   # Ensure game maintains framerate of 30 fps
   clock.tick(30)

# Done! Time to quit
pygame.quit()