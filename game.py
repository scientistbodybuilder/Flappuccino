import pygame
from sys import exit
import random
import time

RECT = pygame.Rect(637,0,6,650)
WIDTH = 1280
HEIGHT = 720
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

class Player1(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom = (320,360))
        self.gravity = 0
        self.player = "P1"
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
            if self.rect.colliderect(RECT):
                self.rect.right  = 637
            

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.top += self.gravity

    def game_over(self):
        if self.rect.top >= 900:
            return True

    def update(self):
        self.player_input()
        self.apply_gravity()

class Player2(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom = (960,360))
        self.gravity = 0
        self.player = "P2"
        # self.jump_sound = pygame.mixer.Sound('Assets/Sound/jump2.wav')
        # self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.gravity = -7
            #self.jump_sound.play()
            if self.rect.top < 0:
                self.rect.top = 0
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.colliderect(RECT):
                self.rect.left  = 643
        if keys[pygame.K_RIGHT]:
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
    def __init__(self, speed,min_x,max_x):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.3)
        self.min_x = min_x
        self.max_x = max_x
        self.x_pos = random.randint(self.min_x,self.max_x)
        self.y_pos = -10
        self.speed = speed
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))
        
    def movement(self):
        self.rect.y += self.speed
    def relocate(self):
            self.rect.y = -20
            self.rect.x = random.randint(self.min_x,self.max_x)
    def offscreen(self):
        if self.rect.y > 720:
            self.relocate()
    def collide(self):
        self.kill()

    def update(self):
        self.movement()
        self.offscreen()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,speed,min_x,max_x):
        super().__init__()
        self.min_x = min_x
        self.max_x = max_x
        self.x_pos = random.randint(self.min_x,self.max_x)
        self.y_pos = -10
        self.speed = speed
        self.image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Sugar1.xcf').convert_alpha(), 0.3)
        self.rect = self.image.get_rect(midbottom = (self.x_pos,self.y_pos))

    def movement(self):
        self.rect.y += self.speed

    def relocate(self):
            self.rect.y = -20
            self.rect.x = random.randint(self.min_x,self.max_x)
    def offscreen(self):
        if self.rect.y > 720:
            self.kill()
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

    def display(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

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

def display_hp(pos, rect1, rect2,font):  #UPDATED
    hp_surface = font.render("Health:",False,WHITE)
    hp_rect = hp_surface.get_rect(midtop=pos)
    screen.blit(hp_surface,hp_rect)

    pygame.draw.rect(screen, "red", rect1)
    pygame.draw.rect(screen, (9, 216, 39), rect2)

def display_powerUp(pos, rect1, rect2,font): #UPDATED
    power_up_surface = font.render("Power Up:",False,WHITE)
    power_up_rect = power_up_surface.get_rect(midtop=pos)
    screen.blit(power_up_surface,power_up_rect)

    pygame.draw.rect(screen, (177,123,71), rect1)
    pygame.draw.rect(screen, BLACK, rect2) # len is 200 in single, 150 in coop

def addBean(x, obstacles,speed,min,max):
    for i in range(x):
        obstacles.add(Bean(speed,min,max))
def addEnemy(x, obstacles,speed,min,max):
    for i in range(x):
        obstacles.add(Enemy(speed,min,max))
def elapsed_time(start_time):
    current_time = pygame.time.get_ticks()
    return (current_time - start_time)/1000
def numObj(obstacles,thing):
    count = [x for x in obstacles.sprites() if isinstance(x,thing)]
    return len(count)
def displaySeparator(rect):
    pygame.draw.rect(screen, BLACK, rect)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #main display surface
pygame.display.set_caption("Flappuccino")
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None,23)
large_font = pygame.font.Font(None,50)
arial = pygame.font.SysFont("arialblack",30)
comicsans = pygame.font.SysFont("comic_sans.ttf",30)
WHITE = (255,255,255)
GREY = (64,64,64)
BLACK = (0,0,0)

