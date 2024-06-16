import sys
import pygame
import pygame_gui
import random
import json

# Start PyGame environment
pygame.init()

# Game window and game table
dis_width = 900
dis_height = 600
game_width = 600
game_height = 600
W, H = 40, 40  # Размер ячеек в игровом поле
TILE = 15  # Плотность ячеек

# Game Fonts
font_style = pygame.font.SysFont("bahnschrift", 15)  # Шрифт для системных сообщений
score_font = pygame.font.SysFont(None, 22)  # Шрифт для счетчика
score_font1 = pygame.font.SysFont(None, 25)  # Шрифт для счетчика

# Loge size Left side
logo_width = dis_width - game_width
logo_height = (dis_width - game_width) * 334 / 590

# Message position
mes_pos_x = game_width + 15
mes_pos_y = logo_height + 15

# Score position
score_pos_x = game_width + 15
score_pos_y = logo_height + 200

# Game table grid
grid_color = (24, 24, 24)
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# Game data score json
snake_score = "score/snake_score.json"

# Game Colors
white = (255, 255, 255)
yellow = (244, 232, 178)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (49, 140, 231)
lilla = (148, 87, 235)
green = (0, 175, 98)
green2 = (160, 196, 21)
grey = (193, 193, 193)
welcome_bg = (160, 196, 21)
app_bg = black

# Snake settings
snake_block = 15  # шаг змейки
snake_color = green2

# Create Game window
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('SNAKE  >>> OLEG STROGANOV,2024 <<<')  # Добавляем название игры.

# Circle time function set
clock = pygame.time.Clock()

# Init Pygame_gui for input player name at first
MANAGER = pygame_gui.UIManager((dis_width, dis_height))
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 380), (280, 40)), manager=MANAGER,
                                                 object_id="#main_text_entry", placeholder_text="Enter Here!")

def start_game(text_to_show,sound_on):
    gameLoop(text_to_show,sound_on)

def get_user_name():
    sound_on=True
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_s:
                    if sound_on:
                        sound_on = False
                    else:
                        sound_on = True
                    sound_on_off(sound_on)
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                start_game(event.text,sound_on)
                # print(show_text(event.text))

            MANAGER.process_events(event)

        MANAGER.update(UI_REFRESH_RATE)
        dis.fill(welcome_bg)

        logo = pygame.image.load('img/pysnake.png').convert_alpha()
        logo = pygame.transform.scale(logo, (480, 300))
        dis.blit(logo, (200, 30))
        title_font = pygame.font.SysFont(None, 40)  # Шрифт
        name_title = title_font.render("ENTER YOUR NAME:", True, black)
        dis.blit(name_title, [300, 350])

        MANAGER.draw_ui(dis)


        if sound_on:
            vol_button = pygame.image.load('img/sound_on.png').convert_alpha()
        else:
            vol_button = pygame.image.load('img/sound_off.png').convert_alpha()

        sound_font = pygame.font.SysFont('Tahoma', 13, bold=True)  # Шрифт для счетчика
        dis.blit(sound_font.render("'S'- On/Off", True, black), [dis_width - 80, dis_height - 85])
        vol_button = pygame.transform.scale(vol_button, (50, 50))
        # dis.blit(vol_button, (game_width+(dis_width - game_width / 2), dis_width / 2))
        dis.blit(vol_button, (dis_width - 70, dis_height - 70))


        pygame.display.update()

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block], 1)
        # pygame.draw.circle(dis, blue, [x[0], x[1]], snake_radius)

def Your_score(score, speed, player_name, snake_steps):
    value1 = score_font.render(f"{player_name} score: " + str(score), True, black)
    value2 = score_font.render("Snake speed: " + str(speed), True, black)
    value3 = score_font.render("Snake steps: " + str(snake_steps), True, black)
    dis.blit(value1, [mes_pos_x, mes_pos_y])
    dis.blit(value2, [mes_pos_x, mes_pos_y + snake_block])
    dis.blit(value3, [mes_pos_x, mes_pos_y + snake_block * 2])

def game_end(score, speed, player_name, snake_steps):
    value0 = score_font1.render(f"GAME OVER! {player_name}", True, black)
    value0_1 = score_font1.render("Press: Q - Quit / C - Play Again ", True, black)
    value1 = score_font.render("Your Score: " + str(score), True, black)
    value2 = score_font.render("Snake speed: " + str(speed), True, black)
    value3 = score_font.render("Snake steps: " + str(snake_steps), True, black)
    dis.blit(value0, [mes_pos_x, mes_pos_y])
    dis.blit(value0_1, [mes_pos_x, mes_pos_y + snake_block * 6])
    dis.blit(value1, [mes_pos_x, mes_pos_y + snake_block * 2])
    dis.blit(value2, [mes_pos_x, mes_pos_y + snake_block * 3])
    dis.blit(value3, [mes_pos_x, mes_pos_y + snake_block * 4])

