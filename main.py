import pygame
import random
from random import randint as rd
import math
from pygame import mixer as mx  

# initialize the pygame
pygame.init()

# game screen
screen=pygame.display.set_mode((800,600))

# backgorund image
background=pygame.image.load('images/background.png')

# Title and Icon of game window
pygame.display.set_caption("Space Invaders")
game_icon=pygame.image.load('images/ufo.png')
pygame.display.set_icon(game_icon)

# Background music
mx.music.load('sounds/background.wav')
mx.music.set_volume(0.5)
mx.music.play(-1)


# Player Object
player_image=pygame.image.load('images/player.png')
player={
    'image':player_image,
    'x':370,
    'y':480,
    'dx':0
}

# Enemy Objects
def make_enemy():        
    enemy_image=pygame.image.load('images/enemy.png')
    enemy={
        'image':enemy_image,
        'x': rd(0,730),
        'y': rd(5,100),
        'dx': random.random()+3,
        'dy': 30
    }
    
    return enemy

enemies=[make_enemy() for x in range(10)]

def respawn_enemy(enemy):
    enemy['x']=rd(0,730)
    enemy['y']=rd(0,150)
   

# bullet object
bullet_image=pygame.image.load('images/bullet.png')
bullet={
    'image':bullet_image,
    'x': 0,
    'y':480,
    'dy': 15,
    'fire':False
}

# game restart button
rg_font=pygame.font.Font('fonts/Fun Mountain.ttf',40)
color = (255,255,255) # white color
color_light = (170,170,170) # light shade
color_dark = (100,100,100) # dark shade


# score object
font=pygame.font.Font('fonts/Homemade Donuts.ttf',32)
score_value=0

# Game Over Text
go_font=pygame.font.Font('fonts/Fun Mountain.ttf',64)

def show_restart_btn(mouse):
    text=rg_font.render('Restart',True,color)
    if 330 <= mouse[0] <= 510 and 330 <= mouse[1] <= 400:
        pygame.draw.rect(screen,color_light,[330,330,180,60])
    else:
        pygame.draw.rect(screen,color_dark,[330,330,180,60])
    
    screen.blit(text,(350,340))

def game_over():
    game_over_text=go_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over_text,(250,250))

def show_score(x,y):
    score=font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def move_player(player):
    x=player['x']
    y=player['y']
    image=player['image']
    screen.blit(image,((x,y)))

def move_enemy(enemy):    
    image=enemy['image']
    x=enemy['x']
    y=enemy['y']
    
    screen.blit(image,((x,y)))
    
def check_boundaries_player(key):
    return (key=='left' and player['x']<=0) or (key=='right' and player['x']>=736)
    
def check_boundaries_enemy(enemy):
    if(enemy['x']<=0 or enemy['x']>=736):
        enemy['dx']*=-1
        return True
    
    return False

def fire_bullet(bullet):
    x=bullet['x']
    y=bullet['y']
    image=bullet['image']
    bullet['fire']=True
    
    screen.blit(image,(x + 16,y + 10))
    
def isCollision(enemy,bullet):
    x1=enemy['x']
    y1=enemy['y']
    x2=bullet['x']
    y2=bullet['y']
    
    distance=math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    
    return True if distance < 25 else False

def remove_enemies(enemy):
    enemy['y']=2000
    return enemy 

def game_restart(player,enemies):
    
    global go_flag
    go_flag=False
        
    player['x']=370
    player['y']=480
    
    for enemy in enemies:
        enemy['y']=rd(5,150)
        enemy['dx']=random.random()+3
        enemy['x']=rd(0,730)   

# game variables
running=True
key=''
level_up=True
go_flag=False # flag to check if game is over or not

while running:
    
    screen.fill((5,5,5))
    
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT:
            running=False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # check if mouse is pressed down in restart button area
            mouse=pygame.mouse.get_pos()
            if 330 <= mouse[0] <= 510 and 330 <= mouse[1] <= 400 and go_flag:
                score_value=0
                game_restart(player,enemies)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player['dx']= -4.6
                key='left'              
                
            if event.key == pygame.K_RIGHT:
                player['dx']= 4.6  
                key='right'
            
            if event.key == pygame.K_SPACE:
                if bullet['fire'] is False:                    
                    bullet['x']=player['x']
                    fire_bullet(bullet)
                    bullet_sound=mx.Sound('sounds/laser.wav')
                    bullet_sound.play()                                      
         
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and key=='left') or (event.key == pygame.K_RIGHT and key=='right'):
                player['dx']= 0.0
                
    
    # updating player's x value    
    if (check_boundaries_player(key)):
        player['dx']=0    
                     
    player['x']+=player['dx']    
    move_player(player)   
    
    # bullet firing
    if bullet['fire'] is True:
        bullet['y']-=bullet['dy']
        fire_bullet(bullet)
        if bullet['y']<=0:
            bullet['fire']=False
            bullet['y']=480
    
    for enemy in enemies:
        
        # Game Over
        if enemy['y']>441:
            enemies=map(remove_enemies,enemies)
            enemies=list(enemies)
            go_flag=True
            game_over()
            show_restart_btn(pygame.mouse.get_pos())
            break                    
        
        # updating enemy's cordinates
        if(check_boundaries_enemy(enemy)):
            enemy['y']+=enemy['dy']
        
        enemy['x']+=enemy['dx']
        
    
        # Collision
        collision=isCollision(enemy,bullet)
    
        if collision:
            bullet['y']=480
            bullet['fire']=False
            respawn_enemy(enemy)
            score_value += 1
            collision_sound=mx.Sound('sounds/explosion.wav')
            collision_sound.play()  
          
        
        move_enemy(enemy) 
    
    # some fun by increasing the speed of the enemy
    if score_value==50 and level_up :
        for enemy in enemies:            
            enemy['dx']=random.random()+4            
        level_up=False
    elif score_value==100 and level_up :
        for enemy in enemies:            
            enemy['dx']=random.random()+6
            print(enemy['dx'])
        level_up=False
    elif score_value!=50 and score_value !=100:
        level_up=True       
        
    show_score(10,10)
    
    pygame.display.update()
            
    
        
        
    

