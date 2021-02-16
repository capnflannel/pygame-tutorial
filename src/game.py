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
   K_RETURN,   # RETURN Key
   K_KP_ENTER, # ENTER Key
   K_w,        # W Key
   K_s,        # S Key
   K_a,        # A Key
   K_d,        # D Key
   K_q,        # Q Key
   KEYDOWN,    # Keypress Event
   QUIT        # Quit Event
)

#------------------------------
# Defines
#------------------------------

# Define constants for the screen width and height
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Frames Per Second
GAME_FPS_30 = 30
GAME_FPS_60 = 60

# Player Movement Step (pixels)
PLAYER_MOVE_STEP = 10

# Color definitions
COLOR_BLACK  = (0, 0, 0)
COLOR_WHITE  = (255, 255, 255)
COLOR_RED    = (255, 0, 0)
COLOR_GREEN  = (0, 255, 0)
COLOR_BLUE   = (0, 0, 255)
COLOR_SKY    = (135, 206, 250)
COLOR_GRAY   = (128, 128, 128)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 128, 0)

# Location of graphical assets, relative to project top level directory
PLANE_IMG      = "assets/plane5.png"
MISSILE_IMG    = "assets/missile.png"
CLOUD1_IMG     = "assets/cloud1.png"
CLOUD2_IMG     = "assets/cloud2.png"
CLOUD3_IMG     = "assets/cloud3.png"
ORB_RED_IMG    = "assets/red_orb.png"
ORB_BLUE_IMG   = "assets/blue_orb.png"
ORB_GREEN_IMG  = "assets/green_orb.png"
ORB_YELLOW_IMG = "assets/yellow_orb.png"
BULLET_IMG     = "assets/bullet.png"

# Array of cloud images
cloud_imgs = [CLOUD1_IMG, CLOUD2_IMG, CLOUD3_IMG]

# Array of orb images
orb_imgs = [ORB_RED_IMG, ORB_YELLOW_IMG, ORB_BLUE_IMG, ORB_GREEN_IMG]
# Array of orb health bonus effects
orb_health_bonus = [1, 5, 10, 50]
orb_score = [5, 10, 50, 100]

# Location of audio assets, relative to project top level directory
MUSIC_SND   = "assets/music.wav"
PLANE_SND   = "assets/plane.ogg"
BOOM_SND    = "assets/explosion.mp3"
GAMOVR_SND  = "assets/game_over.ogg"
DING_SND    = "assets/ding.mp3"
POWERUP_SND = "assets/powerup.wav"
BAD_SND     = "assets/bad.wav"
PEW_SND     = "assets/pew.wav"
MENU_SND    = "assets/menu_music.ogg"

# Player health bounds
PLAYER_HEALTH_MAX = 100
PLAYER_HEALTH_MIN = 0

#------------------------------
# Classes
#------------------------------

# Player Class
class Player(pygame.sprite.Sprite):
   def __init__(self):
      super(Player, self).__init__()
      self.surf = pygame.image.load(PLANE_IMG).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      self.rect = self.surf.get_rect()
      self.mask = pygame.mask.from_surface(self.surf)
      self.health = PLAYER_HEALTH_MAX
      self.exp = 0
      self.level = 1
      self.health_bar = None

   # Move the Player based on user input
   def update(self, pressed_keys):
      if pressed_keys[K_UP] | pressed_keys[K_w]:
         self.rect.move_ip(0, -PLAYER_MOVE_STEP)
      if pressed_keys[K_DOWN] | pressed_keys[K_s]:
         self.rect.move_ip(0, PLAYER_MOVE_STEP)
      if pressed_keys[K_LEFT] | pressed_keys[K_a]:
         self.rect.move_ip(-PLAYER_MOVE_STEP, 0)
      if pressed_keys[K_RIGHT] | pressed_keys[K_d]:
         self.rect.move_ip(PLAYER_MOVE_STEP, 0)
      if pressed_keys[K_SPACE]:
         self.shoot()

      # Keep the Player on the screen
      if self.rect.left <= 0:
         self.rect.left = 0
      if self.rect.right >= SCREEN_WIDTH:
         self.rect.right = SCREEN_WIDTH
      if self.rect.top <= 0:
         self.rect.top = 0
      if self.rect.bottom >= SCREEN_HEIGHT:
         self.rect.bottom = SCREEN_HEIGHT

   # Adjust the player's health
   def inc_health(self, amount):
      self.health += amount
      if self.health >= PLAYER_HEALTH_MAX:
         self.health = PLAYER_HEALTH_MAX

   # Adjust the player's health
   def dec_health(self, amount):
      self.health -= amount
      if self.health <= PLAYER_HEALTH_MIN:
         self.health = PLAYER_HEALTH_MIN

   # Get the player's current health
   def get_health(self):
      return self.health

   # Draw the player's health bar
   def draw_health_bar(self, surf):
      # Set up bar size parameters
      width = PLAYER_HEALTH_MAX
      height = 20
      bar_fill = (self.health / PLAYER_HEALTH_MAX) * width

      # Create the rectangles
      bar_rect = pygame.Rect(5, 5, width, height)
      fill_rect = pygame.Rect(5, 5, bar_fill, height)
      
      # Get the health bar color
      if self.health >= 75:
         bar_color = COLOR_GREEN
      elif self.health >= 50:
         bar_color = COLOR_YELLOW
      elif self.health >= 25:
         bar_color = COLOR_ORANGE
      else:
         bar_color = COLOR_RED

      # Draw the rectangles
      pygame.draw.rect(surf, bar_color, fill_rect)
      pygame.draw.rect(surf, COLOR_GRAY, bar_rect, 1)

   def shoot(self):
      # Spawn bullets from the front rightof the plane
      new_bullet = Bullet(self.rect.right - (self.rect.width / 4), self.rect.bottom - (self.rect.height / 6))
      bullets.add(new_bullet)
      all_sprites.add(new_bullet)
      pew_sound.play()

