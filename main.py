# Project Started: December 19, 2025
## AUTHORS----------------------------------------------------
# Back-end: DALAGON, TOLEDO ---- GAME LOGIC AND FUNCTIONALITY
# Front-end: PAITAN, RAMOS, ARTILLO ---- UI/UX
#---------------------------------------------------------------

import pygame
import sys
import os
import math
import random

pygame.mixer.init()
pygame.font.init()

#  CONSTANTS
WIDTH, HEIGHT = 800, 600
FPS = 60
TANK_SIZE = 80
BULLET_SIZE = 24
BULLET_SPEED = 7
TANK_SPEED = 3
HEADER_HEIGHT = 80
GRID_SIZE = 60

# Colors
COLOR = {
    'bg': (45, 48, 50),
    'grid': (55, 58, 60),
    'ui_bg': (20, 20, 25),
    'ui_metal': (50, 55, 60),
    'ui_gold': (255, 215, 0),
    'ui_deep_blue': (20, 25, 30),
    'ui_cb': (203, 203, 203),
    'white': (255, 255, 255),
    'white2': (255, 255, 227),
    'gray': (100, 105, 110),
    'green': (40, 255, 40),
    'red': (255, 40, 40),
}

# ========== GAME SETUP ========== (MOVE THIS UP!)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of Tanks")
clock = pygame.time.Clock()

# ========== ASSETS ========== (NOW LOAD IMAGES)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def load_image(path, scale=None): 
    img = pygame.image.load(os.path.join('Assets', path)).convert_alpha() 
    path = "icon.png"
    return pygame.transform.scale(img, scale) if scale else img

def load_sprite(sheet, row, col, size=(16, 16), scale=None):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.blit(sheet, (0, 0), (col * size[0], row * size[1], *size))
    return pygame.transform.scale(surf, scale) if scale else surf.convert_alpha()

# Images
img_icon = load_image('icon.png')
img_bg = load_image('bg.png', (WIDTH, HEIGHT))
img_tank_p1 = load_image('Sprites/P1.png')
img_tank_p2 = load_image('Sprites/P2.png')
img_tank_bot = load_image('Sprites/BOT.png')
img_rock = load_image('Sprites/rock1.png')
img_bullet_sheet = load_image('Sprites/Bullets.png')
img_explosion_sheet = load_image('Sprites/explosion.png')

# Set window icon (AFTER loading)
pygame.display.set_icon(img_icon)

# Fonts
font_title = pygame.font.Font(os.path.join('Assets', 'Fonts', 'title.ttf'), 60)
font_button = pygame.font.Font(os.path.join('Assets', 'Fonts', 'font2.otf'), 24)

# Bullets & Explosions
bullets_p1 = [load_sprite(img_bullet_sheet, 0, i, (16, 16), (BULLET_SIZE, BULLET_SIZE)) for i in range(3)]
bullets_p2 = [load_sprite(img_bullet_sheet, 0, i + 3, (16, 16), (BULLET_SIZE, BULLET_SIZE)) for i in range(3)]
bullets_bot = [load_sprite(img_bullet_sheet, 0, i + 6, (16, 16), (BULLET_SIZE, BULLET_SIZE)) for i in range(3)]

def load_music(filename):
    try:
        pygame.mixer.music.load(os.path.join('Assets', filename))
        return True
    except:
        print(f"Warning: {filename} not fount")
        return False
    
def play_music(filename, volume=0.5, loops=-1):
    if load_music(filename):
        pygame.mixer.music.play(loops)
        pygame.mixer.music.set_volume(volume)
sound_shoot = None
try:
    sound_shoot = pygame.mixer.Sound(os.path.join('Assets', 'Audio', 'shoot.wav'))
    sound_shoot.set_volume(0.1)
    print("✓ Shoot sound loaded!")
except:
    print("✗ Warning: shoot.wav not found")

def get_explosion_frames(sheet, num=10, size=64, scale=1.0):
    frames = []
    for i in range(num):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.blit(sheet, (0, 0), (i * size, 0, size, size))
        if scale != 1.0:
            surf = pygame.transform.scale(surf, (int(size * scale), int(size * scale)))
        frames.append(surf.convert_alpha())
    return frames

explosion_small = get_explosion_frames(img_explosion_sheet, scale=0.6)
explosion_big = get_explosion_frames(img_explosion_sheet, scale=1.4)

# ========== UI GLOBALS ==========
grid_offset_x = grid_offset_y = bounce_time = 0

