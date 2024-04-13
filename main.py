import pygame
import random
import json
import sys
from datetime import datetime, timedelta
import pygame_textinput

pygame.init()  # Инициализация всех импортированных модулей pygame

# Основные настройки экрана и игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Установка размера окна игры
pygame.display.set_caption("Игра Тир")  # Название окна
icon = pygame.image.load("img/pic.png")  # Загрузка иконки окна
pygame.display.set_icon(icon)  # Установка иконки окна
target_img = pygame.image.load("img/target.png")  # Загрузка изображения цели
target_width, target_height = target_img.get_size()  # Получение размеров изображения цели

# Настройки шрифтов и цвета
FONT = pygame.font.Font(None, 36)  # Определение шрифта обычного текста
BIG_FONT = pygame.font.Font(None, 72)  # Определение шрифта для большого текста
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройки игры и счета
game_settings = {'difficulty': 1, 'game_duration': 60}  # Настройки сложности и продолжительности игры
move_times = {1: 5, 2: 3, 3: 1}  # Задержка перед перемещением цели
game_times = {1: 60, 2: 120, 3: 180, 4: 300, 5: 600}  # Время игры в секундах
score = 0  # Игровой счет
last_hit_message = None  # Сообщение о последнем попадании или промахе
last_hit_message_time = None  # Время отображения последнего сообщения

# Компонент для текстового ввода
text_input = pygame_textinput.TextInputVisualizer()


def load_leaderboard():
    # Загрузка рейтинга из файла JSON
    try:
        with open('leaderboard.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_leaderboard(name, scores, difficulty):
    # Сохранение данных игрока в рейтинг
    leaderboard = load_leaderboard()
    leaderboard.append({
        'name': name,
        'score': scores,
        'date': datetime.now().isoformat(),
        'difficulty': difficulty  # Добавление сложности в данные
    })
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file)


def draw_text(text, font, color, x, y):
    # Функция для отображения текста на экране
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)


def show_start_screen():
    options = ["1: Легкая - 5 сек", "2: Нормальная - 3 сек", "3: Сложная - 1 сек"]
    time_options = ["1: 1 мин", "2: 2 мин", "3: 3 мин", "4: 5 мин", "5: 10 мин"]
    selected_option = 0
    selected_time = 0
    choosing_difficulty = True
    choosing_time = False

    while choosing_difficulty:
        screen.fill(BLACK)
        draw_text("Выберите сложность:", FONT, WHITE, SCREEN_WIDTH / 2, 50)
        for i, option in enumerate(options):
            if i == selected_option:
                draw_text(f"> {option}", FONT, GREEN, SCREEN_WIDTH / 2, 150 + i * 50)
            else:
                draw_text(option, FONT, WHITE, SCREEN_WIDTH / 2, 150 + i * 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_option > 0:
                    selected_option -= 1
                elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                    selected_option += 1
                elif event.key == pygame.K_RETURN:
                    game_settings['difficulty'] = move_times[selected_option + 1]
                    choosing_difficulty = False
                    choosing_time = True

    while choosing_time:
        screen.fill(BLACK)
        draw_text("Выберите время игры:", FONT, WHITE, SCREEN_WIDTH / 2, 50)
        for i, option in enumerate(time_options):
            if i == selected_time:
                draw_text(f"> {option}", FONT, GREEN, SCREEN_WIDTH / 2, 150 + i * 50)
            else:
                draw_text(option, FONT, WHITE, SCREEN_WIDTH / 2, 150 + i * 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_time > 0:
                    selected_time -= 1
                elif event.key == pygame.K_DOWN and selected_time < len(time_options) - 1:
                    selected_time += 1
                elif event.key == pygame.K_RETURN:
                    game_settings['game_duration'] = game_times[selected_time + 1]
                    choosing_time = False

    start_game()


def start_game():
    # Начало игрового процесса, настройка и инициализация начальных параметров
    global score, last_hit_message, last_hit_message_time
    score = 0
    last_hit_message = None
    last_hit_message_time = None
    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(0, SCREEN_HEIGHT - target_height)
    start_time = datetime.now()
    next_move_time = start_time + timedelta(seconds=game_settings['difficulty'])

    while True:
        screen.fill((200, 200, 200))
        screen.blit(target_img, (target_x, target_y))
        current_time = datetime.now()

        if current_time >= next_move_time:
            target_x = random.randint(0, SCREEN_WIDTH - target_width)
            target_y = random.randint(0, SCREEN_HEIGHT - target_height)
            next_move_time += timedelta(seconds=game_settings['difficulty'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if target_x <= mouse_x <= target_x + target_width and target_y <= mouse_y <= target_y + target_height:
                    score += 1
                    last_hit_message = "АЙ!"
                    last_hit_message_time = current_time + timedelta(seconds=0.5)
                    target_x = random.randint(0, SCREEN_WIDTH - target_width)
                    target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                else:
                    score -= 1
                    last_hit_message = "Мимо!"
                    last_hit_message_time = current_time + timedelta(seconds=0.5)

        if last_hit_message and current_time <= last_hit_message_time:
            message_color = GREEN if last_hit_message == "АЙ!" else RED
            draw_text(last_hit_message, FONT, message_color,
                      target_x - 40 if last_hit_message == "АЙ!" else target_x + target_width + 10, target_y)

        elapsed_time = (current_time - start_time).seconds
        draw_text(f'Время: {game_settings['game_duration'] - elapsed_time}', FONT, BLACK, 70, 30)
        draw_text(f'Очки: {score}', FONT, BLACK, SCREEN_WIDTH - 70, 30)
        pygame.display.update()

        if elapsed_time >= game_settings['game_duration']:
            end_game()


def end_game():
    # Завершение игры и ввод имени пользователя
    screen.fill(BLACK)
    draw_text(f'Игра окончена! Ваш счет: {score}', BIG_FONT, WHITE, SCREEN_WIDTH / 2, 100)
    draw_text("Введите ваше имя:", FONT, WHITE, SCREEN_WIDTH / 2, 200)
    name = ""
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    save_leaderboard(name, score, game_settings['difficulty'])
                    show_leaderboard(game_settings['difficulty'])
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(BLACK, (0, 250, SCREEN_WIDTH, 50))
        draw_text(name, FONT, WHITE, SCREEN_WIDTH / 2, 250)
        pygame.display.update()


def show_leaderboard(current_difficulty):
    # Отображение лидерборда по выбранной сложности
    leaderboard = load_leaderboard()
    filtered_leaderboard = [entry for entry in leaderboard if entry['difficulty'] == current_difficulty]
    filtered_leaderboard.sort(key=lambda x: x['score'], reverse=True)
    filtered_leaderboard = filtered_leaderboard[:10]

    screen.fill(BLACK)
    draw_text("ТОП 10 игроков на сложности: {}".format(current_difficulty), BIG_FONT, WHITE, SCREEN_WIDTH / 2, 50)
    for idx, entry in enumerate(filtered_leaderboard):
        draw_text(f'{idx + 1}. {entry["name"]} - {entry["score"]}', FONT, WHITE, SCREEN_WIDTH / 2, 150 + idx * 30)
    pygame.display.update()
    pygame.time.wait(5000)  # Показываем лидерборд в течение 5 секунд, затем выходим
    pygame.quit()
    sys.exit()


show_start_screen()
