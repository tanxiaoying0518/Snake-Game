import random

import pygame

SCREEN_SIZE=(1000,800)
WHITE=(255,255,255)

CELL_RADIUS=20
SNAKE_COLOR=(0,0,0)
FOOD_RADIUS=20

UPDATE=pygame.USEREVENT+1
FOOD=pygame.USEREVENT+2

LIGHT_GREY=(100,100,100)
MSG_POSITION=(180,350)

cell_diameter=CELL_RADIUS*2
max_cell_x=SCREEN_SIZE[0]//cell_diameter
max_cell_y=SCREEN_SIZE[1]//cell_diameter


def init_game():
    pygame.init()
    pygame.display.set_caption("Snake Game")
    pygame.time.set_timer(UPDATE, 300)
    pygame.time.set_timer(FOOD, 2000)
    
    


class Game:
    def __init__(self):
        self.running = True
        self.quit_requested = False
        self.screen_mode = "home"
        self.settings_choice = None
        self.speed = 300
        self.food_color = (200, 0, 0)
        self.win_length = 10
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.snake = Snake()
        self.food = None
        self.message = None



def draw_homescreen():
    game.screen.fill(WHITE)
    font = pygame.font.Font(None, 40)
    title = font.render("SNAKE GAME", True, (0, 0, 0))
    game.screen.blit(title, (380, 250))

    font = pygame.font.Font(None, 30)
    game.screen.blit(font.render("Press S for Settings", True, LIGHT_GREY), (380, 330))
    game.screen.blit(font.render("Press any other key to Start", True, LIGHT_GREY), (330, 370))



def draw_settings():
    game.screen.fill(WHITE)
    font = pygame.font.Font(None, 40)
    game.screen.blit(font.render("SETTINGS", True, (0, 0, 0)), (420, 220))

    font = pygame.font.Font(None, 30)
    game.screen.blit(font.render("Press 1 for food color", True, LIGHT_GREY), (330, 300))
    game.screen.blit(font.render("Press 2 for speed", True, LIGHT_GREY), (330, 340))
    game.screen.blit(font.render("Press 3 for winning condition", True, LIGHT_GREY), (330, 380))
    game.screen.blit(font.render("Press ESC to return home", True, LIGHT_GREY), (330, 420))

    if game.settings_choice == "color":
        game.screen.blit(font.render("r = Red, g = Green, b = Blue", True, LIGHT_GREY), (330, 470))
    elif game.settings_choice == "speed":
        game.screen.blit(font.render("s = Slow, m = Medium, f = Fast", True, LIGHT_GREY), (330, 470))
    elif game.settings_choice == "win_condition":
        game.screen.blit(font.render("Press a to win by reaching length of 10", True, LIGHT_GREY), (330, 470))
        game.screen.blit(font.render("Press b to win by reaching length of 20", True, LIGHT_GREY), (330, 510))
        game.screen.blit(font.render("Press c to win by fill up the screen", True, LIGHT_GREY), (330, 550))

        


def handle_menu_key(key):
    if game.screen_mode == "home":
        if key == pygame.K_s:
            game.screen_mode = "settings"
            game.settings_choice = None
        else:
            game.snake = Snake()
            game.food = None
            game.screen_mode = "game"
            pygame.time.set_timer(UPDATE, game.speed)
    elif game.screen_mode == "settings":
        if key == pygame.K_ESCAPE:
            game.screen_mode = "home"
            game.settings_choice = None
        elif key == pygame.K_1:
            game.settings_choice = "color"
        elif key == pygame.K_2:
            game.settings_choice = "speed"
        elif key == pygame.K_3:
            game.settings_choice = "win_condition"
        elif game.settings_choice == "color" and key in (pygame.K_r, pygame.K_g, pygame.K_b):
            if key == pygame.K_r:
                game.food_color = (200, 0, 0)
            elif key == pygame.K_g:
                game.food_color = (0, 200, 0)
            else:
                game.food_color = (0, 0, 200)
        elif game.settings_choice == "speed":
            if key == pygame.K_s:
                game.speed = 500
            elif key == pygame.K_m:
                game.speed = 300
            elif key == pygame.K_f:
                game.speed = 150
        elif game.settings_choice == "win_condition":
            if key == pygame.K_a:
                game.win_length = 10
            elif key == pygame.K_b:
                game.win_length = 20
            elif key == pygame.K_c:
                game.win_length = max_cell_x*max_cell_y
            pygame.time.set_timer(UPDATE, game.speed)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_tuple(self):
        return (self.x, self.y)
    def copy(self):
        return Cell(self.x, self.y)
    def update(self, direction):
        if direction=="U":
            self.y-=CELL_RADIUS*2
        elif direction=="D":
            self.y+=CELL_RADIUS*2  
        elif direction=="L":
            self.x-=CELL_RADIUS*2
        elif direction=="R":
            self.x+=CELL_RADIUS*2
