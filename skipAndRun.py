""" Designing a game "skip and run" 
    player needs to avoid the incoming obstacles
"""
import os
# import  pygame
import pygame
# random for random number of enemies
import random
import time

# to keep track of keystrokes better import pygame.locals
from pygame.locals import(
    RLEACCEL,
    K_UP,   K_DOWN,
    K_LEFT, K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# player has 2 lives
global life 
life = 2

# setting up the window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 

# setting up the screen
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

# Mixer module for music
pygame.mixer.init()

# load background music
pygame.mixer.music.load("P:\dev\EAinternship\pygame\skipAndRun\_Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play( loops = -1)

# moving up,down and collision sounds
move_up_sound   = pygame.mixer.Sound("P:\dev\EAinternship\pygame\skipAndRun\_Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("P:\dev\EAinternship\pygame\skipAndRun\_Falling_putter.ogg")
collision_sound = pygame.mixer.Sound(os.path.join("skipAndRun\_Collision.ogg"))


# initializing pygame
pygame.init()

# Clock object to maintain the frame rate
clock = pygame.time.Clock()


# player class extending pygame.sprite.Sprite
class Player( pygame.sprite.Sprite ):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("P:\dev\EAinternship\pygame\skipAndRun\jet.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.life = 2

    # function to update user movements and positions
    def update(self,pressed_key):
        if pressed_key[K_UP]:
            pygame.Rect.move_ip(self.rect,0,-6)
            move_up_sound.play()

        if pressed_key[K_DOWN]:
            pygame.Rect.move_ip(self.rect,0,7)
            move_down_sound.play()

        if pressed_key[K_LEFT]:
            pygame.Rect.move_ip(self.rect,-7,0)

        if pressed_key[K_RIGHT]:
            pygame.Rect.move_ip(self.rect,6,0)

        # to check and keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# class Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()   # call to superclass constructor
        self.surf = pygame.image.load("P:\dev\EAinternship\pygame\skipAndRun\enemy.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)    # speed could be bw 5 and 20 pixel/move

    # update the enemy location  
    # move the sprite based on speed
    # remove the sprite when it passes left of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:   # when enemy is at left corner
            self.kill()


# class Cloud
class Cloud( pygame.sprite.Sprite ):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("P:\dev\EAinternship\pygame\skipAndRun\cloud.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-10, 0)
        # if it is at left corner of the screen
        if self.rect.right < 0:
            self.kill()



# CUSTOM EVENT to create enemies at a regular interval
ADDENEMY = pygame.USEREVENT + 1      # +1 UPDATES ENEMY ID BY 1
pygame.time.set_timer(ADDENEMY, 250)

# CUSTOM EVENT for Clouds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 500)


# INSTANTIATING THE PLAYER
player = Player()


# use of Sprite Groups to handle all_sprites as a group
#  1.> enemies Group and Cloud Group : to detect collision or position

enemies = pygame.sprite.Group()       # Sprite Group for enemies
all_sprites = pygame.sprite.Group()   # Group for all entities of game
all_sprites.add(player)               # add the player to Group
clouds = pygame.sprite.Group()        # Group for Clouds



# game loop
running = True
while running:
    # if user press the esc or quit
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running  = False

        elif event.type == QUIT:
            running = False

        # check if it is time to create new enemy
        elif event.type == ADDENEMY:
            new_enemy = Enemy()       # instantiate enemy
            enemies.add(new_enemy)    # add to enemies Group  
            all_sprites.add(new_enemy)    # add to all_sprites Group


        # check if it Cloud event is invoked 
        elif event.type == ADDCLOUD:
            # create new cloud and add it to all_sprites Group
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        

    # getting the pressed keys as dictionary
    pressed_keys = pygame.key.get_pressed()
    # to update the game, call the update() function 
    player.update(pressed_keys)

    # update the Enemy sprite Group
    enemies.update()

    # update the Clouds Group
    clouds.update()

    # fill the screen with Sky Blue color
    screen.fill((135,206,250))

    # Draw the Sprites on the screen
    # our all_sprites contains all the game entities
    # game loop will refresh all the entities w.r.t each frame
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    

    # Check for Collision detection using .spritecollideany(player,enemies)
    collide =  pygame.sprite.spritecollideany(player, enemies)
    if collide and player.life >= 1:
        player.life -= 1    

    elif collide and player.life == 0:    
        player.kill()
        # stop moving sounds
        move_up_sound.stop()
        move_down_sound.stop()
        # play the collsion sound
        collision_sound.play()
            
        # stop the loop
        running = False

    # push the items to the screen
    pygame.display.flip()

    #set the desired frame rate ( 30 FPS )
    clock.tick(30)


# Done! quit the game
pygame.quit()


     
