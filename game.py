import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/flappy.xcf').convert_alpha(), 0.5)
        self.rect = self.image.get_rect(midbottom = (400,250))
        self.gravity = 0
        # self.jump_sound = pygame.mixer.Sound('Assets/Sound/jump2.wav')
        # self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.gravity = -7
            #self.jump_sound.play()
            if self.rect.top < 0:
                self.rect.top = 0
        if keys[pygame.K_a]:
            self.rect.x -= 3
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_d]:
            self.rect.x += 3
            if self.rect.right > 800:
                self.rect.right = 800

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.top += self.gravity

    def game_over(self):
        if self.rect.top >= 700:
            return True

    def update(self):
        self.player_input()
        self.apply_gravity()

class Bean(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)
        self.x_pos = random.randint(1,800)
        self.y_pos = -10
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))
        

    def movement(self):
        self.rect.y += 2

    # def rotate(self):
    #      self.angle += self.rotation_speed
    #      self.image = pygame.transform.rotate(self.image, self.angle)
    #      self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))

    def destroy(self):
        if self.rect.y > 500:
            self.kill()

    def update(self):
        #self.rotate()
        self.movement()
        self.destroy()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = random.randint(1,800)
        self.y_pos = -10
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Sugar1.xcf').convert_alpha(), 0.3)
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))

    def movement(self):
        self.rect.y += 2

    def destroy(self):
        if self.rect.y > 500:
            self.kill()

    def update(self):
        #self.rotate()
        self.movement()
        self.destroy()

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button and has clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # check if left mouse button clicked
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def display_score2():
    score = collision_count
    score_surface = font.render(f'SCORE: {score}',False,WHITE)
    score_rect = score_surface.get_rect(midtop = (100,450))
    screen.blit(score_surface,score_rect)



# def object_movement(object_rect_list):
#     if object_rect_list:
#         for obj_rect in object_rect_list:
#             obj_rect.y += 5  #make object fall
#             Rotated_surface = pygame.transform.rotate(Food_surface, rotation)    #make object rotate
#             screen.blit(Rotated_surface, obj_rect)

#         object_rect_list = [object for object in object_rect_list if object.y <600]
                        
#         return object_rect_list
#     else:
#         return []

pygame.init()

width = 800
height = 500
screen = pygame.display.set_mode((width, height))   #main display surface
pygame.display.set_caption("Flappuccino")
font = pygame.font.Font(None, 30)
arial = pygame.font.SysFont("arialblack",30)
comicsans = pygame.font.SysFont("comic_sans.ttf",30)
WHITE = (255,255,255)
GREY = (64,64,64)
BLACK = (0,0,0)

#Groups
obstacles = pygame.sprite.Group()

flappy = Player()
player = pygame.sprite.GroupSingle()
player.add(flappy)

game_active_background = pygame.image.load('Assets/Backgrounds/GameActiveBackground1.png')
game_intro_background =  pygame.image.load('Assets/Backgrounds/IntroBackground1.png')
pause_menu_packground = pygame.image.load('Assets/Backgrounds/PauseMenu1.png')
quit_button_img = pygame.image.load('Assets/Buttons/Quit Button1.png')
resume_button_img = pygame.image.load('Assets/Buttons/Resume Button1.png')

dashboard_surface = pygame.Surface((800,70))
dashboard_surface.fill((102, 64, 26))

bean_surface = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)

#Player Stats
health = 5
ratio = 1

#Game States

game_active = False
game_paused = False
rotation = 0
collision_count = 0
collision_sound = pygame.mixer.Sound('Assets/Sound/player-select.mp3')
collision_sound.set_volume(0.15)
game_over_sound = pygame.mixer.Sound('Assets/Sound/player-lose.wav')
game_over_sound.set_volume(0.3)
damage_sound = pygame.mixer.Sound('Assets/Sound/damage1-mixkit.wav')
damage_sound.set_volume(0.5)

object_timer = pygame.USEREVENT +1
pygame.time.set_timer(object_timer, 900)
#Frame rate. we need to set a upper and lower bound for it
clock = pygame.time.Clock()


while True: # lets our code keep running forever epic. we break if the game ends
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if game_paused == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                         player_gravity = -15
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                if event.type == object_timer and game_active:
                    obstacles.add(Bean())
                    obstacles.add(Enemy())

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_gravity = 0
                game_active = True
                     
    if game_active and game_paused == False:
        screen.blit(game_active_background,(0,0))
        #screen.blit(Player_surface,Player_rect)
        player.draw(screen)
        player.update()
        for character in player:
            if character.game_over():
                game_active = False

        obstacles.draw(screen)
        obstacles.update()
        
        screen.blit(dashboard_surface,(0,430))
        screen.blit(bean_surface, (150,435))

        pygame.draw.rect(screen, "red", (242,446,200,35))
        pygame.draw.rect(screen, (9, 216, 39), (242,446, 200 * ratio, 35))
        
        display_score2()

        collisions = pygame.sprite.spritecollide(flappy,obstacles,True)
        for obstacle in collisions:
            if type(obstacle) == Bean:
                collision_count += 1
                collision_sound.play()
            else:  #Player hit an enemy now
                damage_sound.play()
                health-=1
                ratio -= 0.2
                if health == 0:
                    game_active = False
                    game_over_sound.play()
    
        rotation += 3

    elif game_active and game_paused:
        screen.blit(pause_menu_packground,(0,0))

        score_pause_surface = comicsans.render(f'Current Score: {collision_count}',False,BLACK)
        score_pause_rect = score_pause_surface.get_rect(midbottom = (400,70))
        screen.blit(score_pause_surface,score_pause_rect)

        button1 = Button(400,200, resume_button_img, 1)
        if button1.draw(): #resume button was clicked
            game_paused = False
        button2 = Button(400,300, quit_button_img, 1)
        if button2.draw():  # quit button was clicked
            game_paused = False
            game_active = False
        
    else:
        if collision_count != 0 and game_paused == False:
            game_over_sound.play()
        screen.blit(game_intro_background,(0,0))
        Gameover_suface = font.render(f'Press Space to Start',False,GREY)
        gameover_rect = Gameover_suface.get_rect(midbottom = (300,250))

        Controls_surface = font.render("Use 'w,a,d' to move and press ESC to pause",False,GREY)
        controls_rect = Controls_surface.get_rect(midbottom = (300,285))
        screen.blit(Gameover_suface,gameover_rect)
        screen.blit(Controls_surface,controls_rect)
        collision_count = 0
        health = 5
        ratio = 1

        #Reset the player back to the starting position
        for character in player:
            character.rect.midbottom = (400,250)
            character.gravity = 0
        
       
    pygame.display.update()
    clock.tick(60) #won't run faster than 60 frames per second