# ========== HELPER FUNCTIONS ==========
def draw_grid(surface, offset_x, offset_y):
    for i in range(-GRID_SIZE, max(WIDTH, HEIGHT) + GRID_SIZE, GRID_SIZE):
        if i + offset_x < WIDTH:
            pygame.draw.line(surface, COLOR['ui_cb'], (i + offset_x, 0), (i + offset_x, HEIGHT), 1)
        if i + offset_y < HEIGHT:
            pygame.draw.line(surface, COLOR['ui_cb'], (0, i + offset_y), (WIDTH, i + offset_y), 1)

def draw_battlefield(surface):
    surface.fill(COLOR['bg'])
    for x in range(0, WIDTH, 50):
        pygame.draw.line(surface, COLOR['grid'], (x, HEADER_HEIGHT), (x, HEIGHT))
    for y in range(HEADER_HEIGHT, HEIGHT, 50):
        pygame.draw.line(surface, COLOR['grid'], (0, y), (WIDTH, y))
    pygame.draw.rect(surface, COLOR['ui_gold'], (WIDTH // 2 - 1, HEADER_HEIGHT, 2, HEIGHT - HEADER_HEIGHT))

def draw_header(surface, title, tank1=None, tank2=None, elapsed_time=0.0):
    pygame.draw.rect(surface, COLOR['ui_bg'], (0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.rect(surface, COLOR['ui_metal'], (0, 0, WIDTH, HEADER_HEIGHT - 3))
    pygame.draw.line(surface, COLOR['ui_gold'], (0, HEADER_HEIGHT - 3), (WIDTH, HEADER_HEIGHT - 3), 3)
    
    # === LEFT: Player 1 ===
    if tank1:
        # Name
        p1_name = font_button.render("PLAYER 1", True, COLOR['green'] if tank1.alive else COLOR['gray'])
        surface.blit(p1_name, (10, 8))
        
        # Health bar
        bar_w, bar_h = 80, 12
        pygame.draw.rect(surface, (60, 60, 60), (10, 32, bar_w, bar_h), border_radius=5)
        if tank1.alive:
            health_ratio = tank1.health / 100
            pygame.draw.rect(surface, COLOR['green'], (10, 32, bar_w * health_ratio, bar_h), border_radius=5)
        
        # Health percentage
        health_txt = font_button.render(f"{tank1.health}%", True, COLOR['white'])
        surface.blit(health_txt, (95, 30))
    
    # === CENTER: VS + Timer ===
    vs_font = pygame.font.Font(os.path.join('Assets', 'Fonts', 'title.ttf'), 35)
    vs_txt = vs_font.render("VS", True, COLOR['ui_gold'])
    surface.blit(vs_txt, (WIDTH // 2 - 25, 5))
    
    # Timer
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_txt = font_button.render(f"{minutes:02d}:{seconds:02d}", True, COLOR['white'])
    surface.blit(timer_txt, (WIDTH // 2 - timer_txt.get_width() // 2, 40))
    
    # === RIGHT: Player 2/Bot ===
    if tank2:
        # Name
        p2_label = "BOT" if tank2.tank_type == 'BOT' else "PLAYER 2"
        p2_name = font_button.render(p2_label, True, COLOR['red'] if tank2.alive else COLOR['gray'])
        surface.blit(p2_name, (WIDTH - p2_name.get_width() - 10, 8))
        
        # Health bar
        bar_w, bar_h = 80, 12
        pygame.draw.rect(surface, (60, 60, 60), (WIDTH - 90, 32, bar_w, bar_h), border_radius=5)
        if tank2.alive:
            health_ratio = tank2.health / 100
            pygame.draw.rect(surface, COLOR['red'], (WIDTH - 90, 32, bar_w * health_ratio, bar_h), border_radius=5)
        
        # Health percentage
        health_txt = font_button.render(f"{tank2.health}%", True, COLOR['white'])
        surface.blit(health_txt, (WIDTH - 165, 30))

# ========== CLASSES ==========
class Button:
    def __init__(self, text, x, y, w=350, h=70):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        
    def draw(self, surface):
        color = COLOR['white'] if self.is_hovered() else COLOR['ui_cb']
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        txt = font_button.render(self.text, True, COLOR['ui_bg'])
        surface.blit(txt, txt.get_rect(center=self.rect.center))
    
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered()


class Explosion:
    def __init__(self, x, y, big=False):
        self.frames = explosion_big if big else explosion_small
        self.x, self.y = x, y
        self.frame = 0
        self.speed = 2
        self.counter = 0
    
    def update(self):
        self.counter += 1
        if self.counter >= self.speed:
            self.counter = 0
            self.frame += 1
    
    def draw(self, surface):
        if self.frame < len(self.frames):
            surface.blit(self.frames[self.frame], self.frames[self.frame].get_rect(center=(self.x, self.y)))
    
    def is_finished(self):
        return self.frame >= len(self.frames)


class Rock:
    def __init__(self, x, y, size=80):  # ← Changed default from 60 to 80
        self.image = pygame.transform.scale(img_rock, (size, size))  # ← Use img_rock
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 30
        self.alive = True
    
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
    
    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)


class Bullet:
    DIRECTIONS = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
    
    def __init__(self, x, y, direction, frames):
        self.frames = frames
        self.direction = direction
        self.dx, self.dy = self.DIRECTIONS[direction]
        self.frame_idx = 0
        self.anim_counter = 0
        self.anim_speed = 5
        
        self.rect = pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE)
        self.update_image()
    
    def update_image(self):
        """Update the current image based on frame and direction"""
        img = self.frames[self.frame_idx]
        
        # Rotate based on direction
        if self.direction == 'left':
            img = pygame.transform.flip(img, True, False)
        elif self.direction == 'up':
            img = pygame.transform.rotate(img, 90)
        elif self.direction == 'down':
            img = pygame.transform.rotate(img, -90)
        # 'right' stays as is
        
        self.image = img
    
    def update(self):
        self.rect.x += self.dx * BULLET_SPEED
        self.rect.y += self.dy * BULLET_SPEED
        
        # Animate
        self.anim_counter += 1
        if self.anim_counter >= self.anim_speed and len(self.frames) > 1:
            self.anim_counter = 0
            self.frame_idx = (self.frame_idx + 1) % len(self.frames)
            self.update_image()  # ← Update the rotated image!
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_off_screen(self):
        return not (-20 < self.rect.x < WIDTH + 20 and -20 < self.rect.y < HEIGHT + 20)


class Tank:
    def __init__(self, x, y, image, tank_type, controls=None):
        self.image_orig = pygame.transform.scale(image, (TANK_SIZE, TANK_SIZE))
        self.rect = self.image_orig.get_rect(topleft=(x, y))
        self.tank_type = tank_type
        self.controls = controls
        self.bullets = []
        self.health = 100
        self.alive = True
        self.angle = 0
        self.shoot_cooldown = 0

        if tank_type == 'P1':
            self.angle = 270  # Player 1 faces RIGHT →
        else:  # P2 or BOT
            self.angle = 90   # Player 2/Bot faces LEFT ←
        
        # Bot AI
        self.is_bot = (tank_type == 'BOT')
        self.bot_dir = 'idle'
        self.bot_timer = 0
    
    def move(self, keys, other_tank=None, barrier=None, rocks=None):
        if not self.alive:
            return
        
        old_x = self.rect.x
        old_y = self.rect.y
        
        # Bot AI
        if self.is_bot:
            self.bot_timer -= 1
            if self.bot_timer <= 0:
                self.bot_dir = random.choice(['up', 'down', 'left', 'right', 'idle'])
                self.bot_timer = random.randint(30, 60)
            
            if self.bot_dir == 'up' and self.rect.y - TANK_SPEED > HEADER_HEIGHT:
                self.rect.y -= TANK_SPEED
                self.angle = 0
            elif self.bot_dir == 'down' and self.rect.bottom + TANK_SPEED < HEIGHT:
                self.rect.y += TANK_SPEED
                self.angle = 180
            elif self.bot_dir == 'left' and self.rect.x - TANK_SPEED > 0:
                self.rect.x -= TANK_SPEED
                self.angle = 90
            elif self.bot_dir == 'right' and self.rect.right + TANK_SPEED < WIDTH:
                self.rect.x += TANK_SPEED
                self.angle = 270
            
            if random.random() < 0.02:
                self.shoot()
        
        # Player controls
        elif keys and self.controls:
            if keys[self.controls['up']] and self.rect.y - TANK_SPEED > HEADER_HEIGHT:
                self.rect.y -= TANK_SPEED
                self.angle = 0
            if keys[self.controls['down']] and self.rect.bottom + TANK_SPEED < HEIGHT:
                self.rect.y += TANK_SPEED
                self.angle = 180
            if keys[self.controls['left']] and self.rect.x - TANK_SPEED > 0:
                self.rect.x -= TANK_SPEED
                self.angle = 90
            if keys[self.controls['right']] and self.rect.right + TANK_SPEED < WIDTH:
                self.rect.x += TANK_SPEED
                self.angle = 270
        
        # ========== CHECK ALL COLLISIONS ==========
        collision_detected = False
        
        # Barrier collision (CENTER LINE)
        if barrier and self.rect.colliderect(barrier):
            collision_detected = True
        
        # Rock collision
        if not collision_detected and rocks:
            for rock in rocks:
                if rock.alive and self.rect.colliderect(rock.rect):
                    collision_detected = True
                    break
        
        # Tank collision
        if not collision_detected and other_tank and other_tank.alive:
            if self.rect.colliderect(other_tank.rect):
                collision_detected = True
        
        # If any collision, restore old position
        if collision_detected:
            self.rect.x = old_x
            self.rect.y = old_y
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self):
        if not self.alive or len(self.bullets) >= 5 or self.shoot_cooldown > 0:
            return
        
        # Calculate bullet spawn position based on tank angle
        half_bullet = BULLET_SIZE // 2
        
        if self.angle == 0:  # UP
            bx = self.rect.centerx - half_bullet
            by = self.rect.top - BULLET_SIZE
            direction = 'up'
        elif self.angle == 90:  # LEFT
            bx = self.rect.left - BULLET_SIZE
            by = self.rect.centery - half_bullet
            direction = 'left'
        elif self.angle == 180:  # DOWN
            bx = self.rect.centerx - half_bullet
            by = self.rect.bottom
            direction = 'down'
        elif self.angle == 270:  # RIGHT
            bx = self.rect.right
            by = self.rect.centery - half_bullet
            direction = 'right'
        else:
            bx = self.rect.centerx - half_bullet
            by = self.rect.top - BULLET_SIZE
            direction = 'up'
        
        # Choose bullet sprite
        if self.tank_type == 'P1':
            frames = bullets_p1
        elif self.tank_type == 'P2':
            frames = bullets_p2
        else:
            frames = bullets_bot
        
        self.bullets.append(Bullet(bx, by, direction, frames))
        self.shoot_cooldown = 30

        if sound_shoot:
            sound_shoot.play()
        
        print(f"{self.tank_type} shot bullet at ({bx}, {by}), direction: {direction}")  # ← DEBUG
    
    def update_bullets(self, enemy, explosions, rocks=None):
        to_remove = []
        
        for bullet in self.bullets:
            bullet.update()
            
            if bullet.is_off_screen():
                to_remove.append(bullet)
                continue
            
            # Rock collision
            if rocks:
                for rock in rocks:
                    if rock.alive and bullet.rect.colliderect(rock.rect):
                        rock.take_damage(10)
                        explosions.append(Explosion(bullet.rect.centerx, bullet.rect.centery, not rock.alive))
                        to_remove.append(bullet)
                        break
                if bullet in to_remove:
                    continue
            
            # Enemy collision
            if enemy and enemy.alive and bullet.rect.colliderect(enemy.rect):
                enemy.health -= 10
                explosions.append(Explosion(bullet.rect.centerx, bullet.rect.centery, False))
                to_remove.append(bullet)
                
                if enemy.health <= 0:
                    enemy.alive = False
                    for _ in range(3):
                        ox, oy = random.randint(-15, 15), random.randint(-15, 15)
                        explosions.append(Explosion(enemy.rect.centerx + ox, enemy.rect.centery + oy, True))
        
        for bullet in to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
    
    def draw(self, surface):
        if not self.alive:
            return
        
        # Tank
        rotated = pygame.transform.rotate(self.image_orig, self.angle)
        surface.blit(rotated, rotated.get_rect(center=self.rect.center))
        
        # Bullets
        for bullet in self.bullets:
            bullet.draw(surface)

        # Bullets
        for bullet in self.bullets:
            bullet.draw(surface)


# ========== GAME FUNCTIONS ==========
def show_victory(text, color):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    WIN.blit(overlay, (0, 0))
    
    txt = font_title.render(text, True, color)
    WIN.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    
    continue_txt = font_button.render("Press any key to continue...", True, COLOR['ui_cb'])
    WIN.blit(continue_txt, continue_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def countdown_start():
    """Simple 3-2-1-GO countdown"""
    for number in [3, 2, 1, "GO!"]:
        draw_battlefield(WIN)
        draw_header(WIN, "GET READY!")
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        WIN.blit(overlay, (0, 0))
        
        if number == "GO!":
            font = pygame.font.Font(os.path.join('Assets', 'Fonts', 'title.ttf'), 100)
            color = COLOR['green']
        else:
            font = font_title
            color = COLOR['ui_gold']
        
        txt = font.render(str(number), True, color)
        WIN.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.update()
        pygame.time.wait(1000 if number != "GO!" else 500)

def game_loop(vs_bot):

    play_music('Audio/Game_audio.wav', volume=0.2)
    tank1 = Tank(50, 300, img_tank_p1, 'P1', {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
    tank2 = Tank(690, 300, img_tank_bot if vs_bot else img_tank_p2, 'BOT' if vs_bot else 'P2',
                None if vs_bot else {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})
    
    barrier = pygame.Rect(WIDTH // 2 - 5, HEADER_HEIGHT, 10, HEIGHT - HEADER_HEIGHT)
    rocks = [Rock(WIDTH // 2 - 40, y, 80) for y in [150, 280, 410]]  # ← Size 80, centered better
    explosions = []

    countdown_start()
    start_time = pygame.time.get_ticks()
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return
                if event.key == pygame.K_SPACE:
                    tank1.shoot()
                if not vs_bot and event.key == pygame.K_RCTRL:
                    tank2.shoot()
        
        keys = pygame.key.get_pressed()
        tank1.move(keys, tank2, barrier, rocks)
        tank2.move(keys, tank1, barrier, rocks)
        
        tank1.update_bullets(tank2, explosions, rocks)
        tank2.update_bullets(tank1, explosions, rocks)
        
        explosions = [e for e in explosions if not (e.update() or e.is_finished())]
        
        draw_battlefield(WIN)

        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        draw_header(WIN, "PLAYER VS BOT" if vs_bot else "P1 VS P2", tank1, tank2, elapsed)
        
        for rock in rocks:
            rock.draw(WIN)
        tank1.draw(WIN)
        tank2.draw(WIN)
        for exp in explosions:
            exp.draw(WIN)
        
        if not tank1.alive:
            show_victory("BOT WINS!" if vs_bot else "PLAYER 2 WINS!", COLOR['red'])
            pygame.mixer.music.stop()
            running = False
        elif not tank2.alive:
            show_victory("PLAYER WINS!" if vs_bot else "PLAYER 1 WINS!", COLOR['green'])
            pygame.mixer.music.stop()
            running = False
        
        pygame.display.update()


def menu():
    global grid_offset_x, grid_offset_y, bounce_time

    buttons = [
        Button('PLAYER VS PLAYER', 225, 200),
        Button('PLAYER VS BOT', 225, 300),
        Button('QUIT', 225, 400)
    ]
    
    running = True
    while running:

        if not pygame.mixer.music.get_busy():
            play_music('Audio/Menu_audio.wav', volume=0.5)
        grid_offset_x = (grid_offset_x + 1) % GRID_SIZE
        grid_offset_y = (grid_offset_y + 1) % GRID_SIZE
        bounce_time += 1
        bounce_offset = math.sin(bounce_time * 0.05) * 15
        
        WIN.fill(COLOR['ui_deep_blue'])
        draw_grid(WIN, grid_offset_x, grid_offset_y)
        
        bg = img_bg.copy()
        bg.set_alpha(150)
        WIN.blit(bg, (0, 0))
        
        # Title
        shadow = font_title.render("BATTLE OF TANKS", True, COLOR['gray'])
        title = font_title.render("BATTLE OF TANKS", True, COLOR['white2'])
        WIN.blit(shadow, shadow.get_rect(center=(WIDTH // 2, 80)))
        WIN.blit(title, title.get_rect(center=(WIDTH // 2, 80 + bounce_offset * 0.3)))
        
        # Buttons
        for btn in buttons:
            btn.draw(WIN)
        
        # Decorative tanks
        tank_scale = (150, 150)
        WIN.blit(pygame.transform.scale(img_tank_p1, tank_scale), (WIDTH - 170, int(360 + bounce_offset)))
        WIN.blit(pygame.transform.scale(img_tank_p2, tank_scale), (20, int(360 - bounce_offset)))
        
        pygame.display.update()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if buttons[0].is_clicked(event):
                pygame.mixer.music.stop()
                game_loop(False)
            elif buttons[1].is_clicked(event):
                pygame.mixer.music.stop()
                game_loop(True)
            elif buttons[2].is_clicked(event):
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    menu()