def message(msg, color):  # Создадим функцию, которая будет показывать нам сообщения на игровом экране.
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [mes_pos_x, mes_pos_y])

def music():  # sound back ground
    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("sounds/snake.mp3")  # !!!
    pygame.mixer.Channel(0).set_volume(0.2)
    pygame.mixer.Channel(0).play(game_music, -1)

def get_food():  # sound effect
    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("sounds/snake_eat.mp3")  # !!!
    # pygame.mixer.Channel(1).set_volume(0.4)
    pygame.mixer.Channel(1).play(game_music, loops=0)

def get_bonus():  # sound effect
    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("sounds/bonus.mp3")  # !!!
    # pygame.mixer.Channel(2).set_volume(0.4)
    pygame.mixer.Channel(2).play(game_music, loops=0)

def get_step():  # sound effect
    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("sounds/snake_step.wav")  # !!!
    # pygame.mixer.Channel(3).set_volume(0.4)
    pygame.mixer.Channel(3).play(game_music, loops=0)

def get_crash():  # sound effect
    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("sounds/crash.wav")  # !!!
    # pygame.mixer.Channel(4).set_volume(0.4)
    pygame.mixer.Channel(4).play(game_music, loops=0)

def show_score():
    with open('score/snake_score.json', encoding='utf-8') as f:
        data = json.loads(f.read())

    score_font3 = pygame.font.SysFont('Tahoma', 14, bold=True)  # Шрифт для счетчика
    dis.blit(score_font3.render("GAME SCORE (TOP 10)", True, black), [score_pos_x, score_pos_y - snake_block])
    dis.blit(score_font3.render("-----------------------------------------", True, black),
             [score_pos_x, score_pos_y + snake_block / 4])
    mas = []
    for i in data['game_score']:
        line = str(i['name']) + ":" + str(i['score'])
        mas.append(list(map(str, line.split(':'))))

    mas.sort(key=lambda x: int(x[1]), reverse=True)
    k = 1
    if len(mas)<10:
        lines=len(mas)
    else:
        lines=10
    for j in range(lines):
        top_line = str(k) + ": " + mas[j][0] + " : " + mas[j][1]
        score = score_font3.render(top_line, True, black)
        dis.blit(score, [score_pos_x, score_pos_y + k * snake_block / 0.8])
        k += 1