class Snake:
    def __init__(self):
        cell_diameter=CELL_RADIUS*2
        x=(SCREEN_SIZE[0]/cell_diameter//2)*cell_diameter
        y=(SCREEN_SIZE[1]/cell_diameter//2)*cell_diameter
        self.body=[Cell(x, y)]
        self.cell_size=CELL_RADIUS
        self.color=SNAKE_COLOR
        self.direction="L"

    def update(self):
        head=self.body[0].copy()
        self.body.pop()
        head.update(self.direction)
        self.body.insert(0, head)

def is_snake_food_collide():
    head=game.snake.body[0].copy()
    head.update(game.snake.direction)
    return game.food.x==head.x and game.food.y==head.y

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            game.quit_requested = True
        elif event.type == pygame.KEYDOWN and game.screen_mode != "game":
            handle_menu_key(event.key)
        elif game.screen_mode == "game":
            if event.type == UPDATE:
                game.snake.update()
            elif event.type == FOOD:
                generate_food()

    if game.screen_mode == "game" and game.running:
        check_snake_dir()
        check_food()
        check_head_body_collision()
        check_out_boudary()
        check_win()

def check_win():
    length=len(game.snake.body)
    cell_diameter=CELL_RADIUS*2
    if length==game.win_length:
        game.running=False
        game.message="You WIN! Should restart the game? y/n"

def check_out_boudary():
    cell_diameter=CELL_RADIUS*2
    out_boundary_x_cells=[cell for cell in game.snake.body if  cell.x<cell_diameter or cell.x>SCREEN_SIZE[0]-cell_diameter]
    out_boundary_y_cells=[cell for cell in game.snake.body if  cell.y<cell_diameter or cell.y>SCREEN_SIZE[1]-cell_diameter]
    if len(out_boundary_x_cells)>0 or len(out_boundary_y_cells)>0:
        game.running=False
        game.message="Game Over! Snake out of boundary! Should restart the game? y/n"

def check_head_body_collision():
    head=game.snake.body[0]
    body=game.snake.body
    try:
        index=[cell.to_tuple() for cell in body[1:]].index(head.to_tuple())
    except ValueError:
        index=-1
    if len(game.snake.body)>1 and index>-1:
        game.snake.body=game.snake.body[:index]

def check_food():
    if game.food is not None and is_snake_food_collide():
        cell=Cell(game.food.x, game.food.y)
        game.snake.body.insert(0, cell)
        game.food=None
            


def check_snake_dir():
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP] and not game.snake.direction=="D":
        game.snake.direction="U"
    elif pressed_keys[pygame.K_DOWN] and not game.snake.direction=="U":
        game.snake.direction="D"
    elif pressed_keys[pygame.K_LEFT] and not game.snake.direction=="R":
        game.snake.direction="L"
    elif pressed_keys[pygame.K_RIGHT] and not game.snake.direction=="L":
        game.snake.direction="R"

def generate_food():
    while game.food is None:
        cell_diameter=CELL_RADIUS*2
        rand_x=random.randint(1, SCREEN_SIZE[0]//cell_diameter-1)*cell_diameter
        rand_y=random.randint(1, SCREEN_SIZE[1]//cell_diameter-1)*cell_diameter
        if (rand_x,rand_y) not in [cell.to_tuple() for cell in game.snake.body]:
            game.food=Cell(rand_x, rand_y)
    

def draw():
    if game.screen_mode == "home":
        draw_homescreen()
    elif game.screen_mode == "settings":
        draw_settings()
    else:
        game.screen.fill(WHITE)
        if game.running:
            draw_snake()
            draw_food()
        else:
            draw_restart()
    pygame.display.flip()

def draw_restart():
    font = pygame.font.Font(None, 30)
    restart_msg=font.render(game.message, True, LIGHT_GREY)
    game.screen.blit(restart_msg, MSG_POSITION)

def draw_food():
    if game.food is not None:
        pygame.draw.circle(game.screen, game.food_color, game.food.to_tuple(), FOOD_RADIUS)

def draw_snake():
    for cell in game.snake.body:
        pygame.draw.circle(game.screen, game.snake.color, cell.to_tuple(), game.snake.cell_size)

def check_restart():
    while not game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_requested = True
                return
            if event.type == pygame.KEYDOWN and event.key==pygame.K_y:
                game.snake=Snake()
                game.running=True
                game.message=None
                return
            if event.type == pygame.KEYDOWN and event.key==pygame.K_n:
                game.quit_requested=True
                return
        
            
                
                

if __name__ == "__main__":
    init_game()
    game = Game()
    while not game.quit_requested:
        update()
        draw()
        check_restart()
                

                
    pygame.quit()