# Bullet Class
class Bullet(pygame.sprite.Sprite):
   def __init__(self, x, y):
      super(Bullet, self).__init__()
      self.surf = pygame.image.load(BULLET_IMG).convert()
      self.surf.set_colorkey(COLOR_BLACK, RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            # Spawn based on location of player
            x, y
         )
      )
      self.mask = pygame.mask.from_surface(self.surf)
      self.speed = 20
      self.dmg = 10
      self.score = 0

   def update(self):
      self.rect.move_ip(self.speed, 0)
      if self.rect.left > SCREEN_WIDTH:
         self.kill()

   def get_score(self):
      return self.score

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
      #self.path = 0 # TODO: ENUM describing path (LINEAR, SINUSOID, DIAG, RISE, FALL)
      self.health = 1
      self.dmg = 10
      self.score = 10

   # Move the sprite based on speed
   # Remove the sprite when it passes the left edge of the screen
   def update(self):
      self.rect.move_ip(-self.speed, 0)
      if self.rect.right < 0:
         self.kill()

   # Get amount of damage the enemy does
   def get_dmg(self):
      return self.dmg

   def get_score(self):
      return self.score

# Orb Class
class Orb(pygame.sprite.Sprite):
   def __init__(self):
      super(Orb, self).__init__()
      self.type = random.randint(0, len(orb_imgs) - 1)
      self.surf = pygame.image.load(orb_imgs[self.type]).convert()
      self.surf.set_colorkey(COLOR_BLACK, RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
         )
      )
      self.mask = pygame.mask.from_surface(self.surf)
      self.speed = random.randint(5, 15)

   # Move the sprite based on speed
   # Remove the sprite when it passes the left edge of the screen
   def update(self):
      self.rect.move_ip(-self.speed, 0)
      if self.rect.right < 0:
         self.kill()

   def get_health_bonus(self):
      return orb_health_bonus[self.type]

   def get_score(self):
      return orb_score[self.type]

# Cloud Class
class Cloud(pygame.sprite.Sprite):
   def __init__(self):
      super(Cloud, self).__init__()
      self.type = random.randint(0, len(cloud_imgs) - 1)
      self.surf = pygame.image.load(cloud_imgs[self.type]).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      # The starting position is randomly generated
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
         )
      )
      self.speed = random.randint(2, 7)

   # Move the cloud based on constant speed
   # Remove the cloud when it passes the left edge of the screen
   def update(self):
      self.rect.move_ip(-self.speed, 0)
      if self.rect.right < 0:
         self.kill()

# Score Class
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
      else:
         bad_sound.play()
         if self.total < 0:
            self.total = 0

   def blit(self, surf):
      surf.blit(self.text, ((SCREEN_WIDTH / 2) - (self.text.get_width() / 2), self.text.get_height()))

#------------------------------
# Functions
#------------------------------

# Plays the intro sequence
#def intro():
   # TODO play intro sequence

