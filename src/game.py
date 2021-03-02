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
import math    # Maths

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
   K_KP_1,     # 1 Key
   K_KP_2,     # 2 Key
   K_KP_3,     # 3 Key
   K_KP_4,     # 4 Key
   K_1,        # 1 Key
   K_2,        # 2 Key
   K_3,        # 3 Key
   K_4,        # 4 Key
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
COLOR_BLACK   = (  0,   0,   0)
COLOR_WHITE   = (255, 255, 255)
COLOR_RED     = (255,   0,   0)
COLOR_GREEN   = (  0, 255,   0)
COLOR_BLUE    = (  0,   0, 255)
COLOR_SKY     = (135, 206, 250)
COLOR_GRAY    = (128, 128, 128)
COLOR_YELLOW  = (255, 255,   0)
COLOR_ORANGE  = (255, 128,   0)
COLOR_YEL_GRN = (154, 205,  50)
COLOR_YEL_ORN = (245, 189,  31)

# Location of graphical assets, relative to project top level directory
PLANE_0_2_IMG       = "assets/plane_0_2.png"
PLANE_1_IMG         = "assets/plane_1.png"
PLANE_3_IMG         = "assets/plane_3.png"
MISSILE_IMG         = "assets/missile.png"
MISSILE_BIG_IMG     = "assets/missile_big.png"
CLOUD1_IMG          = "assets/cloud1.png"
CLOUD2_IMG          = "assets/cloud2.png"
CLOUD3_IMG          = "assets/cloud3.png"
ORB_RED_IMG         = "assets/red_orb.png"
ORB_BLUE_IMG        = "assets/blue_orb.png"
ORB_GREEN_IMG       = "assets/green_orb.png"
ORB_YELLOW_IMG      = "assets/yellow_orb.png"
ORB_RED_MINI_IMG    = "assets/red_orb_mini.png"
ORB_BLUE_MINI_IMG   = "assets/blue_orb_mini.png"
ORB_GREEN_MINI_IMG  = "assets/green_orb_mini.png"
ORB_YELLOW_MINI_IMG = "assets/yellow_orb_mini.png"
BULLET_0_IMG        = "assets/bullet_0.png"
BULLET_1_IMG        = "assets/bullet_1.png"
BULLET_2_IMG        = "assets/bullet_2.png"
BULLET_3_IMG        = "assets/bullet_3.png"
EXPLOSION_0_IMG     = "assets/explosion_0.png"
EXPLOSION_1_IMG     = "assets/explosion_1.png"
EXPLOSION_2_IMG     = "assets/explosion_2.png"
EXPLOSION_3_IMG     = "assets/explosion_3.png"
EXPLOSION_4_IMG     = "assets/explosion_4.png"
EXPLOSION_5_IMG     = "assets/explosion_5.png"
EXPLOSION_6_IMG     = "assets/explosion_6.png"

# Array of plane animation images
plane_animation_imgs = [PLANE_0_2_IMG, PLANE_1_IMG, PLANE_0_2_IMG, PLANE_3_IMG]
PLANE_FRAMES_PER_IMG = 2

# Array of bullet animation images
bullet_animation_imgs = [BULLET_0_IMG, BULLET_1_IMG, BULLET_2_IMG, BULLET_3_IMG]
BULLET_FRAMES_PER_IMG = 3

# Array of explosion animation images
explosion_animation_imgs = [EXPLOSION_0_IMG, EXPLOSION_1_IMG, EXPLOSION_2_IMG, EXPLOSION_3_IMG, EXPLOSION_4_IMG, EXPLOSION_5_IMG, EXPLOSION_6_IMG]
EXPLOSION_FRAMES_PER_IMG = 2

# Array of enemy images
enemy_imgs = [MISSILE_IMG, MISSILE_BIG_IMG]
# Array of enemy damage
enemy_dmg = [10, 25]
enemy_score = [50, 100]

# Array of cloud images
cloud_imgs = [CLOUD1_IMG, CLOUD2_IMG, CLOUD3_IMG]

# Array of orb images
orb_imgs = [ORB_RED_IMG, ORB_YELLOW_IMG, ORB_BLUE_IMG, ORB_GREEN_IMG]
orb_mini_imgs = [ORB_RED_MINI_IMG, ORB_YELLOW_MINI_IMG, ORB_BLUE_MINI_IMG, ORB_GREEN_MINI_IMG]
# Array of orb score values
orb_score = [50, 100, 200, 500]

