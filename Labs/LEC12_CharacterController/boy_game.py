from pico2d import *

from grass import Grass
from boy import Boy

pressed_keys = set()


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.start_auto_run()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            pressed_keys.discard(event.key)


def reset_world():
    global world
    global boy

    world = []
    pressed_keys.clear()

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)


def update_world():
    direction = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    boy.set_direction(direction)
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
