import pygame
import os
pygame.mixer.init()
pygame.font.init()

# Variables

FPS = 60
VEL = 1 # VELOCITY/SPEED OF TANK
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
USER1_WIDTH, USER1_HEIGHT = 60, 70
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HP_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 40)
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets/bg.png')), (WIDTH, HEIGHT))

BULLET_BG = pygame.mixer.Sound(os.path.join('Assets', 'fire.wav'))
BULLET_VEL = 5
MAX_BULLET = 5
USER1_HIT = pygame.USEREVENT + 1
USER2_HIT = pygame.USEREVENT +2
pygame.display.set_caption("Battle Of Tanks")

# Image Import/Adjustment

USER1_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'tank.png'))
USER1_TANK = pygame.transform.rotate(pygame.transform.scale(USER1_TANK_IMAGE, (USER1_WIDTH, USER1_HEIGHT)), 0)
USER2_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'tank_enemy.png'))
USER2_TANK = pygame.transform.rotate(pygame.transform.scale(USER2_TANK_IMAGE, (USER1_WIDTH, USER1_HEIGHT)), 0)

def drawing_window(USER1, USER2, user1_bullets, user2_bullets, user1_hp, user2_hp):
        WIN.blit(BG, (0, 0))

        user1_hp_text = HP_FONT.render("Tank HP: " + str(user1_hp), 1, WHITE)
        user2_hp_text = HP_FONT.render("Tank HP: " + str(user2_hp), 1, WHITE)
        WIN.blit(user1_hp_text, (10, 10))
        WIN.blit(user2_hp_text, (WIDTH - user1_hp_text.get_width() - 10, 10))
        pygame.draw.rect(WIN, BLACK, BORDER)
        WIN.blit(USER1_TANK, (USER1.x, USER1.y))
        WIN.blit(USER2_TANK, (USER2.x, USER2.y))

        for bullet in user1_bullets:
            pygame.draw.rect(WIN, BLACK, bullet)

        for bullet in user2_bullets:
            pygame.draw.rect(WIN, BLACK, bullet)
        
        pygame.display.update()

def user1_movement(keys_pressed, USER1):
        if keys_pressed[pygame.K_a] and USER1.x - VEL > 0: # LEFT KEY
            USER1.x -= VEL
        if keys_pressed[pygame.K_d] and USER1.x + VEL + USER1.width < BORDER.x: # RIGHT KEY
            USER1.x += VEL
        if keys_pressed[pygame.K_w] and USER1.y - VEL > 0: # UP KEY
            USER1.y -= VEL
        if keys_pressed[pygame.K_s] and USER1.y + VEL + USER1.height < HEIGHT: # DOWN KEY
            USER1.y += VEL

def user2_movement(keys_pressed, USER2):
        if keys_pressed[pygame.K_LEFT] and USER2.x - VEL  > BORDER.x + BORDER.width: # LEFT KEY
            USER2.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and USER2.x + VEL + USER2.width < WIDTH: # RIGHT KEY
            USER2.x += VEL
        if keys_pressed[pygame.K_UP] and USER2.y - VEL > 0: # UP KEY
            USER2.y -= VEL
        if keys_pressed[pygame.K_DOWN] and USER2.y + VEL + USER2.height < HEIGHT: # DOWN KEY
            USER2.y += VEL

def handle_bullets(user1_bullets, user2_bullets, USER1, USER2):
    for bullet in user1_bullets:
        bullet.x += BULLET_VEL
        if USER2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(USER2_HIT))
            user1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            user1_bullets.remove(bullet)

    for bullet in user2_bullets:
        bullet.x -= BULLET_VEL
        if USER1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(USER1_HIT))
            user2_bullets.remove(bullet)
        elif bullet.x < 0:
            user2_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    USER1 = pygame.Rect(100, 300, USER1_WIDTH, USER1_HEIGHT)
    USER2 = pygame.Rect(800, 300, USER1_WIDTH, USER1_HEIGHT)

    user1_bullets = []
    user2_bullets = []

    user1_hp = 10
    user2_hp = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(user1_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(USER1.x + USER1.width, USER1.y + USER1.height//2 - 2, 10, 5)
                    user1_bullets.append(bullet)
                    BULLET_BG.play()


                if event.key == pygame.K_RALT and len(user2_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(USER2.x, USER2.y + USER2.height//2 - 2, 10, 5)
                    user2_bullets.append(bullet)
                    BULLET_BG.play()

            if event.type == USER1_HIT:
                user1_hp -= 1

            if event.type == USER2_HIT:
                user2_hp -= 1

        winner_text = ""
        if user1_hp <= 0:
            winner_text = "PLAYER 2 WINS!"

        if user2_hp <= 0:
            winner_text = "PLAYER 1 WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        user1_movement(keys_pressed, USER1)
        user2_movement(keys_pressed, USER2)
        handle_bullets(user1_bullets, user2_bullets, USER1, USER2)

        drawing_window(USER1, USER2, user1_bullets, user2_bullets, user1_hp, user2_hp)

        

                
    main()

if __name__ == "__main__":
    main()