# Object Movement patterns
movement_pattern = ["LINEAR", "SINE", "COSINE", "RISE", "FALL"]

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

# Max power level
MAX_POWER = 1
# Max of 1 of each type, no stacking
MAX_POWERUPS = 1

#------------------------------
# Classes
#------------------------------

# Player Class
class Player(pygame.sprite.Sprite):
   def __init__(self):
      super(Player, self).__init__()
      self.frame_cnt = 0
      self.img_cnt = 0
      self.surf = pygame.image.load(plane_animation_imgs[self.img_cnt]).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      self.rect = self.surf.get_rect()
      self.mask = pygame.mask.from_surface(self.surf)
      self.health = PLAYER_HEALTH_MAX
      self.exp = 0
      self.power = 0
      self.health_bar = None
      self.health_font = pygame.font.SysFont("Arial", 12)
      self.health_text = None
      self.powerups = [0, 0, 0, 0]
      #self.powerups = [1, 1, 1, 1] # For Testing
      self.shoot_cnt = 0

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
      if pressed_keys[K_KP_1] | pressed_keys[K_1]:
         self.use_power(0)
      if pressed_keys[K_KP_2] | pressed_keys[K_2]:
         self.use_power(1)
      if pressed_keys[K_KP_3] | pressed_keys[K_3]:
         self.use_power(2)
      if pressed_keys[K_KP_4] | pressed_keys[K_4]:
         self.use_power(3)

      # Keep the Player on the screen
      if self.rect.left <= 0:
         self.rect.left = 0
      if self.rect.right >= SCREEN_WIDTH:
         self.rect.right = SCREEN_WIDTH
      if self.rect.top <= 0:
         self.rect.top = 0
      if self.rect.bottom >= SCREEN_HEIGHT:
         self.rect.bottom = SCREEN_HEIGHT

      # Draw the correct sprite for the animation
      self.frame_cnt += 1
      if self.frame_cnt == PLANE_FRAMES_PER_IMG:
         self.frame_cnt = 0
         self.img_cnt += 1
         if self.img_cnt == len(plane_animation_imgs) - 1:
            self.img_cnt = 0
         self.surf = pygame.image.load(plane_animation_imgs[self.img_cnt]).convert()
         self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)

   # Increment the player's power
   def inc_power(self, amount):
      self.power += amount
      if self.power > MAX_POWER:
         self.power = MAX_POWER

   # Decrement the player's power
   def dec_power(self, amount):
      self.power -= amount
      if self.power < 0:
         self.power = 0

   # Collect an orb and add to the power-ups
   def collect_orb(self, orb_type):
      # Add the power-up
      if self.powerups[orb_type] < MAX_POWERUPS:
         self.powerups[orb_type] += 1

   # Increment the player's health
   def inc_health(self, amount):
      self.health += amount
      if self.health >= PLAYER_HEALTH_MAX:
         self.health = PLAYER_HEALTH_MAX

   # Decrement the player's health
   def dec_health(self, amount):
      self.health -= amount
      if self.health <= PLAYER_HEALTH_MIN:
         self.health = PLAYER_HEALTH_MIN

   # Get the player's current health
   def get_health(self):
      return self.health

   # Draw the player's health bar and power-ups
   def draw_health_bar(self, surf):
      # Set up bar size parameters
      width = PLAYER_HEALTH_MAX
      height = 20
      bar_fill = (self.health / PLAYER_HEALTH_MAX) * width

      # Create the rectangles
      bar_rect = pygame.Rect(5, 5, width, height)
      fill_rect = pygame.Rect(5, 5, bar_fill, height)
      
      # Get the health bar color
      if self.health >= 80:
         bar_color = COLOR_GREEN
      elif self.health >= 60:
         bar_color = COLOR_YEL_GRN
      elif self.health >= 50:
         bar_color = COLOR_YELLOW
      elif self.health >= 40:
         bar_color = COLOR_YEL_ORN
      elif self.health >= 20:
         bar_color = COLOR_ORANGE
      else:
         bar_color = COLOR_RED

      # Draw the rectangles
      pygame.draw.rect(surf, bar_color, fill_rect)
      pygame.draw.rect(surf, COLOR_BLACK, bar_rect, 2)

      # Draw the text value of the health
      self.health_text = self.health_font.render("{}/{}".format(self.health, PLAYER_HEALTH_MAX), 1, COLOR_BLACK)
      surf.blit(self.health_text, ((bar_rect.left + (bar_rect.width / 2) - (self.health_text.get_width() / 2)), (bar_rect.top + (bar_rect.height / 2) - (self.health_text.get_height() / 2))))

      # Draw available power-ups
      i = 0
      for pwrup in self.powerups:
         if pwrup > 0:
            # Draw it
            pwrup_img = pygame.image.load(orb_mini_imgs[i]).convert()
            pwrup_img.set_colorkey(COLOR_BLACK, RLEACCEL)
            surf.blit(pwrup_img, (bar_rect.left + 18 + (20 * i), (bar_rect.bottom + 5)))
         i += 1

   # Shoot!
   def shoot(self):
      # Spawn bullets from the front right of the plane
      if self.power > 0:
         new_bullet_1 = Bullet(self.rect.right - (self.rect.width / 4), self.rect.bottom - (self.rect.height / 6), movement_pattern[0])
         new_bullet_2 = Bullet(self.rect.right - (self.rect.width / 4), self.rect.bottom - (self.rect.height / 6), movement_pattern[3])
         new_bullet_3 = Bullet(self.rect.right - (self.rect.width / 4), self.rect.bottom - (self.rect.height / 6), movement_pattern[4])
         bullets.add(new_bullet_1)
         all_sprites.add(new_bullet_1)
         bullets.add(new_bullet_2)
         all_sprites.add(new_bullet_2)
         bullets.add(new_bullet_3)
         all_sprites.add(new_bullet_3)
      else:
         new_bullet = Bullet(self.rect.right - (self.rect.width / 4), self.rect.bottom - (self.rect.height / 6), movement_pattern[0])
         bullets.add(new_bullet)
         all_sprites.add(new_bullet)

      # Don't play sound for every bullet
      if self.shoot_cnt % 3 == 0:
         pew_sound.play()
      self.shoot_cnt += 1

   def use_power(self, power):
      if self.powerups[power] > 0:
         if power == 0:
            # Red Orb: Wave of Death
            new_wave = Wave(self.rect.center)
            waves.append(new_wave)
         elif power == 1:
            # Yellow Orb: Gun Upgrade
            self.inc_power(1)
         elif power == 2:
            # Blue Orb: Shield
            new_shield = Shield(self.rect.center, self.rect.width, self.rect.height)
            shields.append(new_shield)
         elif power == 3:
            # Green Orb: Full Heal
            self.inc_health(PLAYER_HEALTH_MAX)
         
         # Remove the power-up
         self.powerups[power] -= 1

