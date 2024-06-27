import pygame
from sys import exit
import random
import time

def getHighScore():
    try:
        with open('high_score.txt','r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

HIGHEST_SCORE = getHighScore()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/flappy.xcf').convert_alpha(), 0.5)
        self.rect = self.image.get_rect(midbottom = (640,360))
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
            if self.rect.right > 1280:
                self.rect.right = 1280

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.top += self.gravity

    def game_over(self):
        if self.rect.top >= 900:
            return True

    def update(self):
        self.player_input()
        self.apply_gravity()

class Bean(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)
        self.x_pos = random.randint(1,1280)
        self.y_pos = -10
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))
        

    def movement(self):
        self.rect.y += 2

    # def rotate(self):
    #      self.angle += self.rotation_speed
    #      self.image = pygame.transform.rotate(self.image, self.angle)
    #      self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))

    def destroy(self):
        if self.rect.y > 720:
            self.kill()

    def clear(self):
        self.kill()

    def update(self):
        #self.rotate()
        self.movement()
        self.destroy()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = random.randint(1,1280)
        self.y_pos = -10
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Sugar1.xcf').convert_alpha(), 0.3)
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))

    def movement(self):
        self.rect.y += 2

    def destroy(self):
        if self.rect.y > 720:
            self.kill()

    def clear(self):
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

def display_score2(pos):
    score = collision_count
    score_surface = font.render(f'SCORE: {score}',False,WHITE)
    score_rect = score_surface.get_rect(midtop = pos) #100,675
    screen.blit(score_surface,score_rect)

def displayHighScore(pos):
    high_score_surface = font.render(f'HIGH SCORE: {HIGHEST_SCORE}',False,WHITE)
    high_score_rect = high_score_surface.get_rect(midtop = pos)
    screen.blit(high_score_surface,high_score_rect)

def display_hp(pos):
    hp_surface = font.render("Health:",False,WHITE)
    hp_rect = hp_surface.get_rect(midtop=pos)
    screen.blit(hp_surface,hp_rect)

    pygame.draw.rect(screen, "red", (272,667,200,35))
    pygame.draw.rect(screen, (9, 216, 39), (272,667, 200 * ratio, 35))

def display_powerUp(pos):
    power_up_surface = font.render("Power Up:",False,WHITE)
    power_up_rect = power_up_surface.get_rect(midtop=pos)
    screen.blit(power_up_surface,power_up_rect)

    pygame.draw.rect(screen, (177,123,71), (585,667,200,35))
    pygame.draw.rect(screen, BLACK, (585,667, 200 * progress, 35))

def addBean(x):
    for i in range(x):
        obstacles.add(Bean())
def addEnemy(x):
    for i in range(x):
        obstacles.add(Enemy())

# def powerUpTimer():
#     B=5
#     start_time = pygame.time.get_ticks()
#     power_up_timer_active=True

#     if power_up_timer_active:
#         current_time = pygame.time.get_ticks()
#         elapsed_time = (current_time - start_time)/1000
#         if elapsed_time > power_up_duration:
#             power_up_timer_active=False
#             powerup=False
#             progress = 1
#             B=1





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

width = 1280
height = 720
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

game_active_background = pygame.image.load('Assets/Backgrounds/bkg1_1280x720.png')
game_intro_background =  pygame.image.load('Assets/Backgrounds/titlepage2_1280x720.png')
pause_menu_packground = pygame.image.load('Assets/Backgrounds/pause_1280x720.png')
game_over_background = pygame.image.load('Assets/Backgrounds/gameover_bkg_1280x720.png')
quit_button_img = pygame.image.load('Assets/Buttons/Quit Button1.png')
resume_button_img = pygame.image.load('Assets/Buttons/Resume Button1.png')

dashboard_surface = pygame.Surface((width,70))
dashboard_surface.fill((102, 64, 26))

bean_surface = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)

#Player Stats
health = 5
ratio = 1
progress = 1

#Game States

game_active = False
game_paused = False
flappy_died = False
powerup = False
B = 2
E = 2
power_up_timer_active=False
power_up_duration=10
start_time=None

