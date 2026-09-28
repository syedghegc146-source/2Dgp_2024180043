# 실습 과제 진행
from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('character.png')

grass.draw(400, 30) 
character.draw(400, 90)
update_canvas()

x = 0
while x < 800:
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, 90)
    update_canvas()
    x += 2
    delay(0.01)
    
delay(5)
close_canvas()