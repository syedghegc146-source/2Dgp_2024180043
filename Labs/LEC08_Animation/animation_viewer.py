from pico2d import *
 
# 1. 화면 창 생성 (800x600)
open_canvas(800, 600)
 
# 2. 스프라이트 시트 이미지 로드
# 파일명은 영문 png 권장 (실제 파일명과 정확히 일치해야 함)
IMAGE_FILE = 'hollow_knight.png'
image = load_image(IMAGE_FILE)
 
# 3. 애니메이션 정보 (애니메이션별 프레임 수 다름)
animations = [
    {"name": "Walk 1", "row": 0, "frames": 9,  "width": 100, "height": 100},
    {"name": "Walk 2", "row": 1, "frames": 11, "width": 100, "height": 100},
    {"name": "Jump",   "row": 3, "frames": 12, "width": 100, "height": 100},
    {"name": "Attack", "row": 4, "frames": 11, "width": 100, "height": 100},
]
 
center_x, center_y = 400, 300              # 화면 중앙 좌표
display_width, display_height = 300, 300   # 확대 출력 크기
 
 
def check_quit():
    """창 닫기 이벤트 확인"""
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
    return False
 
 
def draw_frame(anim, frame):
    """스프라이트 시트에서 해당 프레임을 잘라 중앙에 확대 출력"""
    fw, fh = anim["width"], anim["height"]
    left = frame * fw
    bottom = image.h - ((anim["row"] + 1) * fh)  # pico2d는 image.h 사용
    image.clip_draw(left, bottom, fw, fh,
                    center_x, center_y, display_width, display_height)
 
 
running = True
anim_index = 0
 
while running:
    anim = animations[anim_index]
 
    # 각 애니메이션 5회 반복 재생
    for loop in range(5):
        for frame in range(anim["frames"]):
            clear_canvas()
            draw_frame(anim, frame)
            update_canvas()
            delay(0.08)
 
            if check_quit():
                running = False
                break
        if not running:
            break
 
    if not running: 
        break
 
    # 5회 반복 완료 후 1초간 정지 (마지막 프레임 유지)
    clear_canvas()
    draw_frame(anim, anim["frames"] - 1)
    update_canvas()
    delay(1.0)
 
    # 다음 애니메이션으로 순환 (무한 반복)
    anim_index = (anim_index + 1) % len(animations)
 
# 자원 해제
del image
close_canvas()
 