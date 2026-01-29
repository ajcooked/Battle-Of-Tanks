import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of Tanks")


WHITE = (220, 220, 220)
GREEN = (40, 255, 40)
RED = (255, 40, 40)
BLACK = (20, 20, 25)
GRAY = (100, 105, 110)
METAL = (50, 55, 60)
GOLD = (255, 215, 0)
DEEP_BLUE = (20, 25, 30)
CRATE_COLOR = (139, 69, 19)


TANK_SIZE = 40
SPEED = 5
BULLET_SPEED = 10
clock = pygame.time.Clock()


font_main_title = pygame.font.SysFont("Impact", 80)
font_hud = pygame.font.SysFont("Impact", 28)
font_mode = pygame.font.SysFont("Impact", 18)
font_button = pygame.font.SysFont("Verdana", 24, bold=True)
font_victory = pygame.font.SysFont("Impact", 70) # Font for victory message


particles = []
obstacles = []

def create_fx(x, y, color, amount=5, type="spark"):
    for _ in range(amount):
        particles.append({
            "pos": [x, y],
            "vel": [random.uniform(-3, 3), random.uniform(-3, 3)],
            "timer": random.randint(10, 20),
            "color": color,
            "type": type
        })

def draw_glass_rect(surface, rect, color, alpha):
    s = pygame.Surface((rect.width, rect.height))
    s.set_alpha(alpha)
    s.fill(color)
    surface.blit(s, (rect.x, rect.y))
    pygame.draw.rect(surface, GOLD, rect, 2, border_radius=8)

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.health = 3
    
    def draw(self):
        pygame.draw.rect(screen, (80, 40, 20), self.rect, border_radius=4)
        pygame.draw.rect(screen, (139, 69, 19), (self.rect.x+4, self.rect.y+4, 32, 32), border_radius=2)
        pygame.draw.line(screen, (60, 30, 10), self.rect.topleft, self.rect.bottomright, 3)
        pygame.draw.line(screen, (60, 30, 10), self.rect.topright, self.rect.bottomleft, 3)

class Tank:
    def __init__(self, x, y, color, controls=None, bot=False):
        self.rect = pygame.Rect(x, y, TANK_SIZE, TANK_SIZE)
        self.color = color
        self.controls = controls
        self.bullets = []
        self.health = 5
        self.bot = bot
        self.bot_dir = 'idle'
        self.bot_timer = 0

    def move(self, keys=None):
        old_pos = self.rect.copy()
        
        if self.bot:
            self.bot_timer -= 1
            if self.bot_timer <= 0:
                self.bot_dir = random.choice(['up', 'down', 'left', 'right', 'idle'])
                self.bot_timer = random.randint(30, 60)
            
            if self.bot_dir == 'up': self.rect.y -= SPEED
            elif self.bot_dir == 'down': self.rect.y += SPEED
            elif self.bot_dir == 'left': self.rect.x -= SPEED
            elif self.bot_dir == 'right': self.rect.x += SPEED
            if random.random() < 0.02: self.shoot()
        elif keys and self.controls:
            if keys[self.controls["up"]]: self.rect.y -= SPEED
            if keys[self.controls["down"]]: self.rect.y += SPEED
            if keys[self.controls["left"]]: self.rect.x -= SPEED
            if keys[self.controls["right"]]: self.rect.x += SPEED

        for obs in obstacles:
            if self.rect.colliderect(obs.rect):
                self.rect = old_pos

        if self.rect.top < 85: self.rect.top = 85
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT
        
        if self.color == GREEN: 
            if self.rect.right > 395: self.rect.right = 395
            if self.rect.left < 5: self.rect.left = 5
        else: 
            if self.rect.left < 405: self.rect.left = 405
            if self.rect.right > WIDTH - 5: self.rect.right = WIDTH - 5

    def shoot(self):
        if len(self.bullets) < 5:
            direction = 1 if self.rect.x < 400 else -1
            bx = self.rect.right if direction == 1 else self.rect.left - 16
            bullet = pygame.Rect(bx, self.rect.centery - 4, 16, 8)
            self.bullets.append([bullet, direction])

    def draw(self):
        pygame.draw.rect(screen, (0,0,0,80), (self.rect.x+4, self.rect.y+4, TANK_SIZE, TANK_SIZE), border_radius=5)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)
        
        if self.rect.x < 400:
            pygame.draw.rect(screen, self.color, (self.rect.right, self.rect.centery - 5, 18, 10), border_radius=2)
            pygame.draw.rect(screen, BLACK, (self.rect.right, self.rect.centery - 5, 18, 10), 1, border_radius=2)
        else:
            pygame.draw.rect(screen, self.color, (self.rect.left - 18, self.rect.centery - 5, 18, 10), border_radius=2)
            pygame.draw.rect(screen, BLACK, (self.rect.left - 18, self.rect.centery - 5, 18, 10), 1, border_radius=2)

