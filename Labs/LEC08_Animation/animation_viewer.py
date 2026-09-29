from pico2d import *

# 1. 800x600 해상도의 그래픽 창 생성
open_canvas(800, 600)

# 2. 스프라이트 시트 이미지 로드 (배경을 투명 처리한 png)
IMAGE_FILE = 'character_sheet.png'
image = load_image(IMAGE_FILE)

# 3. 스프라이트 시트 구조 정보
#    시트는 144x144 칸의 격자 위에 캐릭터가 그려져 있지만,
#    프레임마다 실제 캐릭터 크기가 달라서 프레임별로 (left, top, width, height)를 따로 저장한다.
SHEET_ORIGIN_X = 528   # 첫 번째 칸의 왼쪽 x (이미지 왼쪽 기준)
SHEET_ORIGIN_Y = 24    # 첫 번째 행의 위쪽 y (이미지 위쪽 기준)
CELL_SIZE = 144        # 한 칸의 크기

# 4. 애니메이션 메타데이터 (애니메이션마다 프레임 수와 프레임 크기가 다름)
animations = [
    {
        "name": "Walk2", "row": 5,
        "frames": [   # (left, top, width, height)
            (559, 792, 57, 96),
            (701, 784, 63, 104),
            (841, 784, 75, 104),
            (985, 792, 72, 96),
            (1129, 784, 78, 104),
            (1273, 784, 71, 104),
        ],
    },
    {
        "name": "Run2", "row": 3,
        "frames": [
            (544, 504, 80, 96),
            (704, 504, 56, 96),
            (825, 504, 87, 96),
            (976, 504, 87, 96),
            (1136, 504, 56, 96),
            (1257, 504, 87, 96),
        ],
    },
    {
        "name": "Roll", "row": 2,
        "frames": [
            (544, 362, 88, 94),
            (697, 392, 78, 64),
            (839, 400, 82, 56),
            (985, 378, 79, 78),
            (1127, 393, 80, 63),
            (1271, 384, 64, 72),
        ],
    },
    {
        "name": "Jump attack", "row": 0,
        "frames": [
            (544, 80, 87, 88),
            (684, 80, 76, 88),
            (840, 73, 104, 95),
            (985, 57, 119, 102),
            (1123, 72, 85, 88),
            (1273, 80, 80, 88),
        ],
    },
    {
        "name": "Pull up", "row": 1,
        "frames": [
            (535, 208, 72, 103),
            (688, 224, 70, 88),
            (848, 219, 72, 91),
            (993, 224, 70, 87),
            (1144, 224, 63, 87),
            (1295, 224, 70, 86),
        ],
    },
    {
        "name": "Sit down", "row": 4,
        "frames": [
            (537, 648, 84, 96),
            (692, 657, 83, 87),
            (842, 672, 79, 74),
            (980, 657, 83, 87),
        ],
    },
]

# 5. 화면 중앙 표시 및 확대 출력 설정
center_x = 400         # 화면 중앙 x
base_y = 90            # 캐릭터 발 위치(화면 아래에서 90px)
scale = 4              # 확대 배율 (캐릭터 높이가 화면의 절반 이상)

REPEAT_COUNT = 5       # 각 애니메이션 반복 횟수
FRAME_DELAY = 0.1      # 프레임 사이 대기 시간(재생 속도 조절)
PAUSE_TIME = 1.0       # 5회 반복 후 정지 시간


def check_quit():
    """창 닫기 이벤트 확인"""
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
    return False


def draw_frame(anim, frame_index):
    """현재 애니메이션의 frame_index번째 프레임을 화면 중앙에 확대 출력"""
    left, top, width, height = anim["frames"][frame_index]

    # pico2d는 y가 아래에서 위로 증가하므로 bottom 좌표로 변환
    bottom = image.h - (top + height)

    # 칸 안에서 캐릭터가 차지하는 위치를 유지해 움직임(점프, 구르기)이 자연스럽게 보이도록 보정
    col = (left + width // 2 - SHEET_ORIGIN_X) // CELL_SIZE
    cell_center_x = SHEET_ORIGIN_X + col * CELL_SIZE + CELL_SIZE // 2
    cell_bottom_y = SHEET_ORIGIN_Y + (anim["row"] + 1) * CELL_SIZE

    offset_x = (left + width / 2 - cell_center_x) * scale
    offset_y = (cell_bottom_y - (top + height)) * scale

    draw_x = center_x + offset_x
    draw_y = base_y + offset_y + height * scale / 2

    image.clip_draw(left, bottom, width, height,
                    draw_x, draw_y, width * scale, height * scale)


running = True
anim_index = 0

while running:
    anim = animations[anim_index]
    frame_count = len(anim["frames"])

    # 각 애니메이션 5회 반복 재생
    for loop in range(REPEAT_COUNT):
        for frame_index in range(frame_count):
            clear_canvas()
            draw_frame(anim, frame_index)
            update_canvas()
            delay(FRAME_DELAY)

            if check_quit():
                running = False
                break
        if not running:
            break

    if not running:
        break

    # 5회 반복 후 마지막 프레임을 유지한 채 1초 정지
    clear_canvas()
    draw_frame(anim, frame_count - 1)
    update_canvas()
    delay(PAUSE_TIME)

    # 다음 애니메이션으로 순환 (무한 반복)
    anim_index = (anim_index + 1) % len(animations)

# 자원 해제 및 안전 종료
del image
close_canvas()