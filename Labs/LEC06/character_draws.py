from pico2d import *
import math

# 맨처음 해야할 일
open_canvas(800, 600)
character = load_image('character.png')


def move_circle():
    print('CIRCLE')
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
    # 캐릭터 이미지 표시
        clear_canvas()
        character.draw(400, 300)
        update_canvas()
        delay(0.01)
    pass 

def draw_top():
    print('top')
    for x in range(100, 700, 2):
        clear_canvas()
        character.draw(x, 500)
        update_canvas()
        delay(0.01) 
    pass

def draw_bottom():
    print('bottom')
    for x in range(100, 700, 2):
        clear_canvas()
        character.draw(x, 100)
        update_canvas()
        delay(0.01)
    pass

def draw_Left():
    print('Lift')
    pass

def draw_Right():
    print('Right')
    for y in range(100, 500, 2):
        clear_canvas()
        character.draw(700, y)
        update_canvas()
        delay(0.01)
    pass

def move_rectangle():
    print('RECTANGLE')
    draw_top()
    draw_bottom()
    draw_Left()
    draw_Right()
    pass

def move_triangle():
    print('TRIANGLE')
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()

