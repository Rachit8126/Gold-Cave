import pygame
import random
import math

from pygame import mixer

# Initialisation
pygame.init()

# Background
bg = pygame.image.load("block.png")
bg_x = 30
bg_y = 30

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Creating Screen
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

# Background
bg_img = pygame.image.load("bg.png")

# Icon and Title
pygame.display.set_caption("Gold Cave")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Coins
coin_img = pygame.image.load("coin.png")
coin_2_img = pygame.image.load("coin_bag.png")
coin_x = 10
coin_y = 10
coin_2_x = 560
coin_2_y = 10
restrictions_x = []
restrictions_y = []

# Player
player = pygame.image.load("player.png")
player_x = 10
player_y = 560
player_x_change = 0
player_y_change = 0

# Enemy
num_of_enemies = 4
enemy_img = []
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
enemy_x = [10, 560, 10, 560]
enemy_y = [120, 230, 340, 450]
enemy_x_change = [1, -1, 1, -1]

# Score and Life
life = 5
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 24)
life_font = pygame.font.Font("freesansbold.ttf", 24)
life_x = 610
life_y = 50
text_x = 610
text_y = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)
restart_font = pygame.font.Font("freesansbold.ttf", 32)


def coin_1(coin_x, coin_y):
    screen.blit(coin_img, (coin_x, coin_y))


def coin_2(coin_2_x, coin_2_y):
    screen.blit(coin_2_img, (coin_2_x, coin_2_y))


def enemy(enemy_x, enemy_y, i):
    screen.blit(enemy_img[i], (enemy_x[i], enemy_y[i]))


def in_block(x, y, block_x, block_y, x_length, y_length):
    if block_x < x < block_x + x_length and block_y < y < block_y + y_length:
        return True
    else:
        return False


def is_collision_1(player_x, player_y, coin_x, coin_y):
    distance = math.sqrt(math.pow((player_x - coin_x), 2) + math.pow((player_y - coin_y), 2))
    if distance < 27:
        return True
    else:
        return False


def is_collision_2(player_x, player_y, coin_2_x, coin_2_y):
    distance = math.sqrt(math.pow((player_x - coin_2_x), 2) + math.pow((player_y - coin_2_y), 2))
    if distance < 27:
        return True
    else:
        return False


def show_score(text_x, text_y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 255))
    screen.blit(score, (text_x, text_y))


def over_text():
    over_text = over_font.render("GAME OVER", True, (250, 250, 250))
    restart_text = restart_font.render("Press SPACE to restart. . .", True, (250, 250, 250))
    screen.fill((0, 0, 0))
    screen.blit(restart_text, (105, 320))
    screen.blit(over_text, (100, 250))


def show_life(life_x, life_y):
    life_text = life_font.render("Lives: " + str(life), True, (0, 255, 255))
    screen.blit(life_text, (life_x, life_y))


def game_reset():
    global score_value
    global life
    global coin_x
    global coin_y
    global coin_2_x
    global coin_2_y
    score_value = 0
    life = 5
    coin_x = 10
    coin_y = 10
    coin_2_x = 560
    coin_2_y = 10
    screen.fill((0, 40, 0))
    screen.blit(bg_img, (0, 0))


def enemy_catch_player(player_x, player_y, enemy_x, enemy_y):
    distance = math.sqrt(math.pow((player_x - enemy_x), 2) + math.pow((player_y - enemy_y), 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
game_is_running = True
while game_is_running:

    # Background Color
    screen.fill((0, 40, 0))

    # Background Image
    screen.blit(bg_img, (0, 0))

    # Background blocks
    for i in range(5):
        for j in range(5):
            x1 = bg_x + 110 * i
            y1 = bg_y + 110 * j
            screen.blit(bg, (x1, y1))
            restrictions_x.append(x1)
            restrictions_y.append(y1)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                player_x_change = -3
                player_y_change = 0
            if event.key == pygame.K_RIGHT:
                player_x_change = 3
                player_y_change = 0
            if event.key == pygame.K_UP:
                player_x_change = 0
                player_y_change = -3
            if event.key == pygame.K_DOWN:
                player_x_change = 0
                player_y_change = 3
            if event.key == pygame.K_SPACE:
                game_reset()
            if event.key == pygame.K_ESCAPE:
                game_is_running = False

    # Player restriction
    if player_x > 560:
        player_x = 560
    if player_x < 10:
        player_x = 10
    if player_y > 560:
        player_y = 560
    if player_y < 10:
        player_y = 10

    for i in range(25):
        if in_block(player_x, player_y, restrictions_x[i] - 10, restrictions_y[i] - 10, 90, 80):
            collision_sound = mixer.Sound("hit.wav")
            collision_sound.play()
            player_x = 10
            player_y = 560
            if score_value > 0:
                score_value -= 10
            else:
                score_value = 0
            life -= 1

    coin_1(coin_x, coin_y)
    coin_2(coin_2_x, coin_2_y)
    if is_collision_1(player_x, player_y, coin_x, coin_y):
        coin_x = random.choice(restrictions_x) - 16
        coin_y = random.choice(restrictions_y) - 16
        coin_sound = mixer.Sound("coin.wav")
        coin_sound.play()
        score_value += 10
        player_x = 10
        player_y = 560
    if is_collision_2(player_x, player_y, coin_2_x, coin_2_y):
        coin_2_x = random.choice(restrictions_x) - 16
        coin_2_y = random.choice(restrictions_y) - 16
        coin_bag_sound = mixer.Sound("coin_bag.wav")
        coin_bag_sound.play()
        score_value += 20
        player_x = 10
        player_y = 560

    for i in range(num_of_enemies):

        # Enemy Restrictions
        if enemy_x[i] > 560:
            enemy_x[i] = 560
            enemy_x_change[i] = -1
        if enemy_x[i] < 10:
            enemy_x[i] = 10
            enemy_x_change[i] = +1

        enemy(enemy_x, enemy_y, i)
        if enemy_catch_player(player_x, player_y, enemy_x[i], enemy_y[i]):
            hit_sound = mixer.Sound("hit.wav")
            hit_sound.play()
            player_x = 10
            player_y = 560
            if score_value > 0:
                score_value -= 20
            else:
                score_value = 0
            life -= 1
        enemy_x[i] += enemy_x_change[i]

    if life < 1:
        over_text()
        player_x_change = 0
        player_y_change = 0

    player_x += player_x_change
    player_y += player_y_change
    show_score(text_x, text_y)
    show_life(life_x, life_y)
    screen.blit(player, (player_x, player_y))
    pygame.display.update()