#Game Over
rotation = 0
collision_count = 0
collision_sound = pygame.mixer.Sound('Assets/Sound/player-select.mp3')
collision_sound.set_volume(0.15)
game_over_sound = pygame.mixer.Sound('Assets/Sound/player-lose.wav')
game_over_sound.set_volume(0.3)
damage_sound = pygame.mixer.Sound('Assets/Sound/damage1-mixkit.wav')
damage_sound.set_volume(0.5)

Intro_suface = font.render(f'Press Space to Start',False,GREY)
Intro_rect = Intro_suface.get_rect(midbottom = (300,360))
Controls_surface = font.render("Use 'w,a,d' to move and press ESC to pause",False,GREY)
controls_rect = Controls_surface.get_rect(midbottom = (300,390))


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
                    addBean(B)
                    addEnemy(E)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                    if event.key == pygame.K_q:
                        game_paused = False
                        game_active = False

        else:
            if flappy_died == True:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    flappy_died = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    collision_count=0
                    flappy_died = False
                    game_active = True
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active == False:
                    player_gravity = 0
                    game_active = True
                     
    if game_active and game_paused == False:
        screen.blit(game_active_background,(0,0))
        player.draw(screen)
        player.update()
        for character in player:
            if character.game_over():
                flappy_died = True
                game_active = False

        obstacles.draw(screen)
        obstacles.update()
        
        screen.blit(dashboard_surface,(0,650))
        screen.blit(bean_surface, (150,660))

        display_hp((230,675))
        display_powerUp((530,675))
        display_score2((100,675))

        collisions = pygame.sprite.spritecollide(flappy,obstacles,True)
        for obstacle in collisions:
            if type(obstacle) == Bean:
                collision_count += 1
                collision_sound.play()
                if progress > 0:
                    progress-=0.1
                
            else:  #Player hit an enemy now
                damage_sound.play()
                health-=1
                ratio -= 0.2
                if health == 0:
                    game_over_sound.play()
                    time.sleep(3)
                    game_active = False
                    flappy_died = True
        if progress == 0:
            powerup = True

    elif game_active and game_paused:
        screen.blit(pause_menu_packground,(0,0))

        score_pause_surface = comicsans.render(f'Current Score: {collision_count}',False,BLACK)
        score_pause_rect = score_pause_surface.get_rect(midbottom = (640,70))
        screen.blit(score_pause_surface,score_pause_rect)

        button1 = Button(640,200, resume_button_img, 1)
        if button1.draw(): #resume button was clicked
            game_paused = False
        button2 = Button(640,300, quit_button_img, 1)
        if button2.draw():  # quit button was clicked
            game_paused = False
            game_active = False

    elif game_active == False and flappy_died == True:
        screen.blit(game_over_background,(0,0))
        if collision_count > HIGHEST_SCORE:
            HIGHEST_SCORE = collision_count
            with open('high_score.txt','w') as file:
                file.write(f"{collision_count}")
                
        displayHighScore((300,275))
        display_score2((300,300)) #293

        retry_surface = font.render(f'Press R to retry',False,WHITE)
        retry_rect = retry_surface.get_rect(midbottom = (300,350))
        home_surface = font.render(f'Press SPACE to return home',False,WHITE)
        home_rect = home_surface.get_rect(midbottom = (300,400))

        screen.blit(retry_surface,retry_rect)
        screen.blit(home_surface,home_rect)
        health = 5
        ratio = 1
        progress = 1

        #Reset the player back to the starting position
        for character in player:
            character.rect.midbottom = (640,360)
            character.gravity = 0
        obstacles.empty()

    else:
        screen.blit(game_intro_background,(0,0))
        screen.blit(Intro_suface,Intro_rect)
        screen.blit(Controls_surface,controls_rect)

        health = 5
        ratio = 1
        progress = 1

        #Reset the player back to the starting position
        for character in player:
            character.rect.midbottom = (640,360)
            character.gravity = 0
        obstacles.empty()

    pygame.display.update()
    clock.tick(60) #won't run faster than 60 frames per second
