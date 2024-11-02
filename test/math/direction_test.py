import unittest

from src.math.direction import *

class DirectionTest(unittest.TestCase):
	def test__is_direction_diagonal(self):
		self.assertFalse(is_direction_diagonal(Direction.NORTH))
		self.assertFalse(is_direction_diagonal(Direction.SOUTH))
		self.assertFalse(is_direction_diagonal(Direction.EAST))
		self.assertFalse(is_direction_diagonal(Direction.WEST))
		self.assertTrue(is_direction_diagonal(Direction.NORTHEAST))
		self.assertTrue(is_direction_diagonal(Direction.NORTHWEST))
		self.assertTrue(is_direction_diagonal(Direction.SOUTHEAST))
		self.assertTrue(is_direction_diagonal(Direction.SOUTHWEST))

if __name__ == "__main__":
	unittest.main()
