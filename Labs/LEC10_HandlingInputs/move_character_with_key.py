from math import sqrt
from time import perf_counter

from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COUNT = 8
FRAME_DURATION = 0.1
MOVE_SPEED = 300.0

open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

KEYS = {SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT}
IDLE_ROW = {'right': 300, 'left': 200}
MOVE_ROW = {'right': 100, 'left': 0}

running = True
pressed_keys = set()
facing = 'right'
x, y = TUK_WIDTH / 2, TUK_HEIGHT / 2
frame = 0
frame_elapsed = 0.0
animation_key = None
previous_time = perf_counter()


def handle_events():
    global running, facing

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in KEYS:
                pressed_keys.add(event.key)
                if event.key == SDLK_LEFT:
                    facing = 'left'
                elif event.key == SDLK_RIGHT:
                    facing = 'right'
        elif event.type == SDL_KEYUP and event.key in KEYS:
            pressed_keys.discard(event.key)


while running:
    handle_events()
    if not running:
        break

    current_time = perf_counter()
    elapsed = current_time - previous_time
    previous_time = current_time

    move_x = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    move_y = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    is_moving = move_x != 0 or move_y != 0

    if move_x and move_y:
        move_x /= sqrt(2)
        move_y /= sqrt(2)

    x += move_x * MOVE_SPEED * elapsed
    y += move_y * MOVE_SPEED * elapsed
    x = min(max(x, FRAME_WIDTH / 2), TUK_WIDTH - FRAME_WIDTH / 2)
    y = min(max(y, FRAME_HEIGHT / 2), TUK_HEIGHT - FRAME_HEIGHT / 2)

    current_animation = ('move' if is_moving else 'idle', facing)
    if current_animation != animation_key:
        frame = 0
        frame_elapsed = 0.0
        animation_key = current_animation

    frame_elapsed += elapsed
    while frame_elapsed >= FRAME_DURATION:
        frame = (frame + 1) % FRAME_COUNT
        frame_elapsed -= FRAME_DURATION

    row = MOVE_ROW[facing] if is_moving else IDLE_ROW[facing]

    clear_canvas()
    tuk_ground.draw(TUK_WIDTH / 2, TUK_HEIGHT / 2)
    character.clip_draw(
        frame * FRAME_WIDTH, row, FRAME_WIDTH, FRAME_HEIGHT, x, y,
    )
    update_canvas()
    delay(1 / 60)

del character
del tuk_ground
close_canvas()
