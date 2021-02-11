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
import time    # Sleep functions

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

# Player Movement Step (pixels)
PLAYER_MOVE_STEP = 10

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED   = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE  = (0, 0, 255)
COLOR_SKY   = (135, 206, 250)

# Location of graphical assets, relative to project top level directory
PLANE_IMG   = "assets/plane5.png"
MISSILE_IMG = "assets/missile.png"
CLOUD1_IMG  = "assets/cloud1.png"
CLOUD2_IMG  = "assets/cloud2.png"
CLOUD3_IMG  = "assets/cloud3.png"

# Array of cloud images
cloud_imgs = [CLOUD1_IMG, CLOUD2_IMG, CLOUD3_IMG]

# Location of audio assets, relative to project top level directory
MUSIC_SND  = "assets/music.wav"
PLANE_SND  = "assets/plane.ogg"
SWOOSH_SND = "assets/swoosh.wav"
BOOM_SND   = "assets/explosion.mp3"
GAMOVR_SND = "assets/game_over.ogg"
DING_SND   = "assets/ding.mp3"

# Player Class
class Player(pygame.sprite.Sprite):
   def __init__(self):
      super(Player, self).__init__()
      self.surf = pygame.image.load(PLANE_IMG).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      self.rect = self.surf.get_rect()
      self.mask = pygame.mask.from_surface(self.surf)

   # Move the Player based on user input
   def update(self, pressed_keys):
      if pressed_keys[K_UP] | pressed_keys[K_w]:
         self.rect.move_ip(0, -PLAYER_MOVE_STEP)
         plane_move_sound.play()
      if pressed_keys[K_DOWN] | pressed_keys[K_s]:
         self.rect.move_ip(0, PLAYER_MOVE_STEP)
         plane_move_sound.play()
      if pressed_keys[K_LEFT] | pressed_keys[K_a]:
         self.rect.move_ip(-PLAYER_MOVE_STEP, 0)
      if pressed_keys[K_RIGHT] | pressed_keys[K_d]:
         self.rect.move_ip(PLAYER_MOVE_STEP, 0)

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
      self.surf = pygame.image.load(MISSILE_IMG).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
         )
      )
      self.mask = pygame.mask.from_surface(self.surf)
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
      self.surf = pygame.image.load(cloud_imgs[random.randint(0, len(cloud_imgs) - 1)]).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
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

# Score Object
class Score(object):
   def __init__(self):
      self.font = pygame.font.SysFont("Arial", 25)
      self.total = 0
      self.color = COLOR_BLACK
      self.text = None

   def update(self):
      self.text = self.font.render("Score: {0}".format(self.total), 1, self.color)

   def add(self, amount):
      self.total += amount
      if amount > 0:
         ding_sound.play()

   def blit(self, surf):
      surf.blit(self.text, ((SCREEN_WIDTH / 2) - (self.text.get_width() / 2), self.text.get_height()))

#------------------------------
# Core Logic
#------------------------------

# Set up mixer for audio
pygame.mixer.init()

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

# Instantiate the score object
score = Score()

# Create Groups to hold enemy sprites and all sprited
# - enemies is used for collision detection and postition updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
enemy_cnt = len(enemies)
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Add the player to the all_sprites Group
all_sprites.add(player)

# Load and play background music
pygame.mixer.music.load(MUSIC_SND)
pygame.mixer.music.play(loops=-1)

# Load and play plane flying sound
plane_fly_sound = pygame.mixer.Sound(PLANE_SND)
plane_fly_sound.play(loops=-1)

# Load all other sound files
plane_move_sound = pygame.mixer.Sound(SWOOSH_SND)
boom_sound = pygame.mixer.Sound(BOOM_SND)
ding_sound = pygame.mixer.Sound(DING_SND)
gamover_sound = pygame.mixer.Sound(GAMOVR_SND)

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
         enemy_cnt += 1
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

   # save off the enemy count
   enemy_cnt_tmp = enemy_cnt
   # Update enemy positions and count how many are remaining
   enemies.update()
   enemy_cnt = len(enemies)

   # Update the score
   score.add(enemy_cnt_tmp - enemy_cnt)

   # Update cloud positions
   clouds.update()

   # Update the score text
   score.update()

   # Fill the background (sky blue)
   screen.fill(COLOR_SKY)

   # Draw all sprites to the screen
   for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)

   # Draw the score to the screen
   score.blit(screen)

   # Check for a collision between the Player and all enemies
   enemy = pygame.sprite.spritecollideany(player, enemies)
   if enemy != None:
      # Check the collision mask for pixel-perfect collision
      if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
         # If so, remove the player and stop the game loop
         player.kill()

         # Stop any moving sounds and play the collision sound
         plane_move_sound.stop()
         plane_fly_sound.stop()
         boom_sound.play()

         # Stop the game loop
         running = False

   # Flip (redraw) the display
   pygame.display.flip()

   # Pause before closing
   if running == False:
      time.sleep(2)
      gamover_sound.play()
      time.sleep(3)

   # Ensure game maintains framerate of 30 fps
   clock.tick(30)

# Stop and quit the sound mixer
pygame.mixer.music.stop()
pygame.mixer.quit()

# Done! Time to quit
pygame.quit()