# Project Started: December 19, 2025
## AUTHORS----------------------------------------------------
# Back-end: DALAGON, TOLEDO ---- GAME LOGIC AND FUNCTIONALITY
# Front-end: PAITAN, RAMOS ---- UI/UX
# Assets/Graphics: ARTILLO
#---------------------------------------------------------------

import pygame
import sys
import os
import math

pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("Battle of Tanks")

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
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
P_WIDTH, P_HEIGHT = 80, 80  # Tank size
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
bullet_speed = 5


# Image Import/Adjustment
BG = pygame.image.load(os.path.join('Assets', 'bg.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
PLAYER1_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'P1.png')).convert_alpha()
PLAYER2_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'P2.png')).convert_alpha()
BOT_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'BOT.png')).convert_alpha()
bullets_sprite = pygame.image.load(os.path.join('Assets', 'Sprites', 'Bullets.png')).convert_alpha()
tank_explode = pygame.image.load(os.path.join('Assets', 'Sprites', 'explosion.png')).convert_alpha()
explosion_sheet_1 = tank_explode
explosion_sheet_2 = tank_explode


# Fonts
ftitle = pygame.font.Font(os.path.join('Assets', 'title.ttf'), 80)
bfont = pygame.font.Font(os.path.join('Assets', 'font2.otf'), 30)


def draw_moving_grid(surface, offset_x, offset_y, grid_size=GRID_SIZE):
    # Draws vertical lines
    for x in range(-grid_size, WIDTH + grid_size, grid_size):
        pygame.draw.line(surface, CB, (x + offset_x, 0), (x + offset_x, 700), 1)
    # Draws horizontal lines
    for y in range(-grid_size, 700 + grid_size, grid_size):
        pygame.draw.line(surface, CB, (0, y + offset_y), (1200, y + offset_y), 1)


def draw_battlefield(surface):
    surface.fill((45, 48, 50))
    for x in range(0, WIDTH, 50):
        pygame.draw.line(surface, (55, 58, 60), (x, 80), (x, HEIGHT))
    for y in range(80, HEIGHT, 50):
        pygame.draw.line(surface, (55, 58, 60), (0, y), (WIDTH, y))
    pygame.draw.rect(surface, (255, 215, 0), (WIDTH//2 - 1, 75, 2, HEIGHT))

def get_explode_frames(sheet, num_frames=10, frame_w=64, frame_h=64):
    frames = []
    for i in range(num_frames):
        frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (i * frame_w, frame_h))
        frames.append(frame.convert_alpha())
    return frames


def get_bullet(sheet, row, col, w=16, h=16):
    bullet = pygame.Surface((w, h), pygame.SRCALPHA)
    bullet.blit(sheet, (0, 0), (col * w, row * h, w, h))
    return bullet.convert_alpha()

# Frames for explosion animation/bullet sprites
explosion_small_f = get_explode_frames(explosion_sheet_1, 10, 64, 64)
explosion_big_f = get_explode_frames(explosion_sheet_2, 10, 64, 64)
p1bullet = [
    get_bullet(bullets_sprite, 0, 0, 16, 16),
    get_bullet(bullets_sprite, 0, 1, 16, 16),
    get_bullet(bullets_sprite, 0, 2, 16, 16),
]
p2bullet = [
    get_bullet(bullets_sprite, 0, 3, 16, 16),
    get_bullet(bullets_sprite, 0, 4, 16, 16),
    get_bullet(bullets_sprite, 0, 5, 16, 16),
]
botbullet = [
    get_bullet(bullets_sprite, 0, 6, 16, 16),
    get_bullet(bullets_sprite, 0, 7, 16, 16),
    get_bullet(bullets_sprite, 0, 8, 16, 16),
]

class Button:
    def __init__(self, text, x_pos, y_pos, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (500, 100))
        
    def draw(self):
        button_text = bfont.render(self.text, True, 'black')
        if self.enabled:
            if self.is_hovered():
                pygame.draw.rect(WIN, DEEP_BLUE, self.button_rect, 0, 20)
            else:
                pygame.draw.rect(WIN, CB, self.button_rect, 0, 20)
        else:
            pygame.draw.rect(WIN, METAL, self.button_rect, 3, 20)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        WIN.blit(button_text, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.button_rect.collidepoint(mouse_pos)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos) and self.enabled:
                return True
        return False

class Explosion:
    def __init__(self, x, y, explosion_type='small'):
        if explosion_type == 'small':
            self.frames = explosion_small_f
            self.scale = 0.8
        else:
            self.frames = explosion_big_f
            self.scale = 1.8

        # Scaling frames guys!
        if self.scale != 1.0:
            size = int(64 * self.scale)
            self.frames = [pygame.transform.scale(f, (size, size)) for f in self.frames]

        self.current_frame = 0
        self.animation_speed = 2
        self.frame_counter = 0
        self.x = x
        self.y = y

    def update(self, surface):
        if self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]
            rect = frame.get_rect(center=(self.x, self.y))
            surface.blit(frame, rect)

    def is_finished(self):
        return self.current_frame >= len(self.frames)