#LOAD ASSETS
#CHARACTERS
flappy_image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/flappy.xcf').convert_alpha(), 0.5)
flappy_char_select = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/flappy.xcf').convert_alpha(), 1.5)
char1 = {'display':flappy_char_select,'game_image':flappy_image}
messy_flappy_image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/messy_flappy.xcf').convert_alpha(), 0.5)
messy_flappy_char_select = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/messy_flappy.xcf').convert_alpha(), 1.5)
char2 = {'display':messy_flappy_char_select,'game_image':messy_flappy_image}
americano_image = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/americano.xcf').convert_alpha(), 0.6)
americano_char_select = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/americano.xcf').convert_alpha(), 1.6)
char3 = {'display':americano_char_select,'game_image':americano_image}

#BACKGROUNDS
game_active_background = pygame.image.load('Assets/Backgrounds/bkg1_1280x720.png').convert()
game_intro_background =  pygame.image.load('Assets/Backgrounds/titlepage_1280x720.png').convert()
pause_menu_packground = pygame.image.load('Assets/Backgrounds/pause_1280x720.png').convert()
game_over_background = pygame.image.load('Assets/Backgrounds/single_gameover_1280x720.png').convert()
coop_game_over_background = pygame.image.load('Assets/Backgrounds/coop_gameover_1280x720.png').convert()
character_selection = pygame.image.load('Assets/Backgrounds/Character Selection.png').convert()
#BUTTONS
quit_button_img = pygame.image.load('Assets/Buttons/Quit Button1.png').convert()
start_button_img = pygame.image.load('Assets/Buttons/start_button.xcf').convert_alpha()
right_character_selection_button = pygame.image.load('Assets/Buttons/CS_button.xcf').convert_alpha()
left_character_selection_button = pygame.transform.flip(right_character_selection_button,True,False)
resume_button_img = pygame.image.load('Assets/Buttons/Resume Button1.png').convert()
single_mode_button_img = pygame.image.load('Assets/Buttons/Single Mode.xcf').convert_alpha()
coop_mode_button_img = pygame.image.load('Assets/Buttons/Coop Mode.xcf').convert_alpha()
dashboard_surface = pygame.Surface((WIDTH,70))
dashboard_surface.fill((102, 64, 26))
bean_surface = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/Player_Sprite/Coffee_bean.xcf').convert_alpha(), 0.4)
#SOUNDS
collision_sound = pygame.mixer.Sound('Assets/Sound/collide_bean.mp3')
collision_sound.set_volume(0.15)
game_over_sound = pygame.mixer.Sound('Assets/Sound/player-lose.wav')
game_over_sound.set_volume(0.3)
damage_sound = pygame.mixer.Sound('Assets/Sound/collide_sugar.wav')
damage_sound.set_volume(0.5)
char_sel_sound = pygame.mixer.Sound('Assets/Sound/blip_click.mp3')
char_sel_sound.set_volume(0.3)
button_sound = pygame.mixer.Sound('Assets/Sound/button.mp3')
button_sound.set_volume(1)
pygame.mixer.music.load('Assets/Sound/house_party_bkg_music.mp3')
pygame.mixer.music.set_volume(0.3)

Controls_surface = font.render("Use 'w,a,d' to move and press ESC in game to pause",False,GREY)
controls_rect = Controls_surface.get_rect(midbottom = (640,600))
Coop_Controls_surface = font.render(f"Player 1 uses 'w,a,d' and Player 2 uses arrow keys for movement",False,GREY)
coop_controls_rect = Coop_Controls_surface.get_rect(midbottom = (640,600))
Back_surface = font.render("Press ESC to return home",False,GREY)
back_rect = Back_surface.get_rect(midbottom = (640,625))

clock = pygame.time.Clock()

