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



class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
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
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)
        self.x_pos = random.randint(1,1280)
        self.y_pos = -10
        self.speed = speed
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))
        

    def movement(self):
        self.rect.y += self.speed
    def relocate(self):
            self.rect.y = -20
            self.rect.x = random.randint(1,1280)
    def offscreen(self):
        if self.rect.y > 720:
            self.relocate()
    def collide(self):
        self.kill()

    def update(self):
        self.movement()
        self.offscreen()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,speed):
        super().__init__()
        self.x_pos = random.randint(1,1280)
        self.y_pos = -10
        self.speed = speed
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Sugar1.xcf').convert_alpha(), 0.3)
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))

    def movement(self):
        self.rect.y += self.speed

    def relocate(self):
            self.rect.y = -20
            self.rect.x = random.randint(1,1280)
    def offscreen(self):
        if self.rect.y > 720:
            self.relocate()
    def collide(self):
        self.kill()

    def update(self):
        self.movement()
        self.offscreen()

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

def display_score2(pos,collision_count): #UPDATED
    score = collision_count
    score_surface = font.render(f'SCORE: {score}',False,WHITE)
    score_rect = score_surface.get_rect(midtop = pos) #100,675
    screen.blit(score_surface,score_rect)

def displayHighScore(pos, highest_score):  #UPDATE
    high_score_surface = font.render(f'HIGH SCORE: {highest_score}',False,WHITE)
    high_score_rect = high_score_surface.get_rect(midtop = pos)
    screen.blit(high_score_surface,high_score_rect)

def display_hp(pos, health):  #UPDATED
    hp_surface = font.render("Health:",False,WHITE)
    hp_rect = hp_surface.get_rect(midtop=pos)
    screen.blit(hp_surface,hp_rect)

    pygame.draw.rect(screen, "red", (272,667,200,35))
    pygame.draw.rect(screen, (9, 216, 39), (272,667, 200 * health, 35))

def display_powerUp(pos, progress): #UPDATED
    power_up_surface = font.render("Power Up:",False,WHITE)
    power_up_rect = power_up_surface.get_rect(midtop=pos)
    screen.blit(power_up_surface,power_up_rect)

    pygame.draw.rect(screen, (177,123,71), (585,667,200,35))
    pygame.draw.rect(screen, BLACK, (585,667, 200 * progress, 35))

def addBean(x, obstacles,speed):
    for i in range(x):
        obstacles.add(Bean(speed))
def addEnemy(x, obstacles,speed):
    for i in range(x):
        obstacles.add(Enemy(speed))
def elapsed_time(start_time):
    current_time = pygame.time.get_ticks()
    return (current_time - start_time)/1000
def numObj(obstacles,thing):
    count = [x for x in obstacles.sprites() if isinstance(x,thing)]
    return len(count)

pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #main display surface
pygame.display.set_caption("Flappuccino")
font = pygame.font.Font(None, 30)
arial = pygame.font.SysFont("arialblack",30)
comicsans = pygame.font.SysFont("comic_sans.ttf",30)
WHITE = (255,255,255)
GREY = (64,64,64)
BLACK = (0,0,0)

#LOAD ASSETS
flappy_image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/flappy.xcf').convert_alpha(), 0.5)
americano_image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/americano.xcf').convert_alpha(), 0.65)
messy_flappy_image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/messy_flappy.xcf').convert_alpha(), 0.5)


game_active_background = pygame.image.load('Assets/Backgrounds/bkg1_1280x720.png').convert()
game_intro_background =  pygame.image.load('Assets/Backgrounds/titlepage2_1280x720.png').convert()
pause_menu_packground = pygame.image.load('Assets/Backgrounds/pause_1280x720.png').convert()
game_over_background = pygame.image.load('Assets/Backgrounds/gameover_bkg_1280x720.png').convert()
quit_button_img = pygame.image.load('Assets/Buttons/Quit Button1.png').convert()
resume_button_img = pygame.image.load('Assets/Buttons/Resume Button1.png').convert()
single_mode_button_img = pygame.image.load('Assets/Buttons/Single Mode.xcf').convert_alpha()
coop_mode_button_img = pygame.image.load('Assets/Buttons/Coop Mode.xcf').convert_alpha()
dashboard_surface = pygame.Surface((WIDTH,70))
dashboard_surface.fill((102, 64, 26))
bean_surface = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)

#Game Over
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

clock = pygame.time.Clock()

def main_menu():
    while True:
        screen.blit(game_intro_background,(0,0))
        screen.blit(Intro_suface,Intro_rect)
        screen.blit(Controls_surface,controls_rect)

        single_player_button = Button(180,470,single_mode_button_img,1.3)
        two_player_button = Button(410,470,coop_mode_button_img,1.3)
        if single_player_button.draw():
            print("clicked single player")
            singleMode()
        if two_player_button.draw():
            #coopMode()
            print("clicked two player")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)

def retry_menu(collision_count,player,obstacles):
    while True:
        high_score = getHighScore()
        screen.blit(game_over_background,(0,0))
        if collision_count > high_score:
            high_score = collision_count
            with open('high_score.txt','w') as file:
                file.write(f"{collision_count}")

        displayHighScore((300,275), high_score)
        display_score2((300,300), collision_count) #293

        retry_surface = font.render(f'Press R to retry',False,WHITE)
        retry_rect = retry_surface.get_rect(midbottom = (300,350))
        home_surface = font.render(f'Press SPACE to return home',False,WHITE)
        home_rect = home_surface.get_rect(midbottom = (300,400))

        screen.blit(retry_surface,retry_rect)
        screen.blit(home_surface,home_rect)

        #Reset the player back to the starting position
        for character in player:
            character.rect.midbottom = (640,360)
            character.gravity = 0
        obstacles.empty()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_menu()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                singleMode()
        pygame.display.update()
        clock.tick(60)

