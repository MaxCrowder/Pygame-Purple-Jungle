import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Purple Jungle')
WINDOW_SIZE = (1280, 720)
WIN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((640, 360))


isRight = False
isLeft = False
isJump = False
y_velocity = 0
jumpClock = 0
true_scroll = [0, 0]


def load_map(path):
    game_map = []
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')

    for row in data:
        game_map.append(list(row))
    return game_map


animation_frames = {}


def load_animation(path, frame_rate):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_rate:
        frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_frames[frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


database = {'run': load_animation('animations/run', [5, 5, 5, 5, 5, 5, 5]),
            'idle': load_animation('animations/idle', [5, 5, 5, 5, 5, 5, 5, 5]),
            'jump': load_animation('animations/jump', [5, 5, 5, 5, 5, 5, 5, 5])}

game_map = load_map('assets/map')
platform1 = pygame.image.load('assets/top.png')
platform2 = pygame.image.load('assets/bottom.png')
bg1 = pygame.image.load('assets/background1.png')
bg2 = pygame.image.load('assets/background2.png')
bg3 = pygame.image.load('assets/background3.png')
bg4 = pygame.image.load('assets/background4.png')


player_action = ''
player_frame = 0
reverse = False

player_rect = pygame.Rect(160, 100, 31, 50)
background_objects = [
                    [0.25, [0, 0, 0, 0]],
                    [0.25, [640, 0, 0, 0]],
                    [0.25, [1280, 0, 0, 0]],
                    [0.25, [1920, 0, 0, 0]],
                    [0.25, [2560, 0, 0, 0]],
                    [0.5, [0, 0, 0, 0]],
                    [0.5, [640, 0, 0, 0]],
                    [0.5, [1280, 0, 0, 0]],
                    [0.5, [1920, 0, 0, 0]],
                    [0.5, [2560, 0, 0, 0]],
                    [0.75, [0, 0, 0, 0]],
                    [0.75, [640, 0, 0, 0]],
                    [0.75, [1280, 0, 0, 0]],
                    [0.75, [1920, 0, 0, 0]],
                    [0.75, [2560, 0, 0, 0]],
                    [1, [0, 0, 0, 0]],
                    [1, [640, 0, 0, 0]],
                    [1, [1280, 0, 0, 0]],
                    [1, [1920, 0, 0, 0]],
                    [1, [2560, 0, 0, 0]],
                    [1, [3200, 0, 0, 0]]]


def collision_test(rect, tiles):
    hit_list = []
    for t in tiles:
        if rect.colliderect(t):
            hit_list.append(t)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for t in hit_list:
        if movement[0] > 0:
            rect.right = t.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = t.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for t in hit_list:
        if movement[1] > 0:
            rect.bottom = t.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = t.bottom
            collision_types['top'] = True
    return rect, collision_types


while True:  # game loop

    display.fill((243, 229, 245))

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])

    # Parallax
    for obj in background_objects:
        obj_rect = pygame.Rect(obj[1][0] - scroll[0] * obj[0], obj[1][1] - scroll[1] * obj[0], obj[1][2], obj[1][3])
        if obj[0] == 1:
            display.blit(bg1, obj_rect)
        elif obj[0] == 0.75:
            display.blit(bg2, obj_rect)
        elif obj [0] == 0.5:
            display.blit(bg3, obj_rect)
        else:
            display.blit(bg4, obj_rect)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(platform2, (x*32-scroll[0], y*32-scroll[1]))
            if tile == '2':
                display.blit(platform1, (x*32-scroll[0], y*32-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*32, y*32, 32, 32))
            x += 1
        y += 1

    player_movement = [0, 0]
    if isRight:
        player_movement[0] += 3
        reverse = False
        if isJump:
            player_action, player_frame = change_action(player_action, player_frame, 'jump')
        else:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
    elif isLeft:
        player_movement[0] -= 3
        reverse = True
        if isJump:
            player_action, player_frame = change_action(player_action, player_frame, 'jump')
        else:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
    else:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    player_movement[1] += y_velocity
    y_velocity += 0.2
    if y_velocity > 6:
        y_velocity = 6

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        jumpClock = 0
        isJump = False
        y_velocity = 0
    else:
        jumpClock += 1

    player_frame += 1
    if player_frame >= len(database[player_action]):
        player_frame = 0
    player_img_id = database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, reverse, False),
                 (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                isRight = True
            if event.key == K_LEFT:
                isLeft = True
            if event.key == K_SPACE:
                isJump = True
                if jumpClock < 6:
                    y_velocity = -6

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                isRight = False
            if event.key == K_LEFT:
                isLeft = False

    WIN.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(120)