def main_menu():
    pygame.mixer.music.play(-1,0.0)
    while True:
        screen.blit(game_intro_background,(0,0))
        single_player_button = Button(180,470,single_mode_button_img,1.3)
        two_player_button = Button(410,470,coop_mode_button_img,1.3)
        if single_player_button.draw():
            button_sound.play()
            singleCharSelect()
        if two_player_button.draw():
            button_sound.play()
            coopCharSelect()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)

def singleCharSelect():
    pygame.mixer.music.play(-1,0.0)
    chars = [char1,char2,char3]
    len_chars = len(chars)-1
    char_index = 0
    while True:
        screen.blit(character_selection,(0,0))
        screen.blit(Controls_surface,controls_rect)
        screen.blit(Back_surface,back_rect)
        rect = chars[char_index]['display'].get_rect(midbottom=(640,450))
        screen.blit(chars[char_index]['display'],rect)
        right_arrow_button = Button(800,480,right_character_selection_button,1.5)
        left_arrow_button = Button(480,480,left_character_selection_button,1.5)
        if char_index == 0: # first character selected
            right_arrow_button.display()   
        elif char_index == len_chars: # last character selected
            left_arrow_button.display()
        else: # middle character
            right_arrow_button.display()
            left_arrow_button.display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if right_arrow_button.rect.collidepoint(pos):
                    char_index+=1
                    char_sel_sound.play()
                elif left_arrow_button.rect.collidepoint(pos):
                    char_index -=1
                    char_sel_sound.play()
        start_btn = Button(640,515,start_button_img,1.5)
        if start_btn.draw():
            button_sound.play()
            singleMode(chars[char_index]['game_image'])
        
        pygame.display.update()
        clock.tick(60)

def coopCharSelect():
    pygame.mixer.music.play(-1,0.0)
    chars = [char1,char2,char3]
    len_chars = len(chars)-1
    p1_char_index = 0
    p2_char_index = 0
    while True:
        screen.blit(character_selection,(0,0))
        screen.blit(Coop_Controls_surface,coop_controls_rect)
        screen.blit(Back_surface,back_rect)
        #display characters
        p1_rect = chars[p1_char_index]['display'].get_rect(midbottom=(430,450))
        screen.blit(chars[p1_char_index]['display'],p1_rect)
        p2_rect = chars[p2_char_index]['display'].get_rect(midbottom=(850,450))
        screen.blit(chars[p2_char_index]['display'],p2_rect)
        p1_right_arrow_button = Button(575,490,right_character_selection_button,1.2)
        p1_left_arrow_button = Button(285,490,left_character_selection_button,1.2)
        p2_right_arrow_button = Button(1000,490,right_character_selection_button,1.2)
        p2_left_arrow_button = Button(700,490,left_character_selection_button,1.2)
        #player 1 select buttons
        if p1_char_index == 0: # first character selected
            p1_right_arrow_button.display()
        if p1_char_index == len_chars: # last character selected
            p1_left_arrow_button.display()
        if p1_char_index > 0 and p1_char_index < len_chars: # middle character
            p1_right_arrow_button.display()
            p1_left_arrow_button.display()

        #player 2 select buttons
        if p2_char_index == 0: # first character selected
            p2_right_arrow_button.display()
        if p2_char_index == len_chars: # last character selected
            p2_left_arrow_button.display()
        if p2_char_index > 0 and p2_char_index < len_chars: # middle character
            p2_right_arrow_button.display()
            p2_left_arrow_button.display()

        start_btn = Button(640,560,start_button_img,1.5)
        if start_btn.draw():
            button_sound.play()
            coopMode(chars[p1_char_index]['game_image'],chars[p2_char_index]['game_image'])
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if p1_right_arrow_button.rect.collidepoint(pos):
                        p1_char_index+=1
                        char_sel_sound.play()
                    elif p1_left_arrow_button.rect.collidepoint(pos):
                        p1_char_index -=1
                        char_sel_sound.play()
                    elif p2_left_arrow_button.rect.collidepoint(pos):
                        p2_char_index -=1
                        char_sel_sound.play()
                    elif p2_right_arrow_button.rect.collidepoint(pos):
                        p2_char_index +=1
                        char_sel_sound.play()
                    
        pygame.display.update()
        clock.tick(60)

