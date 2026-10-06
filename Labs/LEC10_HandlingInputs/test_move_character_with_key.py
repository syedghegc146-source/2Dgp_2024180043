import unittest

import move_character_with_key as game


class MovementInputTests(unittest.TestCase):
    def test_no_keys_means_idle(self):
        move_x, move_y = game.movement_vector(set())

        self.assertEqual((move_x, move_y), (0, 0))
        self.assertEqual(game.animation_row(False, 'right'), 300)


if __name__ == '__main__':
    unittest.main()
