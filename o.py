import pygame
import sys

pygame.init()

SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("BATTLE OF TANKS")

BG = pygame.image.load("assets/bg.jpg")
BG = pygame.transform.scale(BG, (1280, 700))

# Grid parameters
GRID_SIZE = 40
GRID_SPEED = 2
GRID_COLOR = ("BLACK")
grid_offset_x = 0
grid_offset_y = 0
grid_time = 0


def draw_moving_grid(surface, offset_x, offset_y, grid_size=GRID_SIZE):
    """Draws an animated grid in the background"""
    # Draw vertical lines
    for x in range(-grid_size, 1200 + grid_size, grid_size):
        pygame.draw.line(surface, GRID_COLOR,
                        (x + offset_x, 0),
                        (x + offset_x, 700), 1)  # Fixed: Changed offset_y to offset_x for x coordinate

    # Draw horizontal lines
    for y in range(-grid_size, 700 + grid_size, grid_size):
        pygame.draw.line(surface, GRID_COLOR,
                        (0, y + offset_y),
                        (1200, y + offset_y), 1)


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")

        play_text = get_font(45).render("This is the PLAY screen.", True, "White")
        play_rect = play_text.get_rect(center=(640, 260))
        SCREEN.blit(play_text, play_rect)

        play_back = Button(image=None, pos=(640, 460),
                        text_input="BACK MENU", font=get_font(75), base_color="White", hovering_color="Green")

        play_back.changeColor(play_mouse_pos)
        play_back.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.checkForInput(play_mouse_pos):
                    main_menu()

        pygame.display.update()


class Button:

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
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

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                        self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                        self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def main_menu():
    global grid_offset_x, grid_offset_y, grid_time
    while True:
        # Update grid offsets for animation
        grid_offset_x = (grid_offset_x + GRID_SPEED * 1) % GRID_SIZE
        grid_offset_y = (grid_offset_y + GRID_SPEED * 1) % GRID_SIZE

        SCREEN.blit(BG, (0, 0,))
        draw_moving_grid(SCREEN, grid_offset_x, grid_offset_y)

        bg_with_alpha = BG.copy()
        bg_with_alpha.set_alpha(150)
        SCREEN.blit(bg_with_alpha, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("BATTLE OF TANKS", True, "#000000")
        menu_rect = menu_text.get_rect(center=(600, 150))

        play_button = Button(image=pygame.image.load("assets/Play.png"), pos=(600, 400),
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        quit_button = Button(image=pygame.image.load("assets/Quit.png"), pos=(600, 550),
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
