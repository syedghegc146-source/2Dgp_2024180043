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


if __name__ == '__main__':
    unittest.main()
