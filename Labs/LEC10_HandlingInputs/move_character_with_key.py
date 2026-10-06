from math import sqrt
from time import perf_counter

from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COUNT = 8
FRAME_DURATION = 0.1
MOVE_SPEED = 300.0

KEYS = {SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT}
IDLE_ROW = {'right': 300, 'left': 200}
MOVE_ROW = {'right': 100, 'left': 0}


def handle_events(events, pressed_keys, facing):
    running = True
    for event in events:
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
    return running, facing


def movement_vector(pressed_keys):
    move_x = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    move_y = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    if move_x and move_y:
        move_x /= sqrt(2)
        move_y /= sqrt(2)
    return move_x, move_y


def move_character(x, y, move_x, move_y, elapsed):
    x += move_x * MOVE_SPEED * elapsed
    y += move_y * MOVE_SPEED * elapsed
    x = min(max(x, FRAME_WIDTH / 2), TUK_WIDTH - FRAME_WIDTH / 2)
    y = min(max(y, FRAME_HEIGHT / 2), TUK_HEIGHT - FRAME_HEIGHT / 2)
    return x, y


def animation_row(is_moving, facing):
    return MOVE_ROW[facing] if is_moving else IDLE_ROW[facing]


def advance_frame(frame, frame_elapsed, elapsed):
    frame_elapsed += elapsed
    while frame_elapsed >= FRAME_DURATION:
        frame = (frame + 1) % FRAME_COUNT
        frame_elapsed -= FRAME_DURATION
    return frame, frame_elapsed


def main():
    open_canvas(TUK_WIDTH, TUK_HEIGHT)
    tuk_ground = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')

    running = True
    pressed_keys = set()
    facing = 'right'
    x, y = TUK_WIDTH / 2, TUK_HEIGHT / 2
    frame = 0
    frame_elapsed = 0.0
    animation_key = None
    previous_time = perf_counter()

    try:
        while running:
            running, facing = handle_events(get_events(), pressed_keys, facing)
            if not running:
                break

            current_time = perf_counter()
            elapsed = current_time - previous_time
            previous_time = current_time

            move_x, move_y = movement_vector(pressed_keys)
            is_moving = move_x != 0 or move_y != 0
            x, y = move_character(x, y, move_x, move_y, elapsed)

            current_animation = ('move' if is_moving else 'idle', facing)
            if current_animation != animation_key:
                frame = 0
                frame_elapsed = 0.0
                animation_key = current_animation

            frame, frame_elapsed = advance_frame(frame, frame_elapsed, elapsed)
            row = animation_row(is_moving, facing)

            clear_canvas()
            tuk_ground.draw(TUK_WIDTH / 2, TUK_HEIGHT / 2)
            character.clip_draw(
                frame * FRAME_WIDTH, row, FRAME_WIDTH, FRAME_HEIGHT, x, y,
            )
            update_canvas()
            delay(1 / 60)
    finally:
        del character
        del tuk_ground
        close_canvas()


if __name__ == '__main__':
    main()