# Calculate the diagonal of the screen
MAX_RADIUS = math.sqrt((SCREEN_WIDTH * SCREEN_WIDTH) + (SCREEN_HEIGHT * SCREEN_HEIGHT))
# Wave/Ring Class
class Wave(object):
   def __init__(self, center):
      self.center = center
      self.radius = 10
      self.alive = True
      bad_sound.play()

   def update(self):
      if self.radius < MAX_RADIUS:
         self.radius += 15
      else:
         self.alive = False

   def blit(self, surf):
      if self.alive == True:
         self.circle = pygame.draw.circle(surf, COLOR_RED, self.center, self.radius, 5)

   def get_center(self):
      return self.center

   def get_radius(self):
      return self.radius

   def is_alive(self):
      return self.alive

# Define max shield HP
SHIELD_HP_MAX = 5
# Shield Class
class Shield(object):
   def __init__(self, center, width, height):
      self.center = center
      self.x, self.y = self.center
      self.width = width
      self.height = height
      self.radius = 125
      self.hp = SHIELD_HP_MAX
      bad_sound.play()

   def update(self, pressed_keys):
      # Move with player
      if pressed_keys[K_UP] | pressed_keys[K_w]:
         self.y -= PLAYER_MOVE_STEP
      if pressed_keys[K_DOWN] | pressed_keys[K_s]:
         self.y += PLAYER_MOVE_STEP
      if pressed_keys[K_LEFT] | pressed_keys[K_a]:
         self.x -= PLAYER_MOVE_STEP
      if pressed_keys[K_RIGHT] | pressed_keys[K_d]:
         self.x += PLAYER_MOVE_STEP

      # Keep the Shield aligned with the player
      if self.x <= (self.width / 2):
         self.x = (self.width / 2)
      if self.x >= (SCREEN_WIDTH - (self.width / 2)):
         self.x = SCREEN_WIDTH - (self.width / 2)
      if self.y <= (self.height / 2):
         self.y = (self.height / 2)
      if self.y >= SCREEN_HEIGHT - (self.height / 2):
         self.y = SCREEN_HEIGHT - (self.height / 2)

      # Update the center position
      self.center = (self.x, self.y)

   def blit(self, surf):
      self.circle = pygame.draw.circle(surf, COLOR_BLUE, self.center, self.radius, self.hp+1)

   def get_center(self):
      return self.center

   def get_radius(self):
      return self.radius

   def is_alive(self):
      return self.hp > 0

   def hit(self):
      self.hp -= 1
      if self.hp < 0:
         self.hp = 0

