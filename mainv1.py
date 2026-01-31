import pygame
import sys
import os
import math
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("BOT")

# UI
bounce_time = 0
bounce_speed = 1
bounce_amplitude = 20
GRID_SIZE = 40
GRID_SPEED = 1
grid_offset_x = 0
grid_offset_y = 0
grid_time = 0
CB = (203, 203, 203)
WHITE = (255, 255, 255)
WHITE2 = (255, 255, 227)
BLACK = (20, 20, 25)
BLACK2 = (74, 74, 74)
GREEN = (40, 255, 40)
RED = (255, 40, 40)
GRAY = (100, 105, 110)
METAL = (50, 55, 60)
GOLD = (255, 215, 0)
DEEP_BLUE = (20, 25, 30)
CRATE_COLOR = (139, 69, 19)


# Variables

FPS = 60
VEL = 1
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
P_WIDTH, P_HEIGHT = 60, 70
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


# Image Import/Adjustment
BG = pygame.image.load(os.path.join('Assets', 'bg.png'))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
PLAYER1_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'PLAYERS', 'P1.png'))
PLAYER1_TANK = pygame.transform.rotate(pygame.transform.scale(PLAYER1_TANK_IMAGE, (P_WIDTH, P_WIDTH)), 0)
PLAYER2_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'PLAYERS', 'P2.png'))
PLAYER2_TANK =pygame.transform.rotate(pygame.transform.scale(PLAYER2_TANK_IMAGE, (P_WIDTH, P_HEIGHT)), 0)
BOT_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'PLAYERS', 'BOT.png'))



# Fonts
ftitle = pygame.font.Font(os.path.join('Assets', 'title.ttf'), 80)
bfont = pygame.font.Font(os.path.join('Assets', 'font2.otf'), 30)
font_main_title = pygame.font.SysFont("Impact", 80)
font_hud =pygame.font.SysFont("Impact", 28)
font_victory = pygame.font.SysFont("Impact", 70)



def draw_moving_grid(surface, offset_x, offset_y, grid_size=GRID_SIZE):
    # Draws a vertical lines!
    for x in range(-grid_size, WIDTH + grid_size, grid_size):
        pygame.draw.line(surface, CB,
                        (x + offset_x, 0),
                        (x + offset_x, 700), 1)
        
    # Draws horizontal lines!
    for y in range(-grid_size, 700 + grid_size, grid_size):
        pygame.draw.line(surface, CB,
                        (0, y + offset_y),
                        (1200, y + offset_y), 1)




def draw_hud(P1 , P2, bot):
    pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, 80))
    title = font_hud.render("PLAYER 1 VS PLAYER 2", 1, WHITE)

class Button:
    def __init__(self, text, x_pos, y_pos, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.draw()
        
    def draw(self):
        button_text = bfont.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (200, 100))
        if self.enabled:
            if self.check_click():
                pygame.draw.rect(WIN, DEEP_BLUE, button_rect, 0, 20)
            else:
                pygame.draw.rect(WIN, CB, button_rect, 0, 20)
        else:
            pygame.draw.rect(WIN, METAL, button_rect, 3, 22)
        text_rect = button_text.get_rect(center=button_rect.center)
        WIN.blit(button_text, text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (200, 100))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            print("Clicked")
            return True
        else:
            print('Clicked')
            return False





def Menu():

    global grid_offset_x, grid_offset_y, grid_time, bounce_time

    clock = pygame.time.Clock()
    run = True
    while run:

        grid_offset_x = (grid_offset_x + GRID_SPEED * 1) % GRID_SIZE
        grid_offset_y = (grid_offset_y + GRID_SPEED * 1) % GRID_SIZE

        WIN.fill((DEEP_BLUE))
        draw_moving_grid(WIN, grid_offset_x, grid_offset_y)

        bg_with_alpha = BG.copy()
        bg_with_alpha.set_alpha(150)
        WIN.blit(bg_with_alpha, (0, 0))
        bounce_time += 1
        bounce_offset = math.sin(bounce_time * 0.05 * bounce_speed) * bounce_amplitude
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        T1 = ftitle.render("BATTLE OF TANKS", True, GRAY)
        T1_RECT = T1.get_rect(center=(600, 100))
        T2 = ftitle.render("BATTLE OF TANKS", True, WHITE2)
        T2_RECT = T2.get_rect(center=(600, 104 + bounce_offset * 0.3))
        
        P1 = pygame.transform.scale(PLAYER1_TANK_IMAGE, (250, 250))
        P2 =pygame.transform.scale(PLAYER2_TANK_IMAGE, (250, 250))



        play_button = Button('PLAY', 500, 300, True)
        quit_button = Button('QUIT', 500, 450, True)

        WIN.blit(P1, (925, 400 + bounce_offset))
        WIN.blit(P2, (25, 400 - bounce_offset))
        WIN.blit(T1, T1_RECT)
        WIN.blit(T2, T2_RECT)

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        

        pygame.display.update()
if __name__ == "__main__":
    Menu()