def retry_menu(collision_count,player,obstacles,image):
    pygame.mixer.music.play(-1,0.0)
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
                singleMode(image)
        pygame.display.update()
        clock.tick(60)

def coop_retry_menu(p1_score,p2_score,players,p1_obstacles,p2_obstacles,p1_image,p2_image):
    pygame.mixer.music.play(-1,0.0)
    while True:
        screen.blit(coop_game_over_background,(0,0))
        p1_score_surface = large_font.render(f'Player 1 Score: {p1_score}',False,WHITE)
        p1_score_rect = p1_score_surface.get_rect(topleft = (170,200))
        p2_score_surface = large_font.render(f'Player 2 Score: {p2_score}',False,WHITE)
        p2_score_rect = p2_score_surface.get_rect(topleft = (170,240))

        retry_surface = font.render(f'Press R to retry',False,WHITE)
        retry_rect = retry_surface.get_rect(midbottom = (300,350))
        home_surface = font.render(f'Press SPACE to return home',False,WHITE)
        home_rect = home_surface.get_rect(midbottom = (300,400))

        screen.blit(retry_surface,retry_rect)
        screen.blit(p1_score_surface,p1_score_rect)
        screen.blit(p2_score_surface,p2_score_rect)
        screen.blit(home_surface,home_rect)

        #Reset the player back to the starting position
        for character in players:
            character.rect.midbottom = (640,360)
            character.gravity = 0
        p1_obstacles.empty()
        p2_obstacles.empty()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_menu()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                coopMode(p1_image,p2_image)
        pygame.display.update()
        clock.tick(60)
#GAME MODES
def singleMode(image):
    pygame.mixer.music.play(-1,0.0)
    #initialize parameters
    health = 1
    progress = 1
    collision_count = 0
    min_x = 1
    max_x = 1280

    hp_red = pygame.Rect(272,667,200,35)
    powerup_black = pygame.Rect(585,667,200,35)

    game_active = True
    game_paused = False
    flappy_died = False
    powerup = False
    B = 1
    E = 1
    BAR_LEN = 200
    speed = 2
    # power_up_time=False
    power_up_duration=10
    start_time=None

    sprite_spawn = 900
    object_timer = pygame.USEREVENT +1
    pygame.time.set_timer(object_timer, sprite_spawn)
    object_speed_timer = pygame.USEREVENT +2
    pygame.time.set_timer(object_speed_timer,60000)

    #Groups
    obstacles = pygame.sprite.Group()

    flappy = Player(image)
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
                        print(f"adding {B} beans and {E} sugars")
                        addBean(B, obstacles,speed,min_x,max_x)
                        addEnemy(E, obstacles,speed,min_x,max_x)
                    if event.type == object_speed_timer: #find a way to sleep creating new objects, so the old ones are off the screen before increasing timer
                        speed +=0.05
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
                        retry_menu(collision_count,player,obstacles,image)

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

            hp_green = pygame.Rect(272,667,BAR_LEN*health,35)
            display_hp((230,675), hp_red,hp_green,font)
            powerup_brown = pygame.Rect(585,667,BAR_LEN*progress,35)
            display_powerUp((530,675), powerup_black,powerup_brown,font)
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
                        progress-=0.02
                    if numObj(obstacles,Bean) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
                        
                else:  #Player hit an enemy now
                    damage_sound.play()
                    health -= 0.2
                    if health < 0.1:
                        game_over_sound.play()
                        time.sleep(3)
                        game_active = False
                        flappy_died = True  
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

            hp_green = pygame.Rect(272,667,BAR_LEN*health,35)
            display_hp((230,675), hp_red,hp_green,font)
            powerup_brown = pygame.Rect(585,667,BAR_LEN*progress,35)
            display_powerUp((530,675), powerup_black,powerup_brown,font)
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
                    if health < 0.1:
                        game_over_sound.play()
                        time.sleep(3)
                        game_active = False
                        flappy_died = True
                        powerup = False                
                    obstacle.kill()
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
            retry_menu(collision_count,player,obstacles,image)
        # TO MAIN MENU
        else:
            main_menu()
        pygame.display.update()
        clock.tick(60) #won't run faster than 60 frames per second

