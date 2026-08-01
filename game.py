import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# --- НАСТРОЙКИ ЭКРАНА ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GRAY = (200, 200, 200)

# --- МАСШТАБИРОВАНИЕ ---
font_size = int(HEIGHT * 0.05)
font = pygame.font.SysFont("arial", font_size, bold=True)
title_font_size = int(HEIGHT * 0.08)
title_font = pygame.font.SysFont("arial", title_font_size, bold=True)

# --- КЛАСС КНОПКИ ---
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, surface):
        # Рисуем кнопку со скругленными углами
        pygame.draw.rect(surface, self.color, self.rect, border_radius=int(HEIGHT*0.02))
        # Текст на кнопке
        text_obj = font.render(self.text, True, WHITE)
        text_rect = text_obj.get_rect(center=self.rect.center)
        surface.blit(text_obj, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- НАСТРОЙКИ ИГРЫ ---
def reset_game():
    global player_x, player_y, player_width, player_height, player_speed
    global object_radius, fall_speed, falling_objects, spawn_delay, last_spawn, score
    
    player_width = int(WIDTH * 0.25)
    player_height = int(HEIGHT * 0.03)
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - int(HEIGHT * 0.1)
    player_speed = int(WIDTH * 0.02)

    object_radius = int(WIDTH * 0.04)
    fall_speed = int(HEIGHT * 0.008)
    falling_objects = []
    spawn_delay = 1000
    last_spawn = pygame.time.get_ticks()
    score = 0

# Игровые переменные
score = 0
game_state = "MENU" # Состояния: MENU, PLAYING, GAME_OVER
clock = pygame.time.Clock()

# Создаем кнопки (центрируем их)
btn_w, btn_h = int(WIDTH*0.5), int(HEIGHT*0.08)
play_btn = Button(WIDTH//2 - btn_w//2, HEIGHT//2 - btn_h//2, btn_w, btn_h, "ИГРАТЬ", GREEN)
restart_btn = Button(WIDTH//2 - btn_w//2, HEIGHT//2 + int(HEIGHT*0.05), btn_w, btn_h, "ЗАНОВО", BLUE)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

reset_game() # Инициализация переменных при старте

# --- ГЛАВНЫЙ ЦИКЛ ---
running = True
while running:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_AC_BACK:
                if game_state == "PLAYING":
                    game_state = "MENU" # Кнопка назад возвращает в меню
                else:
                    running = False
                    
        # Обработка кликов (тапов) по кнопкам
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU" and play_btn.is_clicked(event.pos):
                reset_game()
                game_state = "PLAYING"
            elif game_state == "GAME_OVER" and restart_btn.is_clicked(event.pos):
                reset_game()
                game_state = "PLAYING"

    # --- СОСТОЯНИЕ: МЕНЮ ---
    if game_state == "MENU":
        draw_text("ЛОВИ КРУЖКИ", title_font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        play_btn.draw(screen)
        draw_text("Зеленые - лови, Красные - избегай!", font, GRAY, screen, WIDTH // 2, HEIGHT // 2 + int(HEIGHT*0.15))

    # --- СОСТОЯНИЕ: ИГРА ---
    elif game_state == "PLAYING":
        # Управление (касание)
        if pygame.mouse.get_pressed()[0]:
            mouse_x = mouse_pos[0]
            if mouse_x < player_x + player_width // 2:
                player_x -= player_speed
            if mouse_x > player_x + player_width // 2:
                player_x += player_speed

        if player_x < 0: player_x = 0
        if player_x > WIDTH - player_width: player_x = WIDTH - player_width

        # Спавн объектов
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn > spawn_delay:
            obj_x = random.randint(object_radius, WIDTH - object_radius)
            is_bad = random.random() < 0.3
            color = RED if is_bad else GREEN
            falling_objects.append([obj_x, 0, color, is_bad])
            last_spawn = current_time
            if spawn_delay > 400: spawn_delay -= 5

        # Обновление и столкновения
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obj in falling_objects[:]:
            obj[1] += fall_speed
            obj_rect = pygame.Rect(obj[0] - object_radius, obj[1] - object_radius, object_radius*2, object_radius*2)

            if player_rect.colliderect(obj_rect):
                if obj[3]:
                    game_state = "GAME_OVER"
                else:
                    score += 1
                falling_objects.remove(obj)
            elif obj[1] > HEIGHT + object_radius:
                falling_objects.remove(obj)

        # Отрисовка игры
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height), border_radius=int(HEIGHT*0.01))
        for obj in falling_objects:
            pygame.draw.circle(screen, obj[2], (obj[0], obj[1]), object_radius)
        draw_text(f"Очки: {score}", font, WHITE, screen, WIDTH // 2, int(HEIGHT * 0.05))

    # --- СОСТОЯНИЕ: ПРОИГРЫШ ---
    elif game_state == "GAME_OVER":
        # Рисуем игру на заднем фоне (затемненную)
        pygame.draw.rect(screen, (50, 50, 50), (player_x, player_y, player_width, player_height), border_radius=int(HEIGHT*0.01))
        for obj in falling_objects:
            pygame.draw.circle(screen, (50, 50, 50), (obj[0], obj[1]), object_radius)
            
        # Полупрозрачный фон
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0,0))

        draw_text("ИГРА ОКОНЧЕНА", title_font, RED, screen, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Ваш счет: {score}", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - int(HEIGHT*0.05))
        restart_btn.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()