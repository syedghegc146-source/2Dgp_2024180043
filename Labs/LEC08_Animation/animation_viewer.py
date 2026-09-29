from pico2d import *

# 1. 화면 창 생성 (800x600)

open_canvas(800, 600)


# 2. 스프라이트 시트 이미지 로드

# (LEC08 폴더 안에 이미지 파일이 위치해야 함)

image = load_image('할로우나이트 이밎.webp')


# 3. 애니메이션 정보 설정 (가산점: 애니메이션별 프레임 수 다름 반영)

animations = [

    {"name": "Walk 1", "row": 0, "frames": 9, "width": 100, "height": 100},

    {"name": "Walk 2", "row": 1, "frames": 11, "width": 100, "height": 100},

    {"name": "Jump",   "row": 3, "frames": 12, "width": 100, "height": 100},

    {"name": "Attack", "row": 4, "frames": 11, "width": 100, "height": 100}

]


center_x, center_y = 400, 300  # 화면 중앙 좌표

display_width, display_height = 300, 300  # 확대 출력 크기 (화면 절반 이상)


running = True

anim_index = 0



while running:

    current_anim = animations[anim_index]

    num_frames = current_anim["frames"]

    frame_width = current_anim["width"]

    frame_height = current_anim["height"]

    row = current_anim["row"]



    # 각 애니메이션 5회 반복 재생

    for loop in range(5):

        for frame in range(num_frames):

            clear_canvas()



            # 프레임 좌표 계산

            left = frame * frame_width

            bottom = image.height - ((row + 1) * frame_height)



            # 중앙에 확대 표시

            image.clip_draw(left, bottom, frame_width, frame_height, 

                           center_x, center_y, display_width, display_height)



            update_canvas()

            delay(0.08)



            # 창 닫기 이벤트 처리

            events = get_events()

            for event in events:

                if event.type == SDL_QUIT:

                    running = False

                    break

            if not running:

                break

        if not running:

            break



    if not running:

        break



    # 5회 반복 완료 후 1초간 정지 (마지막 프레임 유지)

    clear_canvas()

    image.clip_draw((num_frames - 1) * frame_width, image.height - ((row + 1) * frame_height), 

                   frame_width, frame_height, center_x, center_y, display_width, display_height)

    update_canvas()

    delay(1.0)



    # 다음 애니메이션으로 순환 (무한 반복)

    anim_index = (anim_index + 1) % len(animations)



close_canvas()