# Bullet Class
class Bullet(pygame.sprite.Sprite):
   def __init__(self, x, y, path):
      super(Bullet, self).__init__()
      self.frame_cnt = 0
      self.img_cnt = 0
      self.surf = pygame.image.load(bullet_animation_imgs[self.img_cnt]).convert()
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
      self.path = path

   def update(self):
      # Linear
      if self.path == movement_pattern[0]:
         self.rect.move_ip(self.speed, 0)
      # Rising
      elif self.path == movement_pattern[3]:
         self.rect.move_ip(self.speed, -0.01 * self.rect.x)
      # Falling
      elif self.path == movement_pattern[4]:
         self.rect.move_ip(self.speed, 0.01 * self.rect.x)

      self.rect.move_ip(self.speed, 0)
      if self.rect.left > SCREEN_WIDTH:
         self.kill()

      # Draw the correct sprite for the animation
      self.frame_cnt += 1
      if self.frame_cnt == BULLET_FRAMES_PER_IMG:
         self.frame_cnt = 0
         # Latch on the last image
         if self.img_cnt < len(bullet_animation_imgs) - 1:
            self.img_cnt += 1
            self.surf = pygame.image.load(bullet_animation_imgs[self.img_cnt]).convert()
            self.surf.set_colorkey(COLOR_BLACK, RLEACCEL)

   def get_center(self):
      return ((self.rect.right - (self.rect.width / 2)),(self.rect.bottom - (self.rect.height / 2)))