class bullet:
    def __init__(self, x, y, dir, bullet_frames=None):
        if bullet_frames is None:
            bullet_frames = [get_bullet(bullets_sprite, 0, 0, 16, 16)]
            self.frames = bullet_frames
            self.current_frames = 0
            self.animation_speed = 2
            self.animation_counter = 0
            self.dir = dir
            self.speed = bullet_speed
            self.original_img = self.frames[0]

            if dir == -1:
                self.img = pygame.transform.flip(self.original_img, True, False)
            else:
                self.img = self.original_img

            self.rect = self.img.get_rect()
            self.rect.x = x
            self.rect.y = y

    def update(self):
        self.rect.x += self.speed * self.dir
        if len(self.frames) > 1:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_frames = (self.current_frames + 1) % len(self.frames)
                self.original_img = self.frames[self.current_frames]
                if self.dir == -1:
                    self.img = pygame.transform.flip(self.original_img, True, False)
                else:
                    self.img = self.original_img

    def draw(self, surface):
        surface.blit(self.img, self.rect)
    
    def is_off_screen(self):
        return self.rect.x < 0 or self.rect.x > WIDTH + 20


class Tank:
    def __init__(self, x, y, image, player_type, controls=None):
        # PLAYER
        self.original_image = pygame.transform.scale(image, (P_WIDTH, P_HEIGHT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.width = P_WIDTH
        self.height = P_HEIGHT
        self.vel = 3
        self.angle = 0
        self.health = 100
        self.max_health = 100
        self.player_type = player_type
        self.controls = controls
        self.bullet = []
        self.alive = True

        # BOT
        self.bot_dir = 'idle'
        self.bot_timer = 0
        self.shoot_cooldown = 0


    def move(self, keys_pressed, other_tank=None):
        if not self.alive:
            return
        
        old_x = self.x
        old_y = self.y

        # Player 1 controls - WASD
        if self.player_type == "P1":
            if keys_pressed[pygame.K_a] and self.x - self.vel > 0:
                self.x -= self.vel
                self.angle = 180  # Face LEFT
            if keys_pressed[pygame.K_d] and self.x + self.vel + self.width < WIDTH:
                self.x += self.vel
                self.angle = 0  # Face RIGHT
            if keys_pressed[pygame.K_w] and self.y - self.vel > 80:
                self.y -= self.vel
                self.angle = 90  # Face UP
            if keys_pressed[pygame.K_s] and self.y + self.vel + self.height < HEIGHT:
                self.y += self.vel
                self.angle = 270  # Face DOWN

        # Player 2 controls - Arrow Keys
        elif self.player_type == "P2":
            if keys_pressed[pygame.K_LEFT] and self.x - self.vel > 0:
                self.x -= self.vel
                self.angle = 0
            if keys_pressed[pygame.K_RIGHT] and self.x + self.vel + self.width < WIDTH:
                self.x += self.vel
                self.angle = 180
            if keys_pressed[pygame.K_UP] and self.y - self.vel > 80:
                self.y -= self.vel
                self.angle = 270
            if keys_pressed[pygame.K_DOWN] and self.y + self.vel + self.height < HEIGHT:
                self.y += self.vel
                self.angle = 90

        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        surface.blit(rotated_image, rotated_rect)

        health_bar_width = 80
        health_bar_height = 10
        health_ratio = self.health / 100
        health_bar_x = self.x + (self.width // 2) - (health_bar_width // 2)
        health_bar_y = self.y - 15


        pygame.draw.rect(surface, RED,
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
                            border_radius=5)

        pygame.draw.rect(surface, GREEN,
                        (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height),
                            border_radius=5)




def VSPLAYER():

    clock = pygame.time.Clock()

    # Create tanks
    player1 = Tank(100, 350, PLAYER1_TANK_IMAGE, "P1")
    player2 = Tank(1000, 350, PLAYER2_TANK_IMAGE, "P2")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    Menu()

        keys_pressed = pygame.key.get_pressed()


        player1.move(keys_pressed)
        player2.move(keys_pressed)

        # Draw background
        draw_battlefield(WIN)

        # Draw HUD
        pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, 80))
        pygame.draw.rect(WIN, METAL, (0, 0, WIDTH, 75))
        pygame.draw.line(WIN, GOLD, (0, 75), (WIDTH, 75), 3)

        title = bfont.render("PLAYER 1 VS PLAYER 2", 1, WHITE)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        # Draw tanks
        player1.draw(WIN)
        player2.draw(WIN)

        pygame.display.update()


def VSBOT():
    pass


def Mode_Select_WIN():
    global grid_offset_x, grid_offset_y, bounce_time

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

        # Title
        T1 = ftitle.render("SELECT MODE", True, GRAY)
        T1_RECT = T1.get_rect(center=(600, 100))
        T2 = ftitle.render("SELECT MODE", True, WHITE2)
        T2_RECT = T2.get_rect(center=(600, 104 + bounce_offset * 0.3))

        Player_button = Button('PLAYER VS PLAYER', 350, 250, True)
        Bot_button = Button('PLAYER VS BOT', 350, 400, True)
        Back_button = Button('BACK', 350, 550, True)

        WIN.blit(T1, T1_RECT)
        WIN.blit(T2, T2_RECT)

        Player_button.draw()
        Bot_button.draw()
        Back_button.draw()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if Player_button.check_click(event):
                run = False
                VSPLAYER()

            if Bot_button.check_click(event):
                run = False
                VSBOT()

            if Back_button.check_click(event):
                run = False
                Menu()

        pygame.display.update()


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

        T1 = ftitle.render("BATTLE OF TANKS", True, GRAY)
        T1_RECT = T1.get_rect(center=(600, 100))
        T2 = ftitle.render("BATTLE OF TANKS", True, WHITE2)
        T2_RECT = T2.get_rect(center=(600, 104 + bounce_offset * 0.3))
        
        P1 = pygame.transform.scale(PLAYER1_TANK_IMAGE, (250, 250))
        P1 = pygame.transform.rotate(P1, 90)
        P2 = pygame.transform.scale(PLAYER2_TANK_IMAGE, (250, 250))
        P2 = pygame.transform.rotate(P2, -90)

        play_button = Button('PLAY', 350, 300, True)
        quit_button = Button('QUIT', 350, 450, True)
        play_button.draw()
        quit_button.draw()

        WIN.blit(P1, (925, 400 + bounce_offset))
        WIN.blit(P2, (25, 400 - bounce_offset))
        WIN.blit(T1, T1_RECT)
        WIN.blit(T2, T2_RECT)

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if play_button.check_click(event):
                run = False
                Mode_Select_WIN()

            if quit_button.check_click(event):
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    Menu()