def save_score(player_name, game_score, saved):
    if saved == 0:
        score_data = {"name": f"{player_name}", "score": game_score}
        with open("score/snake_score.json", "r", encoding='utf8') as f:
            data = json.load(f)
            data['game_score'].append(score_data)
            with open("score/snake_score.json", "w", encoding='utf8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=2)
    return saved

def sound_on_off(sound_on=True):
    if sound_on:
        v=0.2
    else:
        v=0
    pygame.mixer.init()
    pygame.mixer.Channel(0).set_volume(v)
    pygame.mixer.Channel(1).set_volume(v)
    pygame.mixer.Channel(2).set_volume(v)
    pygame.mixer.Channel(3).set_volume(v)
    pygame.mixer.Channel(4).set_volume(v)


def gameLoop(player="",sound_on=True):
    # get_user_name()
    sound_on_off(sound_on)

    snake_steps = 0
    game_over = False
    game_close = False

    x1 = game_width / 2  # Указываем начальное значение положения змейки по оси х.
    y1 = game_height / 2  # Указываем начальное значение положения змейки по оси y.
    x1_change = 0  # Создаём переменную, которой в цикле while будут
    # присваиваться значения изменения положения змейки по оси х.
    y1_change = 0  # создаём переменную, которой в цикле while будут
    # присваиваться значения изменения положения змейки по оси y.
    snake_speed = 5  # Скорость змейки
    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, game_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, game_height - snake_block) / snake_block) * snake_block

    bonusx = round(random.randrange(0, game_width - snake_block) / snake_block) * snake_block
    bonusy = round(random.randrange(0, game_height - snake_block) / snake_block) * snake_block

    sbonusx = round(random.randrange(0, game_width - snake_block) / snake_block) * snake_block
    sbonusy = round(random.randrange(0, game_height - snake_block) / snake_block) * snake_block

    player_name = player

    sound_on = True

    while not game_over:


        pygame.display.update()

        while game_close:
            saved = 0
            dis.fill(app_bg)

            [pygame.draw.rect(dis, grid_color, i_rect, 1) for i_rect in grid]  # игровое поле
            pygame.draw.rect(dis, (160, 196, 21),
                             [game_width, 0, dis_width - game_width, dis_height])  # информационное поле
            logo = pygame.image.load('img/pysnake.png').convert_alpha()
            logo = pygame.transform.scale(logo, (logo_width, logo_height))
            dis.blit(logo, (game_width, 0))

            game_end(Length_of_snake, snake_speed, player_name, snake_steps)
            show_score()

            if sound_on:
                vol_button = pygame.image.load('img/sound_on.png').convert_alpha()
            else:
                vol_button = pygame.image.load('img/sound_off.png').convert_alpha()

            sound_font = pygame.font.SysFont('Tahoma', 13, bold=True)  # Шрифт для счетчика
            dis.blit(sound_font.render("'S'- On/Off", True, black), [dis_width - 80, dis_height - 85])
            vol_button = pygame.transform.scale(vol_button, (50, 50))
            # dis.blit(vol_button, (game_width+(dis_width - game_width / 2), dis_width / 2))
            dis.blit(vol_button, (dis_width - 70, dis_height - 70))
            pygame.display.update()
            # gameLoop(player=player_name)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        save_score(player_name, Length_of_snake - 1, saved)
                    if event.key == pygame.K_c:
                        snake_steps = 0
                        save_score(player_name, Length_of_snake - 1, saved)
                        get_user_name()
                    if event.key == pygame.K_s:
                        if sound_on:
                            sound_on=False
                        else:
                            sound_on=True
                        sound_on_off(sound_on)
                elif event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:  # Добавляем считывание направления движений с клавиатуры.
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                if event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                if event.key == pygame.K_s:
                    if sound_on:
                        sound_on = False
                    else:
                        sound_on = True
                    sound_on_off(sound_on)
                if event.key != pygame.K_s:
                    snake_steps += 1

        if snake_steps > 0:
            snake_steps += 1

        if x1 > game_width - snake_block or x1 < 0 or y1 > game_height - snake_block or y1 < 0:
            get_crash()
            game_close = True  # если координаты змейки выходят за рамки поля, то игра должна закончиться.

        x1 += x1_change  # Записываем новое значение положения змейки по оси х.
        y1 += y1_change  # Записываем новое значение положения змейки по оси y.

        dis.fill(app_bg)
        [pygame.draw.rect(dis, grid_color, i_rect, 1) for i_rect in grid]  # игровое поле

        if Length_of_snake == 1 and player_name == "":
            get_user_name()

        # информационное поле
        pygame.draw.rect(dis, (160, 196, 21), [game_width, 0, dis_width - game_width, dis_height])
        logo = pygame.image.load('img/pysnake.png').convert_alpha()
        logo = pygame.transform.scale(logo, (logo_width, logo_height))
        dis.blit(logo, (game_width, 0))
        show_score()

        if sound_on:
            vol_button = pygame.image.load('img/sound_on.png').convert_alpha()
        else:
            vol_button = pygame.image.load('img/sound_off.png').convert_alpha()

        sound_font = pygame.font.SysFont('Tahoma', 13, bold=True)  # Шрифт для счетчика
        dis.blit(sound_font.render("'S'- On/Off", True, black), [dis_width - 80, dis_height - 85])
        vol_button = pygame.transform.scale(vol_button, (50, 50))
        # dis.blit(vol_button, (game_width+(dis_width - game_width / 2), dis_width / 2))
        dis.blit(vol_button, (dis_width - 70, dis_height - 70))

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])  # EDA
        if (snake_speed % 4 == 0) and (Length_of_snake > 4):
            pygame.draw.rect(dis, lilla, [bonusx, bonusy, snake_block, snake_block])  # boonus speed
        if (snake_speed % 10 == 0) and (Length_of_snake > 10):
            pygame.draw.rect(dis, green, [sbonusx, sbonusy, snake_block, snake_block])  # super boonus speed

        snake_Head = []  # длина змейки при движениях
        snake_Head.append(x1)  # добавляем при движении по х
        snake_Head.append(y1)  # добавляем при движении по y
        snake_List.append(snake_Head)  # добавляем при движении по y
        get_step()

        if len(snake_List) > Length_of_snake:
            del snake_List[0]  # удаляем первый элемент змейки, чтобы она не увеличивалась при движении

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1, snake_speed, player_name, snake_steps)
        pygame.display.update()

        if x1 == bonusx and y1 == bonusy:
            snake_speed -= 1
            get_bonus()
        if x1 == sbonusx and y1 == sbonusy:
            snake_speed -= 3
            get_bonus()

        if x1 == foodx and y1 == foody:
            get_food()
            foodx = round(random.randrange(0, game_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, game_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            if Length_of_snake % 2 == 0:
                snake_speed += 1
        clock.tick(snake_speed)
    pygame.quit()
    quit()

music()
gameLoop()