# Explosion Class
class Explosion(pygame.sprite.Sprite):
   def __init__(self, x, y):
      super(Explosion, self).__init__()
      self.frame_cnt = 0
      self.img_cnt = 0
      self.surf = pygame.image.load(explosion_animation_imgs[self.img_cnt]).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            # Spawn based on location of bullet
            x, y
         )
      )
      #self.mask = pygame.mask.from_surface(self.surf)

   def update(self):
      # Draw the correct sprite for the animation
      self.frame_cnt += 1
      if self.frame_cnt == EXPLOSION_FRAMES_PER_IMG:
         self.frame_cnt = 0
         # Latch on the last image
         if self.img_cnt < len(explosion_animation_imgs) - 1:
            self.img_cnt += 1
            self.surf = pygame.image.load(explosion_animation_imgs[self.img_cnt]).convert()
            self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
         else:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
   def __init__(self):
      super(Enemy, self).__init__()
      self.type = random.randint(0, len(enemy_imgs) - 1)
      self.surf = pygame.image.load(enemy_imgs[self.type]).convert()
      self.surf.set_colorkey(COLOR_WHITE, RLEACCEL)
      self.rect = self.surf.get_rect(
         center = (
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(10, SCREEN_HEIGHT - 10)
         )
      )
      self.mask = pygame.mask.from_surface(self.surf)
      self.speed = random.randint(8, 20)
      self.path = movement_pattern[random.randint(0, len(movement_pattern) - 1)]
      self.health = 1
      self.dmg = enemy_dmg[self.type]
      self.score = enemy_score[self.type]

   # Move the sprite based on speed and pattern
   def update(self):
      # Linear
      if self.path == movement_pattern[0]:
         self.rect.move_ip(-self.speed, 0)
      # Sine Wave
      elif self.path == movement_pattern[1]:
         self.rect.move_ip(-self.speed, 5 * math.sin(self.rect.x / 250))
      # Cosine Wave
      elif self.path == movement_pattern[2]:
         self.rect.move_ip(-self.speed, 5 * math.cos(self.rect.x / 250))
      # Rising
      elif self.path == movement_pattern[3]:
         self.rect.move_ip(-self.speed, -0.01 * self.rect.x)
      # Falling
      elif self.path == movement_pattern[4]:
         self.rect.move_ip(-self.speed, 0.01 * self.rect.x)
      
      # Remove the sprite when it passes the left edge of the screen
      if self.rect.right < 0:
         self.kill()

   # Get amount of damage the enemy does
   def get_dmg(self):
      return self.dmg

   def get_score(self):
      return self.score

   def get_center(self):
      return ((self.rect.right - (self.rect.width / 2)),(self.rect.bottom - (self.rect.height / 2)))

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

   def get_score(self):
      return orb_score[self.type]

   def get_type(self):
      return self.type

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

   # Array of options (drawn from bottom up)
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
                  #options_menu()
                  paused = False # UNDO
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
               # Only restart the music if we're not quitting
               if running == True:
                  plane_fly_sound.play(loops=-1 == True)
                  pygame.mixer.music.play(loops=-1)
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

         # Update shield objects
         for shield in shields:
            shield.update(pressed_keys)

         # Update the bullets
         bullets.update()

         # Update enemy positions and count how many are remaining
         enemies.update()

         # Update cloud positions
         clouds.update()

         # Update orb positions
         orbs.update()

         # Update wave objects
         for wave in waves:
            wave.update()

         # Fill the background (sky blue)
         screen.fill(COLOR_SKY)

         # Draw all sprites to the screen
         for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

         # Draw shield objects to the screen
         for shield in shields:
            shield.blit(screen)
            if shield.is_alive() == False:
               shields.remove(shield)

         # Draw wave objects to the screen
         for wave in waves:
            wave.blit(screen)
            if wave.is_alive() == False:
               waves.remove(wave)

         # Check for a collision between the Player and all enemies
         enemy = pygame.sprite.spritecollideany(player, enemies)
         if enemy != None:
            # Check the collision mask for pixel-perfect collision
            if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
               new_explosion = Explosion(*enemy.get_center())
               explosions.add(new_explosion)
               all_sprites.add(new_explosion)
               # Apply damage
               player.dec_health(enemy.get_dmg())
               player.dec_power(1)
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
                     new_explosion = Explosion(*bullet.get_center())
                     explosions.add(new_explosion)
                     all_sprites.add(new_explosion)
                     hit.kill()
                     bullet.kill()

         # Check for a collision between Wave objects and enemies
         for wave in waves:
            play_sound = True
            wave_center_x, wave_center_y = wave.get_center()
            for enemy in enemies:
               enemy_center_x, enemy_center_y = enemy.rect.center
               dist_y = enemy_center_y - wave_center_y
               dist_x = enemy_center_x - wave_center_x
               dist = math.sqrt((dist_x * dist_x) + (dist_y * dist_y))

               # Kill the enemy if they are in the circle
               if dist <= wave.get_radius():
                  new_explosion = Explosion(*enemy.get_center())
                  explosions.add(new_explosion)
                  all_sprites.add(new_explosion)
                  score.add(enemy.get_score())
                  enemy.kill()
                  if play_sound == True:
                     boom_sound.play()
                     play_sound = False

         # Check for a collision between Shield objects and enemies
         for shield in shields:
            play_sound = True
            shield_center_x, shield_center_y = shield.get_center()
            for enemy in enemies:
               enemy_center_x, enemy_center_y = enemy.rect.center
               dist_y = enemy_center_y - shield_center_y
               dist_x = enemy_center_x - shield_center_x
               dist = math.sqrt((dist_x * dist_x) + (dist_y * dist_y))

               # Kill the enemy if they are in the circle
               if dist <= shield.get_radius():
                  new_explosion = Explosion(*enemy.get_center())
                  explosions.add(new_explosion)
                  all_sprites.add(new_explosion)
                  score.add(enemy.get_score())
                  enemy.kill()
                  shield.hit()
                  if play_sound == True:
                     boom_sound.play()
                     play_sound = False

         # Update explosions
         explosions.update()

         # Check for a collision between the Player and all orbs
         orb = pygame.sprite.spritecollideany(player, orbs)
         if orb != None:
            # Check the collision mask for pixel-perfect collision
            if pygame.sprite.spritecollide(player, orbs, True, pygame.sprite.collide_mask):
               # If so, apply the power-up and play a sound
               player.collect_orb(orb.get_type())
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
            # TODO Implement a death animation, or at least allow the final explosions to complete
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
pygame.time.set_timer(ADDORB, 15000)

# Create Groups to hold enemy sprites and all sprited
# - enemies is used for collision detection and postition updates
# - orbs is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
orbs = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Wave object group
waves = []

# Shield object group
shields = []

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