#GAME MODES
def singleMode():
    #initialize parameters
    health = 1
    progress = 1
    collision_count = 0

    game_active = True
    game_paused = False
    flappy_died = False
    powerup = False
    B = 1
    E = 1
    speed = 2
    power_up_time=False
    power_up_duration=10
    start_time=None

    sprite_spawn = 900
    object_timer = pygame.USEREVENT +1
    pygame.time.set_timer(object_timer, sprite_spawn)
    object_speed_timer = pygame.USEREVENT +2
    pygame.time.set_timer(object_speed_timer,60000)

    #Groups
    obstacles = pygame.sprite.Group()

    flappy = Player(messy_flappy_image)
    player = pygame.sprite.GroupSingle()
    player.add(flappy)

    while True: # lets our code keep running forever epic. we break if the game ends
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if not game_paused:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_paused = True
                    if event.type == object_timer:
                        #check whether we enough enough objects in the group already
                        if len(obstacles.sprites()) < 15:
                            addBean(B, obstacles,speed)
                            addEnemy(E, obstacles,speed)
                        elif sprite_spawn == 900:
                            sprite_spawn = 10000
                            pygame.time.set_timer(object_timer,sprite_spawn)
                        else:
                            addBean(B, obstacles,speed)
                            addEnemy(E, obstacles,speed)
                    if event.type == object_speed_timer: #find a way to sleep creating new objects, so the old ones are off the screen before increasing timer
                        speed +=0.01
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_paused = False
                        if event.key == pygame.K_q:
                            game_paused = False
                            game_active = False
            else:
                if flappy_died:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        main_menu()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        retry_menu(collision_count,player,obstacles)

        # GAME ACTIVE AND POWER UP NOT ACTIVE           
        if game_active and not game_paused and not powerup: 
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

            display_hp((230,675), health)
            display_powerUp((530,675), progress)
            display_score2((100,675), collision_count)

            if progress < 0:
                B=5
                E=0
                print("power up started")
                print(f"We are drawing {B} beans per tick")
                start_time = pygame.time.get_ticks()
                powerup = True

            collisions = pygame.sprite.spritecollide(flappy,obstacles,False)
            for obstacle in collisions:
                if type(obstacle) == Bean:
                    collision_count += 1
                    collision_sound.play()
                    if progress > 0:
                        progress-=0.05
                    if numObj(obstacles,Bean) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
                        
                else:  #Player hit an enemy now
                    damage_sound.play()
                    health -= 0.2
                    if health <= 0:
                        game_over_sound.play()
                        time.sleep(3)
                        game_active = False
                        flappy_died = True
                    if numObj(obstacles,Enemy) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
        #GAME ACTIVE AND POWER UP ACTIVE
        elif game_active and not game_paused and powerup:
            screen.blit(game_active_background,(0,0))
            player.draw(screen)
            player.update()
            for character in player:
                if character.game_over():
                    flappy_died = True
                    game_active = False
                    powerup = False

            obstacles.draw(screen)
            obstacles.update()
            
            screen.blit(dashboard_surface,(0,650))
            screen.blit(bean_surface, (150,660))

            display_hp((230,675), health)
            display_powerUp((530,675), progress)
            display_score2((100,675), collision_count)

            collisions = pygame.sprite.spritecollide(flappy,obstacles,False)
            for obstacle in collisions:
                if type(obstacle) == Bean:
                    collision_count += 1
                    collision_sound.play()   
                    if numObj(obstacles,Bean) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
                else:  #Player hit an enemy now
                    damage_sound.play()
                    health -= 0.2
                    if health == 0:
                        game_over_sound.play()
                        time.sleep(3)
                        game_active = False
                        flappy_died = True
                        powerup = False                
                    if numObj(obstacles,Enemy) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
            print(f"powerup start time: {start_time}")
            if elapsed_time(start_time) < power_up_duration:
                progress += 0.003
            if progress > 1:
                progress = 1
                B=1
                E=1
                print("power up ended")
                powerup = False
        # PAUSED
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
                main_menu()
        # RETRY SCREEN
        elif not game_active and flappy_died:
            print("going to retry menu")
            retry_menu(collision_count,player,obstacles)
        # TO MAIN MENU
        else:
            print("going back to main menu")
            main_menu()
        pygame.display.update()
        clock.tick(60) #won't run faster than 60 frames per second

def coopMode():
    p1_health = 1
    p2_health = 1
    p1_progress = 1
    p2_progress = 1
    p1_collision_count = 0
    p2_collision_count = 0

    game_active = True
    p1_died = False
    p2_died = False
    p1_powerup = False
    p2_powerup = False
    B = 1
    E = 1

    power_up_time=False
    power_up_duration=10
    start_time=None

    sprite_spawn = 900
    object_timer = pygame.USEREVENT +1
    pygame.time.set_timer(object_timer, sprite_spawn)
    object_speed_timer = pygame.USEREVENT +2
    pygame.time.set_timer(object_speed_timer,60000)

main_menu()
