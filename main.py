import os
import sys
import copy
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name).replace("\\", "/")
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def set_colorkey(colorkey):
    if colorkey is not None:
        image = player_image1.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = player_image1.convert_alpha()
    return image


def load_level(filename):
    '''filename = "data/" + filename'''
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


pygame.init()
pygame.display.set_caption('Лабиринт')
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
fps = 50
clock = pygame.time.Clock()
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image1 = load_image('luigi.png')
player_image2 = load_image('mar.png')
level_name = ''
player_images = [player_image2, player_image1]
second_playerCoords = []
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flag = False


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    global player_images

    def __init__(self, pos_x, pos_y, second_player=False):
        super().__init__(player_group, all_sprites)
        self.image = player_image2
        if second_player:
            self.image = player_image1
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def check_levelbutton(mouse_pos):
    x, y = list(map(int, mouse_pos))
    if 210 < x < 360 and 475 < y < 525:
        return '1'
    elif 420 < x < 570 and 475 < y < 525:
        return '2'
    elif 630 < x < 780 and 475 < y < 525:
        return '3'
    elif 398 < x < 602 and 900 < y < 950:
        return '4'
    return None


def generate_level(level):
    global second_playerCoords
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'F':
                Tile('empty', x, y)
                Player(x, y, True)
                second_playerCoords = [y, x]
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Лабиринт", "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "Для старта нажмите любую кнопку"
                  ]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("arial black", 45)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def history():
    intro_text = ["Казалось, что Марио и Йоши никогда не разлучить,",
                  "но злому магу не нравился их союз.",
                  "Он решил разделить их и построил между ними ",
                  "высочайшие стены, каких еще никто не строил",
                  "и даже не видывал",
                  "Помогите Йоши и Марио встретиться: найдите",
                  "лазейки в стенах злого мага и ",
                  "устройте встречу друзей.",
                  "Вы Марио, и ваша задача во что бы то ни стало",
                  "воссоединиться со своим другом Йоши",
                  "Ни за что не забывайте про него, и не потеряйтесь сами",
                  "Пройдите лабиринт и дойдите до своего",
                  "товарища"
                  ]
    fon = pygame.transform.scale(load_image('changelevelfon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("arial black", 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.rect(screen, pygame.Color('black'), (100, 900, 200, 50), 1)
    font = pygame.font.SysFont("arial black", 30)
    to_main_menu = font.render('Вернуться', 1, pygame.Color('black'))
    screen.blit(to_main_menu, (100, 900))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = list(map(int, event.pos))
                if 100 < x < 300 and 900 < y < 950:
                    change_level()


def change_level():
    global level_name, flag
    pygame.init()
    intro_text = ["Выберите уровень", "",
                  ]
    fon = pygame.transform.scale(load_image('changelevelfon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("arial black", 50)
    text_coord = 50
    for x in range(1, 4):
        pygame.draw.rect(screen, pygame.Color('black'), (210 * x, 475, 150, 50), 1)
        font = pygame.font.SysFont("times new roman", 35)
        level_number = font.render('Уровень ' + str(x), 1, pygame.Color('black'))
        screen.blit(level_number, (210 * x, 475))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.rect(screen, pygame.Color('black'), (398, 900, 204, 50), 1)
    history_text = font.render('Предыстория', 1, pygame.Color('black'))
    screen.blit(history_text, (398, 900))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                a = check_levelbutton(event.pos)
                if a == '1':
                    level_name = os.path.join('data', 'gamelevel1.txt')
                    return
                elif a == '2':
                    level_name = os.path.join('data', 'gamelevel2.txt')
                    return
                elif a == '3':
                    level_name = os.path.join('data', 'gamelevel3.txt')
                    return
                elif a == '4':
                    history()
        pygame.display.flip()
        clock.tick(fps)


def win_window():
    intro_text = ["Друзья снова вместе!", "",
                  ]
    fon = pygame.transform.scale(load_image('finalfon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("arial black", 32)
    text_coord = 50
    pygame.draw.rect(screen, pygame.Color('white'), (50, 850, 300, 50), 1)
    leave_to_main_menu = font.render('Выйти в начало', 1, pygame.Color('white'))
    screen.blit(leave_to_main_menu, (50, 850))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = list(map(int, event.pos))
                if 50 < x < 350 and 850 < y < 900:
                    terminate()
                else:
                    pass

        pygame.display.flip()
        clock.tick(fps)


def move_in_map(player, dx, dy, level_map, level_x, level_y):
    pos_x = player.pos_x + dx
    pos_y = player.pos_y + dy
    if (0 <= pos_x <= level_x and 0 <= pos_y <= level_y and
            level_map[pos_y][pos_x] == '.'):
        player.move(pos_x, pos_y)
        level_map[pos_y][pos_x] = '@'
        level_map[pos_y - dy][pos_x - dx] = '.'


def main():
    pygame.init()
    start_screen()
    change_level()
    level_map = load_level(level_name)
    a = copy.deepcopy(level_map)
    player, level_x, level_y = generate_level(level_map)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                move_in_map(player, 0, -1, a, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                move_in_map(player, 0, 1, a, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                move_in_map(player, -1, 0, a, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                move_in_map(player, 1, 0, a, level_x, level_y)
        screen.fill((255, 255, 255))
        tiles_group.draw(screen)
        player_group.draw(screen)
        if [second_playerCoords[0], second_playerCoords[1] - 1] == [player.pos_y, player.pos_x]:
            win_window()
        elif [second_playerCoords[0], second_playerCoords[1] + 1] == [player.pos_y, player.pos_x]:
            win_window()
        elif [second_playerCoords[0] - 1, second_playerCoords[1]] == [player.pos_y, player.pos_x]:
            win_window()
        elif [second_playerCoords[0] + 1, second_playerCoords[1] + 1] == [player.pos_y, player.pos_x]:
            win_window()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


main()
