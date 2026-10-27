from time import monotonic

from pico2d import load_image, get_canvas_width


FRAME_SIZE = 100
NORMAL_SPEED = 300.0
AUTO_RUN_SPEED = 600.0
AUTO_RUN_SCALE = 1.5
AUTO_RUN_DURATION = 5.0


class Idle:
    name = 'IDLE'
    scale = 1.0

    def update(self, boy, elapsed):
        if boy.direction:
            boy.change_state(Run())
            boy.state.update(boy, elapsed)


class Run:
    name = 'RUN'
    scale = 1.0

    def update(self, boy, elapsed):
        if not boy.direction:
            boy.change_state(Idle())
            return

        boy.face_dir = boy.direction
        boy.move(boy.direction, NORMAL_SPEED, elapsed, self.scale)


class AutoRun:
    name = 'AUTO_RUN'
    scale = AUTO_RUN_SCALE

    def __init__(self):
        self.elapsed = 0.0
        self.direction = 1

    def enter(self, boy):
        self.direction = boy.face_dir

    def update(self, boy, elapsed):
        self.elapsed += elapsed
        if self.elapsed >= AUTO_RUN_DURATION:
            boy.change_state(Idle())
            return

        if boy.direction:
            boy.face_dir = boy.direction
            boy.change_state(Run())
            boy.state.update(boy, elapsed)
            return

        boy.face_dir = self.direction
        if boy.move(self.direction, AUTO_RUN_SPEED, elapsed, self.scale):
            self.direction *= -1


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.direction = 0
        self.last_update = monotonic()
        self.image = load_image('animation_sheet.png')
        self.state = Idle()

    def change_state(self, state):
        self.state = state
        if isinstance(state, AutoRun):
            state.enter(self)

    def start_auto_run(self):
        if self.state.name == Idle.name:
            self.change_state(AutoRun())

    def update(self, elapsed=None):
        now = monotonic()
        if elapsed is None:
            elapsed = now - self.last_update
        self.last_update = now

        self.state.update(self, elapsed)
        self.frame = (self.frame + 1) % 8

    def set_direction(self, direction):
        self.direction = direction

    def move(self, direction, speed, elapsed, scale):
        self.x += direction * speed * elapsed
        half_width = FRAME_SIZE * scale / 2
        left_edge = half_width
        right_edge = get_canvas_width() - half_width

        if self.x <= left_edge:
            self.x = left_edge
            return True
        if self.x >= right_edge:
            self.x = right_edge
            return True
        return False

    def draw(self):
        is_moving = self.state.name != Idle.name
        if is_moving:
            row = 100 if self.face_dir == 1 else 0
        else:
            row = 300 if self.face_dir == 1 else 200

        size = FRAME_SIZE * self.state.scale
        self.image.clip_draw(
            self.frame * FRAME_SIZE,
            row,
            FRAME_SIZE,
            FRAME_SIZE,
            self.x,
            self.y,
            size,
            size,
        )
