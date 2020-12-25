import pygame as pyg 
import random
import math
from pygame import mixer


# intialize game
pyg.init()

#title and icon
pyg.display.set_caption("Space invaders") 
icon = pyg.image.load('trial\\py_quicksort_visualisation\\venv\\rocket-ship_1.png')
pyg.display.set_icon(icon) 

#create screen
screen = pyg.display.set_mode((800,600))

# Background image
background = pyg.image.load('trial\\py_quicksort_visualisation\\venv\\background.png')

#Background sound
# mixer.music.load('trial\\py_quicksort_visualisation\\venv\\background.wav')
# mixer.music.play(-1)

#Player
playerimg = pyg.image.load('trial\\py_quicksort_visualisation\\venv\\space-invaders.png')
playerx  = 370
playery = 480
playerX_change = 0

#Enemy 
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyimg.append(pyg.image.load('trial\\py_quicksort_visualisation\\venv\\alien_rotated.png'))
    enemyx.append(random.randint(0 , 735))
    enemyy.append(random.randint(0,100))
    enemyx_change.append(4) 
    enemyy_change.append(36)

#Bullet
bulletimg = pyg.image.load('trial\\py_quicksort_visualisation\\venv\\bullet.png')
bulletx = 0
bullety = 480 
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"    #ready state you cant see bullet #fire state for bullet to be fired

score_value = 0 
font = pyg.font.Font('freesansbold.ttf' , 32)
textx = 10 
texty = 10 

def show_score(x,y):
    score = font.render("SCORE :" + str(score_value) , True , (255,255,255))
    screen.blit(score , (x , y))

game_over_font = pyg.font.Font('freesansbold.ttf' , 64) 
def game_over_text():
    game_over = game_over_font.render("GAME OVER" , True , (255,255,255))
    screen.blit(game_over , (200 , 250))


def player(x , y):
    screen.blit( playerimg , (x , y) )

def enemy(x ,y, i):
    screen.blit(enemyimg[i] , (x , y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg , (x+16 , y+10))

def iscollision(ex , ey, bx, by) :
    distance = math.sqrt(math.pow( (ex - bx),2 ) + math.pow((ey - by),2)) 
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True

while running:
    #RGB  Red , Blue , Green 
    screen.fill((0,0,0)) 
    #background 
    screen.blit(background , (0,0))
   
    for event in pyg.event.get():
        if event.type == pyg.QUIT :
            running = False 
    #checking for key mechanism 
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_LEFT :
                playerX_change = -5
            if event.key == pyg.K_RIGHT :
                playerX_change = 5
            if event.key == pyg.K_SPACE :
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('trial\\py_quicksort_visualisation\\venv\\laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(playerx , bullety)

        if event.type == pyg.KEYUP :
            if event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
                playerX_change = 0

    #boundaries for spaceship so that they dont go outside screen  
    playerx += playerX_change
    if playerx >=730:
        playerx = 730
    elif playerx <= 4:
        playerx = 4

    #bullet movement
    if bullety <= 0:
        bullety = 480 
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletx , bullety)
        bullety -= bullety_change

    #boundaries for enemies so that they dont go outside screen  & MOVEMENT
    for i in range(no_of_enemies):

        #GAME OVER
        if enemyy[i] >= 480:
            for j in range(no_of_enemies):
                enemyy[j] = 2000

            game_over_text() 
            break 

        enemyx[i] += enemyx_change[i]
        if enemyx[i] >=736:
            enemyx_change[i] = -4
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] <= 4:
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]

        collision = iscollision(enemyx[i] , enemyy[i] , bulletx , bullety)
        if collision:
            explosion_sound = mixer.Sound('trial\\py_quicksort_visualisation\\venv\\explosion.wav')
            explosion_sound.play()
            score_value += 1
            bullety = 480 
            bullet_state = "ready"
            enemyx[i] = random.randint(0 , 735) 
            enemyy[i] = random.randint(0,100)

        enemy(enemyx[i] , enemyy[i] , i)

    show_score(textx , texty)

    player(playerx , playery)
    pyg.display.update()