def draw_hud(t1, t2, bot_mode):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 80))
    pygame.draw.rect(screen, METAL, (0, 0, WIDTH, 75))
    pygame.draw.line(screen, GOLD, (0, 75), (WIDTH, 75), 3)
    
    title = font_hud.render("Battle of Tanks", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 5))
    
    mode_str = "PLAYER vs BOT" if bot_mode else "MULTIPLAYER MODE"
    mode_color = RED if bot_mode else GREEN
    mode_txt = font_mode.render(mode_str, True, mode_color)
    screen.blit(mode_txt, (WIDTH//2 - mode_txt.get_width()//2, 38))

    esc_tip = pygame.font.SysFont("Arial", 11, bold=True).render("[ESC] FOR EXIT", True, GOLD)
    screen.blit(esc_tip, (WIDTH//2 - esc_tip.get_width()//2, 58))

    pygame.draw.rect(screen, BLACK, (20, 25, 205, 25), border_radius=4)
    if t1.health > 0:
        pygame.draw.rect(screen, GREEN, (22, 27, t1.health * 40, 21), border_radius=2)
    
    pygame.draw.rect(screen, BLACK, (WIDTH - 225, 25, 205, 25), border_radius=4)
    if t2.health > 0:
        bar_w = t2.health * 40
        pygame.draw.rect(screen, RED, (WIDTH - 22 - bar_w, 27, bar_w, 21), border_radius=2)


def show_victory(winner_text, color):
 
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))


    shadow = font_victory.render(winner_text, True, (20, 20, 20))
    text = font_victory.render(winner_text, True, color)
    
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(shadow, (text_rect.x + 5, text_rect.y + 5))
    screen.blit(text, text_rect)

    restart_txt = font_button.render("PRESS ANY KEY FOR MENU", True, WHITE)
    screen.blit(restart_txt, (WIDTH//2 - restart_txt.get_width()//2, HEIGHT//2 + 80))
    
    pygame.display.update()
    
 
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def game_loop(bot_mode):
    global obstacles, particles
    particles = []
    obstacles = [Obstacle(380, 150), Obstacle(380, 300), Obstacle(380, 450)]
    
    t1 = Tank(100, 300, GREEN, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d})
    t2 = Tank(660, 300, RED, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}, bot=bot_mode)
    
    running = True
    while running:
        screen.fill((45, 48, 50))
        for x in range(0, WIDTH, 50):
            pygame.draw.line(screen, (55, 58, 60), (x, 80), (x, HEIGHT))
        for y in range(80, HEIGHT, 50):
            pygame.draw.line(screen, (55, 58, 60), (0, y), (WIDTH, y))
        
        pygame.draw.rect(screen, (255, 215, 0, 50), (399, 75, 2, HEIGHT))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_SPACE: t1.shoot()
                if not t2.bot and event.key == pygame.K_RETURN: t2.shoot()

        keys = pygame.key.get_pressed()
        t1.move(keys)
        t2.move(keys)

        for t, enemy in [(t1, t2), (t2, t1)]:
            for b_data in t.bullets[:]:
                bullet, direction = b_data
                bullet.x += (BULLET_SPEED * direction)
                pygame.draw.rect(screen, GOLD if t == t1 else (255, 100, 100), bullet, border_radius=2)
                
                hit_obs = False
                for obs in obstacles[:]:
                    if bullet.colliderect(obs.rect):
                        obs.health -= 1
                        create_fx(bullet.x, bullet.y, (139, 69, 19), 8, "spark")
                        if obs.health <= 0: obstacles.remove(obs)
                        t.bullets.remove(b_data)
                        hit_obs = True
                        break
                if hit_obs: continue

                if bullet.colliderect(enemy.rect):
                    enemy.health -= 1
                    create_fx(bullet.x, bullet.y, enemy.color, 20, "spark")
                    t.bullets.remove(b_data)
                elif bullet.x < -20 or bullet.x > WIDTH + 20: 
                    t.bullets.remove(b_data)

        for p in particles[:]:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["timer"] -= 1
            if p["timer"] <= 0: particles.remove(p)
            else:
                pygame.draw.circle(screen, p["color"], (int(p["pos"][0]), int(p["pos"][1])), 3)

        for obs in obstacles: obs.draw()
        t1.draw(); t2.draw()
        draw_hud(t1, t2, bot_mode)
        

        if t1.health <= 0:
            show_victory("RED TANK WON!", RED)
            running = False
        elif t2.health <= 0:
            show_victory("GREEN TANK WON!", GREEN)
            running = False

        pygame.display.update()
        clock.tick(60)

def main_menu():
    counter = 0
    while True:
        counter += 1
        screen.fill(DEEP_BLUE)
        for i in range(0, WIDTH, 40):
            offset = (counter % 40)
            pygame.draw.line(screen, (40, 45, 50), (i + offset, 0), (i + offset, HEIGHT), 1)
            pygame.draw.line(screen, (40, 45, 50), (0, i + offset), (WIDTH, i + offset), 1)

        title_surf = font_main_title.render("Battle of Tanks", True, GOLD)
        title_rect = title_surf.get_rect(center=(WIDTH//2, 150))
        glow = abs(int(random.uniform(2, 6)))
        shadow_surf = font_main_title.render("BATTLE OF TANKS", True, (80, 60, 0))
        screen.blit(shadow_surf, (title_rect.x + glow, title_rect.y + glow))
        screen.blit(title_surf, title_rect)
        
        btn1_rect = pygame.Rect(WIDTH//2 - 150, 310, 300, 60)
        draw_glass_rect(screen, btn1_rect, METAL, 200)
        txt1 = font_button.render("[ 1 ]  MULTIPLAYER", True, WHITE)
        screen.blit(txt1, (btn1_rect.centerx - txt1.get_width()//2, btn1_rect.centery - txt1.get_height()//2))

        btn2_rect = pygame.Rect(WIDTH//2 - 150, 400, 300, 60)
        draw_glass_rect(screen, btn2_rect, METAL, 200)
        txt2 = font_button.render("[ 2 ]  PLAYER vs BOT", True, WHITE)
        screen.blit(txt2, (btn2_rect.centerx - txt2.get_width()//2, btn2_rect.centery - txt2.get_height()//2))

        if (counter // 30) % 2 == 0:
            tip_text = pygame.font.SysFont("Arial", 16, bold=True).render("SELECT MODE TO ENGAGE", True, GOLD)
            screen.blit(tip_text, (WIDTH//2 - tip_text.get_width()//2, 530))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: game_loop(False)
                if event.key == pygame.K_2: game_loop(True)
        clock.tick(60)

if __name__ == "__main__":
    main_menu()