def coopMode(p1_image,p2_image):
    pygame.mixer.music.play(-1,0.0)
    game_active = True
    BAR_LEN = 150
    speed = 2
    p1_min_x = 1
    p1_max_x = 630
    p2_min_x = 650
    p2_max_x = 1280

    # power_up_time=False
    power_up_duration=10
    
    object_speed_timer = pygame.USEREVENT +2
    pygame.time.set_timer(object_speed_timer,60000)
    players = pygame.sprite.Group()

    #PLAYER 1
    p1_bean_rate = 1
    p1_enemy_rate = 1
    p1_health = 1
    p1_progress = 1
    p1_collision_count = 0
    p1_died = False
    p1_powerup = False
    p1_start_time=None

    p1_hp_red = pygame.Rect((200,680,BAR_LEN,27))
    p1_powerup_black = pygame.Rect(400,680,BAR_LEN,27)

    p1_sprite_spawn = 900
    p1_object_timer = pygame.USEREVENT +1
    pygame.time.set_timer(p1_object_timer, p1_sprite_spawn)

    p1_obstacles = pygame.sprite.Group()
    p1 = Player1(p1_image)
    players.add(p1)

    #PLAYER 2
    p2_bean_rate = 1
    p2_enemy_rate = 1
    p2_health = 1
    p2_progress = 1
    p2_collision_count = 0
    p2_died = False
    p2_powerup = False
    p2_start_time = None

    p2_hp_red = pygame.Rect((800,680,BAR_LEN,27))
    p2_powerup_black = pygame.Rect(1000,680,BAR_LEN,27)

    p2_sprite_spawn = 900
    p2_object_timer = pygame.USEREVENT +1
    pygame.time.set_timer(p2_object_timer, p2_sprite_spawn)

    p2_obstacles = pygame.sprite.Group()
    p2 = Player2(p2_image)
    players.add(p2)

    while True: # lets our code keep running forever epic. we break if the game ends
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         game_paused = True
                if event.type == p1_object_timer:
                    #check whether we enough enough objects in the group already
                    if len(p1_obstacles.sprites()) < 15:
                        addBean(p1_bean_rate, p1_obstacles,speed,p1_min_x,p1_max_x)
                        addEnemy(p1_enemy_rate, p1_obstacles,speed,p1_min_x,p1_max_x)
                if event.type == p2_object_timer:
                    #check whether we enough enough objects in the group already
                    if len(p2_obstacles.sprites()) < 15:
                        addBean(p2_bean_rate, p2_obstacles,speed,p2_min_x,p2_max_x)
                        addEnemy(p2_enemy_rate, p2_obstacles,speed,p2_min_x,p2_max_x)
                if event.type == object_speed_timer: #find a way to sleep creating new objects, so the old ones are off the screen before increasing timer
                    speed +=0.05
            else:
                if p1_died or p2_died:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        main_menu()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        coop_retry_menu(p1_collision_count,p2_collision_count,list(players),p1_obstacles,p2_obstacles,p1_image,p2_image)
        # GAME ACTIVE AND POWER UP NOT ACTIVE           
        if game_active: 
            screen.blit(game_active_background,(0,0))
            players.draw(screen)
            players.update()
            for character in players:
                if character.game_over():
                    game_active = False
                    if character.player == "P1":
                        p1_died = True
                    else:
                        p2_died = True

            p1_obstacles.draw(screen)
            p1_obstacles.update()
            p2_obstacles.draw(screen)
            p2_obstacles.update()
            
            screen.blit(dashboard_surface,(0,650))
            screen.blit(bean_surface, (120,660))  # bean icon for p1
            screen.blit(bean_surface, (745,660)) # bean icon for p2

            displaySeparator(RECT)  # separator

            p1_hp_green = pygame.Rect(200,680,BAR_LEN*p1_health,27)
            display_hp((227,660), p1_hp_red, p1_hp_green,small_font)
            p1_powerup_brown = pygame.Rect(400,680,BAR_LEN*p1_powerup,27)
            display_powerUp((441,660), p1_powerup_black, p1_powerup_brown,small_font)
            display_score2((55,675), p1_collision_count)

            p2_hp_green = pygame.Rect(800,680,BAR_LEN*p2_health,27)
            display_hp((827,660), p2_hp_red, p2_hp_green,small_font)
            p2_powerup_brown = pygame.Rect(1000,680,BAR_LEN*p2_powerup,27)
            display_powerUp((1041,660), p2_powerup_black, p2_powerup_brown,small_font)
            display_score2((700,675), p2_collision_count)

            if p1_progress < 0 and not p1_powerup:
                p1_bean_rate=5
                p1_enemy_rate=0
                print("p1 power up started")
                p1_start_time = pygame.time.get_ticks()
                p1_powerup = True
            if p2_progress < 0 and not p2_powerup:
                p2_bean_rate=5
                p2_enemy_rate=0
                print("p2 power up started")
                p2_start_time = pygame.time.get_ticks()
                p2_powerup = True

            p1_collisions = pygame.sprite.spritecollide(p1,p1_obstacles,False)
            for obstacle in p1_collisions:
                if type(obstacle) == Bean:
                    p1_collision_count += 1
                    collision_sound.play()
                    # if p1_progress > 0:
                    #     p1_progress-=0.05
                    if numObj(p1_obstacles,Bean) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
                    if not p1_powerup:
                        p1_progress-=0.02
                    if p1_powerup:
                        if elapsed_time(p1_start_time) < power_up_duration:
                            p1_progress += 0.003
                            if p1_progress > 1:
                                p1_progress = 1
                                p1_bean_rate=1
                                p1_enemy_rate=1
                                print("p1 power up ended")
                                p1_powerup = False             
                else:  #Player hit an enemy now
                    damage_sound.play()
                    p1_health -= 0.2
                    if p1_health < 0.1:
                        game_over_sound.play()
                        time.sleep(3)
                        game_active = False
                        p1_died = True
                    obstacle.kill()

            p2_collisions = pygame.sprite.spritecollide(p2,p2_obstacles,False)
            for obstacle in p2_collisions:
                if type(obstacle) == Bean:
                    p2_collision_count += 1
                    collision_sound.play()
                    # if p2_progress > 0:
                    #     p2_progress-=0.05
                    if numObj(p1_obstacles,Bean) < 7:
                        obstacle.relocate()
                    else:
                        obstacle.kill()
                    if not p2_powerup:
                        p2_progress-=0.02
                    if p2_powerup:
                        if elapsed_time(p2_start_time) < power_up_duration:
                            p2_progress += 0.003
                            if p2_progress > 1:
                                p2_progress = 1
                                p2_bean_rate=1
                                p2_enemy_rate=1
                                print("p2 power up ended")
                                p2_powerup = False                
                else:  #Player hit an enemy now
                    damage_sound.play()
                    p2_health -= 0.2
                    if p2_health < 0.1:
                        game_over_sound.play()
                        time.sleep(3)
                        game_active = False
                        p2_died = True
                    obstacle.kill()
        # RETRY SCREEN
        elif not game_active and (p1_died or p2_died):
            coop_retry_menu(p1_collision_count,p2_collision_count,list(players),p1_obstacles,p2_obstacles,p1_image,p2_image)
        # TO MAIN MENU
        else:
            main_menu()
        pygame.display.update()
        clock.tick(60) #won't run faster than 60 frames per second

# main_menu()
main_menu()
