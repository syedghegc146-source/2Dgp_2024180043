import unittest

import move_character_with_key as game


class MovementInputTests(unittest.TestCase):
    def test_no_keys_means_idle(self):
        move_x, move_y = game.movement_vector(set())

        self.assertEqual((move_x, move_y), (0, 0))
        self.assertEqual(game.animation_row(False, 'right'), 300)

    def test_horizontal_arrow_keys_set_horizontal_direction(self):
        self.assertEqual(game.movement_vector({game.SDLK_RIGHT}), (1, 0))
        self.assertEqual(game.movement_vector({game.SDLK_LEFT}), (-1, 0))

    def test_vertical_arrow_keys_set_vertical_direction(self):
        self.assertEqual(game.movement_vector({game.SDLK_UP}), (0, 1))
        self.assertEqual(game.movement_vector({game.SDLK_DOWN}), (0, -1))

    def test_opposite_keys_cancel_each_axis(self):
        horizontal = game.movement_vector({game.SDLK_LEFT, game.SDLK_RIGHT})
        vertical = game.movement_vector({game.SDLK_UP, game.SDLK_DOWN})

        self.assertEqual(horizontal, (0, 0))
        self.assertEqual(vertical, (0, 0))

    def test_diagonal_speed_is_normalized(self):
        move_x, move_y = game.movement_vector({game.SDLK_RIGHT, game.SDLK_UP})

        self.assertAlmostEqual(move_x * move_x + move_y * move_y, 1.0)


class MovementPositionTests(unittest.TestCase):
    def test_right_movement_uses_elapsed_time(self):
        x, y = game.move_character(600, 500, 1, 0, 0.5)

        self.assertEqual((x, y), (750, 500))

    def test_left_movement_uses_elapsed_time(self):
        x, y = game.move_character(600, 500, -1, 0, 0.5)

        self.assertEqual((x, y), (450, 500))

    def test_vertical_movement_uses_elapsed_time(self):
        upward = game.move_character(600, 500, 0, 1, 0.5)
        downward = game.move_character(600, 500, 0, -1, 0.5)

        self.assertEqual(upward, (600, 650))
        self.assertEqual(downward, (600, 350))

    def test_left_screen_boundary_clamps_character(self):
        x, y = game.move_character(50, 500, -1, 0, 1.0)

        self.assertEqual((x, y), (50, 500))

    def test_right_screen_boundary_clamps_character(self):
        x, y = game.move_character(1230, 500, 1, 0, 1.0)

        self.assertEqual((x, y), (1230, 500))

    def test_bottom_screen_boundary_clamps_character(self):
        x, y = game.move_character(600, 50, 0, -1, 1.0)

        self.assertEqual((x, y), (600, 50))


if __name__ == '__main__':
    unittest.main()