# The start menu loop
#def start_menu():
   # TODO Draw game start menu

# The pause menu loop
def pause_menu():
   # Game is paused
   paused = True

   # Return value to tell the game whether it should continue running
   running = True

   # Play the menu music
   menu_music.play(loops=-1)

   # Set up the menu font
   menu_font = pygame.font.SysFont('Arial', 25)

   # Draw the menu
   border_width = SCREEN_WIDTH / 4
   border_height = SCREEN_HEIGHT / 3
   window_width = border_width - 4
   window_height = border_height - 4
   # Draw the window border
   border = pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect((((SCREEN_WIDTH / 2) - (border_width / 2)), ((SCREEN_HEIGHT / 2) - (border_height / 2))), (border_width, border_height)), border_radius=8)
   # Draw the window
   window = pygame.draw.rect(screen, COLOR_GRAY, pygame.Rect((((SCREEN_WIDTH / 2) - (window_width / 2)), ((SCREEN_HEIGHT / 2) - (window_height / 2))), (window_width, window_height)), border_radius=8)

   # Draw the menu text
   paused_text = menu_font.render('PAUSED', True, COLOR_BLACK)
   text_height = paused_text.get_height()
   screen.blit(paused_text, (window.left + ((window.width - paused_text.get_width()) / 2), window.top + (text_height / 2)))

   # Initialize the menu text
   resume_text = menu_font.render('RESUME', True, COLOR_WHITE)
   resume_text_hl = menu_font.render('RESUME', True, COLOR_YELLOW)
   restart_text = menu_font.render('RESTART', True, COLOR_WHITE)
   restart_text_hl = menu_font.render('RESTART', True, COLOR_YELLOW)
   options_text = menu_font.render('OPTIONS', True, COLOR_WHITE)
   options_text_hl = menu_font.render('OPTIONS', True, COLOR_YELLOW)
   quit_text = menu_font.render('QUIT', True, COLOR_WHITE)
   quit_text_hl = menu_font.render('QUIT', True, COLOR_YELLOW)

   # Array of options
   menu_options = [quit_text, options_text, restart_text, resume_text]
   menu_options_hl = [quit_text_hl, options_text_hl, restart_text_hl, resume_text_hl]
   menu_index = len(menu_options) - 1

   while paused:
      # Process all events in the event queue
      for event in pygame.event.get():
         # Did the user hit a key?
         if event.type == KEYDOWN:
            # Handle ESC keypress
            if event.key == K_ESCAPE:
               paused = False
            # Handle UP keypress
            elif event.key == K_UP:
               if menu_index < (len(menu_options) - 1):
                  menu_index += 1
               else:
                  menu_index = 0
               ding_sound.play()
            # Handle DOWN keypress
            elif event.key == K_DOWN:
               if menu_index > 0:
                  menu_index -= 1
               else:
                  menu_index = len(menu_options) - 1
               ding_sound.play()
            # Handle ENTER|RETURN keypress
            elif ((event.key == K_KP_ENTER) or (event.key == K_RETURN)):
               if menu_index == 0:
                  # QUIT case
                  paused = False
                  running = False
               elif menu_index == 1:
                  # TODO: OPTIONS case
                  paused = False
               elif menu_index == 2:
                  # TODO: RESTART case
                  paused = False
               elif menu_index == 3:
                  # RESUME case
                  paused = False
               
               # Pause quick
               bad_sound.play()
               time.sleep(0.5)
         # Did the user close the window?
         elif event.type == pygame.QUIT:
            paused = False
            running = False

      # Update the highlighted text based on menu_index
      i = 0
      for opt in menu_options:
         if i == menu_index:
            txt = menu_options_hl[i]
         else:
            txt = menu_options[i]
         # Draw the text to the screen
         screen.blit(txt, (window.left + ((window.width - txt.get_width()) / 2), window.bottom - ((i + 1) * text_height) - ((i + 1) * (text_height / 2))))
         # Increment the index
         i += 1

      # Flip (redraw) the display
      pygame.display.flip()

   # Fade the music out
   menu_music.fadeout(1)

   # Return whether the game should keep running
   return running

# The options menu loop
#def options_menu():
   # TODO Draw game options menu

