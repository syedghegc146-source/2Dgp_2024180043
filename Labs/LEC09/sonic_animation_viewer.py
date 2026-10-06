from time import perf_counter

from pico2d import *


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
SPRITE_FILE = 'sonic-sprite.png'
SCALE = 4
FRAME_DELAY = 0.1
REPEAT_COUNT = 5
PAUSE_TIME = 1.0
GROUND_Y = 115
MOVE_SPEED = 180.0
JUMP_HEIGHT = 90
FPS = 60


# Frame rectangles use (left, top, width, height) with a top-left image origin.
# Positions and dimensions were measured from the transparent sprite pixels.
ANIMATIONS = [
    {
        'name': '동작 01', 'moving': True, 'jump': False,
        'frames': [
            (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
            (86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
            (182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 38),
            (270, 45, 24, 32), (302, 51, 29, 26),
        ],
    },
    {
        'name': '동작 02', 'moving': True, 'jump': False,
        'frames': [
            (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
            (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
            (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
            (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
        ],
    },
    {
        'name': '동작 03', 'moving': True, 'jump': False,
        'frames': [
            (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
            (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
        ],
    },
    {
        'name': '동작 04', 'moving': True, 'jump': False,
        'frames': [
            (1, 169, 29, 30), (36, 167, 28, 31), (67, 169, 30, 29),
            (98, 170, 31, 28), (131, 168, 29, 30), (162, 168, 29, 31),
            (193, 170, 30, 29), (230, 170, 31, 28), (268, 170, 30, 30),
        ],
    },
    {
        'name': '동작 05', 'moving': True, 'jump': False,
        'frames': [
            (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
            (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
        ],
    },
    {
        'name': '동작 06', 'moving': True, 'jump': False,
        'frames': [
            (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
            (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
        ],
    },
    {
        'name': '동작 07', 'moving': True, 'jump': False,
        'frames': [
            (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
            (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 33),
        ],
    },
    {
        'name': '동작 08', 'moving': True, 'jump': True,
        'frames': [
            (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
            (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
            (184, 341, 40, 28), (232, 341, 39, 27),
        ],
    },
    {
        'name': '동작 09', 'moving': False, 'jump': False,
        'frames': [
            (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
            (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
            (217, 379, 33, 36), (254, 378, 33, 36),
        ],
    },
    {
        'name': '동작 10', 'moving': False, 'jump': False,
        'frames': [
            (6, 429, 34, 40), (49, 426, 34, 43),
            (96, 427, 23, 39), (125, 427, 23, 39),
        ],
    },
]


def validate_animations(animations, image_width, image_height):
    """Reject incomplete animation data and frames outside the sprite sheet."""
    if len(animations) != 10:
        raise ValueError(f'동작은 10개여야 합니다: {len(animations)}개')

    frame_total = sum(len(animation['frames']) for animation in animations)
    if frame_total != 76:
        raise ValueError(f'프레임은 총 76개여야 합니다: {frame_total}개')

    moving_total = sum(animation['moving'] for animation in animations)
    if moving_total != 8:
        raise ValueError(f'이동 동작은 8개여야 합니다: {moving_total}개')

    for animation in animations:
        if not animation['frames']:
            raise ValueError(f"{animation['name']}에 프레임이 없습니다")
        for frame in animation['frames']:
            left, top, width, height = frame
            if (left < 0 or top < 0 or width <= 0 or height <= 0
                    or left + width > image_width
                    or top + height > image_height):
                raise ValueError(f"{animation['name']}의 프레임 좌표가 이미지 범위를 벗어납니다: {frame}")


def move_horizontally(position, direction, elapsed, speed, left_edge, right_edge):
    """Move at a constant speed and reflect cleanly at either edge."""
    span = right_edge - left_edge
    if span <= 0:
        return (left_edge + right_edge) / 2, direction

    offset = min(max(position, left_edge), right_edge) - left_edge
    phase = (offset + direction * speed * elapsed) % (2 * span)
    if phase < span:
        return left_edge + phase, 1
    return right_edge - (phase - span), -1


def check_quit():
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
    return False


def draw_frame(image, animation, frame_index, center_x, direction):
    left, top, width, height = animation['frames'][frame_index]
    bottom = image.h - (top + height)
    draw_height = height * SCALE
    draw_width = width * SCALE

    jump_offset = 0
    if animation['jump']:
        progress = frame_index / max(len(animation['frames']) - 1, 1)
        jump_offset = 4 * JUMP_HEIGHT * progress * (1 - progress)

    image.clip_composite_draw(
        left, bottom, width, height, 0,
        'h' if animation['moving'] and direction < 0 else '',
        center_x, GROUND_Y + jump_offset + draw_height / 2,
        draw_width, draw_height,
    )


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    image = None
    try:
        image = load_image(SPRITE_FILE)
        validate_animations(ANIMATIONS, image.w, image.h)

        animation_index = 0
        frame_index = 0
        completed_loops = 0
        frame_elapsed = 0.0
        pause_remaining = 0.0
        paused = False
        direction = 1
        center_x = CANVAS_WIDTH / 2
        previous_time = perf_counter()
        running = True

        while running:
            if check_quit():
                break

            now = perf_counter()
            elapsed = now - previous_time
            previous_time = now
            animation = ANIMATIONS[animation_index]

            if paused:
                pause_remaining -= elapsed
                if pause_remaining <= 0:
                    animation_index = (animation_index + 1) % len(ANIMATIONS)
                    animation = ANIMATIONS[animation_index]
                    frame_index = 0
                    completed_loops = 0
                    frame_elapsed = 0.0
                    paused = False
                    if not animation['moving']:
                        center_x = CANVAS_WIDTH / 2
            else:
                if animation['moving']:
                    _, _, frame_width, _ = animation['frames'][frame_index]
                    half_width = frame_width * SCALE / 2
                    left_edge = half_width + 2
                    right_edge = CANVAS_WIDTH - half_width - 2
                    center_x, direction = move_horizontally(
                        center_x, direction, elapsed, MOVE_SPEED,
                        left_edge, right_edge,
                    )

                frame_elapsed += elapsed
                while frame_elapsed >= FRAME_DELAY and not paused:
                    frame_elapsed -= FRAME_DELAY
                    if frame_index + 1 < len(animation['frames']):
                        frame_index += 1
                    else:
                        completed_loops += 1
                        if completed_loops >= REPEAT_COUNT:
                            frame_index = len(animation['frames']) - 1
                            pause_remaining = PAUSE_TIME
                            paused = True
                        else:
                            frame_index = 0

            clear_canvas()
            animation = ANIMATIONS[animation_index]
            draw_x = center_x if animation['moving'] else CANVAS_WIDTH / 2
            draw_frame(image, animation, frame_index, draw_x, direction)
            update_canvas()
            delay(1 / FPS)
    finally:
        if image is not None:
            del image
        close_canvas()


if __name__ == '__main__':
    main()
