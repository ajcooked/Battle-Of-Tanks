import pygame
import sys
import math

pygame.init()
SCREEN = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Battle of Tanks")
BG = pygame.image.load("assets/bg.png")

# Bounce parameters
bounce_time = 0
bounce_speed = 2.0
bounce_amplitude = 20

# Grid parameters
GRID_SIZE = 40
GRID_SPEED = 2
GRID_COLOR = ("green")
grid_offset_x = 0
grid_offset_y = 0
grid_time = 0

def draw_moving_grid(surface, offset_x, offset_y, grid_size=GRID_SIZE):
    """Draws an animated grid in the background"""
    # Draw vertical lines
    for x in range(-grid_size, 1200 + grid_size, grid_size):
        pygame.draw.line(surface, GRID_COLOR,
                        (x + offset_x, 0), 
                        (x + offset_x, 700), 1)
    
    # Draw horizontal lines
    for y in range(-grid_size, 700 + grid_size, grid_size):
        pygame.draw.line(surface, GRID_COLOR, 
                        (0, y + offset_y), 
                        (1200, y + offset_y), 1)

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, scale=1.0):
        if scale != 1.0 and image is not None:
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        else:
            self.image = image
            
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.image is None:
            self.image = self.text
            
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.scale = scale

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

icon = pygame.image.load("assets/PLAYERS/p1.png")
pygame.display.set_icon(icon)

def get_font(size):
    return pygame.font.Font("Assets/font.ttf", size)

def AI():
    pygame.display.set_caption("AI Mode")

    global grid_offset_x, grid_offset_y, grid_time
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(("darkgreen"))

        grid_offset_x = (grid_offset_x + GRID_SPEED * 1) % GRID_SIZE
        grid_offset_y = (grid_offset_y + GRID_SPEED * 1) % GRID_SIZE
        
        draw_moving_grid(SCREEN, grid_offset_x, grid_offset_y)
        
        bg_with_alpha = BG.copy()
        bg_with_alpha.set_alpha(150)  
        SCREEN.blit(bg_with_alpha, (1200, 700))

        AI_TEXT = get_font(80).render("This is the VS. AI screen.", True, "White")
        AI_RECT = AI_TEXT.get_rect(center=(600, 250))
        SCREEN.blit(AI_TEXT, AI_RECT)
    
        AI_BACK = Button(image=None, pos=(600, 500), 
                        text_input="BACK", font=get_font(75), base_color="White", hovering_color="Red")
        AI_BACK.changeColor(PLAY_MOUSE_POS)
        AI_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AI_BACK.checkForInput(PLAY_MOUSE_POS):
                    play_menu()
        
        pygame.display.update()

def PLAYER():
    pygame.display.set_caption("2 Player Mode")

    global grid_offset_x, grid_offset_y, grid_time
    
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(("darkblue"))

        grid_offset_x = (grid_offset_x + GRID_SPEED * 1) % GRID_SIZE
        grid_offset_y = (grid_offset_y + GRID_SPEED * 1) % GRID_SIZE
        
        draw_moving_grid(SCREEN, grid_offset_x, grid_offset_y)
        
        bg_with_alpha = BG.copy()
        bg_with_alpha.set_alpha(150)  
        SCREEN.blit(bg_with_alpha, (1200, 700))

        PLAYER_TEXT = get_font(80).render("This is the 2 PLAYER screen.", True, "White")
        PLAYER_RECT = PLAYER_TEXT.get_rect(center=(600, 250))
        SCREEN.blit(PLAYER_TEXT, PLAYER_RECT)
        
        PLAYER_BACK = Button(image=None, pos=(600, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Red")
        PLAYER_BACK.changeColor(OPTIONS_MOUSE_POS)
        PLAYER_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAYER_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    play_menu()
        
        pygame.display.update()

def play_menu():
    pygame.display.set_caption("Battle of Tanks")
    
    global grid_offset_x, grid_offset_y, grid_time
    global bounce_time

    while True:

        grid_offset_x = (grid_offset_x + GRID_SPEED * 1) % GRID_SIZE
        grid_offset_y = (grid_offset_y + GRID_SPEED * 1) % GRID_SIZE
        
        SCREEN.fill((15, 20, 30))
        draw_moving_grid(SCREEN, grid_offset_x, grid_offset_y)
        
        bg_with_alpha = BG.copy()
        bg_with_alpha.set_alpha(150)  
        SCREEN.blit(bg_with_alpha, (1200, 700))

        bounce_time += 1
        
        bounce_offset = math.sin(bounce_time * 0.05 * bounce_speed) * bounce_amplitude
        title_bounce = 100 + bounce_offset * 0.3
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TANK = pygame.image.load("assets/PLAYERS/p1.png")
        TANK = pygame.transform.scale(TANK, (250, 250))
        TANK2 = pygame.image.load("assets/PLAYERS/p2.png")
        TANK2 = pygame.transform.scale(TANK2, (250, 250))

        MENU_TEXT = get_font(100).render("BATTLE OF TANKS", True, "#F9F9F9")
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 5 + title_bounce))

        MENU_TEXT2 = get_font(102).render("BATTLE OF TANKS", True, "#0B5E00")
        MENU_RECT2 = MENU_TEXT2.get_rect(center=(600, 6 + title_bounce + 4))

        MENU_TEXT3 = get_font(80).render("SELECT MODE", True, "#E5FF00")
        MENU_RECT3 = MENU_TEXT3.get_rect(center=(600, 450 + title_bounce + 4))


        AI_image = pygame.image.load("assets/PLAYERS/BOT.png").convert_alpha() 
        AI_BUTTON = Button(image=AI_image, pos=(600, 420),  
            text_input="[2] VS. BOT", font=get_font(70), base_color="White", hovering_color="Green", scale=0.650)
        PLAYER_image = pygame.image.load("assets/PLAYERS/p2.png").convert_alpha() 
        PLAYER_BUTTON = Button(image=PLAYER_image, pos=(600, 300), 
            text_input="[1] 2 PLAYER", font=get_font(70), base_color="White", hovering_color="Green", scale=0.750)

        SCREEN.blit(TANK, (925, 400 + bounce_offset))
        SCREEN.blit(TANK2, (25, 400 - bounce_offset))
        SCREEN.blit(MENU_TEXT3, MENU_RECT3)
        SCREEN.blit(MENU_TEXT2, MENU_RECT2)
        SCREEN.blit(MENU_TEXT, MENU_RECT)
    

        for button in [AI_BUTTON, PLAYER_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    AI()
                if PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAYER()

        pygame.display.update()

if __name__ == "__main__":
    play_menu()