# The main game loop
def game():
   # Set the game to running
   running = True

   # Instantiate the player object
   player = Player()

   # Instantiate the score object
   score = Score()

   # Add the player to the all_sprites Group
   all_sprites.add(player)

   # Start the music
   pygame.mixer.music.play(loops=-1)
   plane_fly_sound.play(loops=-1)

   while running:
      # Process all events in the event queue
      for event in pygame.event.get():
         # Did the user hit a key?
         if event.type == KEYDOWN:
            # Handle ESC keypress
            if event.key == K_ESCAPE:
               #playing = False
               pygame.mixer.music.pause()
               plane_fly_sound.stop()
               running = pause_menu()
               plane_fly_sound.play()
               pygame.mixer.music.play()
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
         # Add a new orb?
         elif event.type == ADDORB:
            # Create the new orb and add it to the sprite groups
            new_orb = Orb()
            orbs.add(new_orb)
            all_sprites.add(new_orb)

      # Check if running again after getting input, in case we need to quit
      if running == True:
         # Get all the keys currently pressed
         pressed_keys = pygame.key.get_pressed()

         # Update the player sprite based on user input
         player.update(pressed_keys)

         # Update the bullets
         bullets.update()

         # Update enemy positions and count how many are remaining
         enemies.update()

         # Update cloud positions
         clouds.update()

         # Update orb positions
         orbs.update()

         # Fill the background (sky blue)
         screen.fill(COLOR_SKY)

         # Draw all sprites to the screen
         for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

         # Check for a collision between the Player and all enemies
         enemy = pygame.sprite.spritecollideany(player, enemies)
         if enemy != None:
            # Check the collision mask for pixel-perfect collision
            if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
               # Apply damage
               player.dec_health(enemy.get_dmg())
               boom_sound.play()

         # Check for a collision between all bullets and enemies
         for bullet in bullets:
            enemy = pygame.sprite.spritecollideany(bullet, enemies)
            if enemy != None:
               # Check the collision mask for pixel-perfect collision
               hits = pygame.sprite.spritecollide(bullet, enemies, True, pygame.sprite.collide_mask)
               if hits != None:
                  for i in hits:
                     hit = hits.pop()
                     score.add(hit.get_score())
                     hit.kill()

         # Check for a collision between the Player and all orbs
         orb = pygame.sprite.spritecollideany(player, orbs)
         if orb != None:
            # Check the collision mask for pixel-perfect collision
            if pygame.sprite.spritecollide(player, orbs, True, pygame.sprite.collide_mask):
               # If so, apply the power-up and play a sound
               player.inc_health(orb.get_health_bonus())
               powerup_sound.play()
               score.add(orb.get_score())

         # Update the score text
         score.update()

         # Draw the score to the screen
         score.blit(screen)

         # Draw the player's health bar
         player.draw_health_bar(screen)

         # Check for player death
         if player.get_health() == PLAYER_HEALTH_MIN:
            # Remove the player
            player.kill()

            # Stop the game loop
            running = False

         # Flip (redraw) the display
         pygame.display.flip()

      # Game is no longer running
      if running == False:
         # Pause before closing
         time.sleep(1)
         gamover_sound.play()
         time.sleep(3)
         pygame.mixer.music.stop()
         plane_fly_sound.stop()

      # Ensure game maintains framerate of 30 fps
      clock.tick(GAME_FPS_30)

# Clean up pygame resources and quit the game
def cleanup():
   # Stop and quit the sound mixer
   pygame.mixer.music.stop()
   pygame.mixer.quit()

   # Done! Time to quit
   pygame.quit()

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
pygame.time.set_timer(ADDCLOUD, 2000)

# Create a custom event for adding orbs
ADDORB = pygame.USEREVENT + 3
pygame.time.set_timer(ADDORB, 10000)

# Create Groups to hold enemy sprites and all sprited
# - enemies is used for collision detection and postition updates
# - orbs is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
orbs = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Load and play background music
pygame.mixer.music.load(MUSIC_SND)

# Load and play plane flying sound
plane_fly_sound = pygame.mixer.Sound(PLANE_SND)

# Load all other sound files
boom_sound = pygame.mixer.Sound(BOOM_SND)
ding_sound = pygame.mixer.Sound(DING_SND)
powerup_sound = pygame.mixer.Sound(POWERUP_SND)
gamover_sound = pygame.mixer.Sound(GAMOVR_SND)
bad_sound = pygame.mixer.Sound(BAD_SND)
pew_sound = pygame.mixer.Sound(PEW_SND)
menu_music = pygame.mixer.Sound(MENU_SND)

# TODO: Load all game sounds
#init_sounds()

# Play the Intro
#intro()

# Run the Game loop
game()

# Cleanup and exit the game
cleanup()