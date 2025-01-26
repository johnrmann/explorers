"""Tests for the direction util file."""

import unittest

from src.math.vector2 import Vector2
from src.math.direction import *

class DirectionTest(unittest.TestCase):
	"""Tests for the direction util file."""
	def test__is_direction_diagonal(self):
		"""Test if directions are cardinal or diagonal."""
		self.assertFalse(is_direction_diagonal(Direction.NORTH))
		self.assertFalse(is_direction_diagonal(Direction.SOUTH))
		self.assertFalse(is_direction_diagonal(Direction.EAST))
		self.assertFalse(is_direction_diagonal(Direction.WEST))
		self.assertTrue(is_direction_diagonal(Direction.NORTHEAST))
		self.assertTrue(is_direction_diagonal(Direction.NORTHWEST))
		self.assertTrue(is_direction_diagonal(Direction.SOUTHEAST))
		self.assertTrue(is_direction_diagonal(Direction.SOUTHWEST))
	
	def test__delta_to_direction(self):
		self.assertEqual(
			delta_to_direction(Vector2(0,1)),
			Direction.SOUTH,
		)
		self.assertEqual(
			delta_to_direction(Vector2(1,0)),
			Direction.EAST,
		)
		self.assertEqual(
			delta_to_direction(Vector2(0,-1)),
			Direction.NORTH,
		)
		self.assertEqual(
			delta_to_direction(Vector2(-1,0)),
			Direction.WEST,
		)
		self.assertEqual(
			delta_to_direction(Vector2(1,1)),
			Direction.SOUTHEAST,
		)
		self.assertEqual(
			delta_to_direction(Vector2(1,-1)),
			Direction.NORTHEAST,
		)
		self.assertEqual(
			delta_to_direction(Vector2(-1,-1)),
			Direction.NORTHWEST,
		)
		self.assertEqual(
			delta_to_direction(Vector2(-1,1)),
			Direction.SOUTHWEST,
		)

	def test__delta_to_direction__rejects_weird(self):
		"""Test that delta to direction rejects zero vectors, or vectors
		that are not of the form k * (-1,0,1)^2"""
		self.assertRaises(ValueError, lambda: delta_to_direction(Vector2(0,0)))
		self.assertRaises(ValueError, lambda: delta_to_direction(Vector2(3,2)))

	def test__direction_rotate_90(self):
		"""Test that it can handle rotating 90deg."""
		self.assertEqual(
			direction_rotate_90(Direction.NORTH, quarter_turns=0),
			Direction.NORTH,
		)
		self.assertEqual(
			direction_rotate_90(Direction.NORTH, quarter_turns=1),
			Direction.EAST,
		)
		self.assertEqual(
			direction_rotate_90(Direction.NORTHEAST, quarter_turns=2),
			Direction.SOUTHWEST,
		)

	def test__direction_rotate_90__loop(self):
		"""Test that it can handle overflow."""
		self.assertEqual(
			direction_rotate_90(Direction.WEST, quarter_turns=1),
			Direction.NORTH,
		)
		self.assertEqual(
			direction_rotate_90(Direction.NORTHWEST, quarter_turns=2),
			Direction.SOUTHEAST,
		)

	def test__direction_rotate_90__backward(self):
		"""Test that it can handle negative numbers."""
		self.assertEqual(
			direction_rotate_90(Direction.SOUTH, quarter_turns=-1),
			Direction.EAST
		)
		self.assertEqual(
			direction_rotate_90(Direction.NORTHWEST, quarter_turns=-2),
			Direction.SOUTHEAST
		)

	def test__direction_rotate_45__quarter(self):
		"""Test quarter-turns expressed as 45deg increments."""
		self.assertEqual(
			direction_rotate_45(Direction.NORTH, eighth_turns=2),
			Direction.EAST,
		)
		self.assertEqual(
			direction_rotate_45(Direction.SOUTHEAST, eighth_turns=2),
			Direction.SOUTHWEST,
		)

	def test__direction_rotate_45__eighth(self):
		"""Tests eighth turns."""
		self.assertEqual(
			direction_rotate_45(Direction.NORTH, eighth_turns=1),
			Direction.NORTHEAST,
		)
		self.assertEqual(
			direction_rotate_45(Direction.SOUTHEAST, eighth_turns=3),
			Direction.WEST,
		)

	def test__direction_rotate_45__loop(self):
		"""Tests overflowing rotating directions by 45deg."""
		self.assertEqual(
			direction_rotate_45(Direction.NORTHWEST, eighth_turns=3),
			Direction.EAST,
		)
		self.assertEqual(
			direction_rotate_45(Direction.WEST, eighth_turns=3),
			Direction.NORTHEAST,
		)

	def test__direction_rotate_45__backward(self):
		"""Tests rotating directions by 45deg increments backward."""
		self.assertEqual(
			direction_rotate_45(Direction.NORTHWEST, eighth_turns=-3),
			Direction.SOUTH,
		)
		self.assertEqual(
			direction_rotate_45(Direction.WEST, eighth_turns=-3),
			Direction.SOUTHEAST,
		)

	def test__left_wall_direction(self):
		"""
		The default camera orientation is NW, so the left wall should
		be south.
		"""
		self.assertEqual(
			left_wall_direction(Direction.NORTHWEST),
			Direction.SOUTH
		)

	def test__right_wall_direction(self):
		"""
		The default camera orientation is NW, so the left wall should
		be east.
		"""
		self.assertEqual(
			right_wall_direction(Direction.NORTHWEST),
			Direction.EAST
		)

	def test__left_ridge_direction(self):
		"""
		The default camera orientation is NW, so the left ridge should be
		west.
		"""
		self.assertEqual(
			left_ridge_direction(Direction.NORTHWEST),
			Direction.WEST,
		)

	def test__right_ridge_direction(self):
		"""
		The default camera orientation is NW, so the right ridge should be
		north.
		"""
		self.assertEqual(
			right_ridge_direction(Direction.NORTHWEST),
			Direction.NORTH,
		)

	def test__quarter_turns_between_directions__cardinal(self):
		"""Test quarter turns between cardinal directions."""
		self.assertEqual(
			quarter_turns_between_directions(Direction.NORTH, Direction.EAST),
			1
		)
		self.assertEqual(
			quarter_turns_between_directions(Direction.NORTH, Direction.SOUTH),
			2
		)
		self.assertEqual(
			quarter_turns_between_directions(Direction.NORTH, Direction.WEST),
			3
		)
		self.assertEqual(
			quarter_turns_between_directions(Direction.EAST, Direction.NORTH),
			3
		)

	def test__quarter_turns_between_directions__diagonal(self):
		"""Test quarter turns between diagonal directions."""
		self.assertEqual(
			quarter_turns_between_directions(
				Direction.NORTHEAST, Direction.SOUTHEAST
			),
			1
		)
		self.assertEqual(
			quarter_turns_between_directions(
				Direction.NORTHEAST, Direction.SOUTHWEST
			),
			2
		)
		self.assertEqual(
			quarter_turns_between_directions(
				Direction.NORTHEAST, Direction.NORTHWEST
			),
			3
		)
		self.assertEqual(
			quarter_turns_between_directions(
				Direction.SOUTHWEST, Direction.NORTHEAST
			),
			2
		)

	def test__quarter_turns_between_directions__invalid(self):
		"""Test quarter turns between invalid direction pairs."""
		with self.assertRaises(ValueError):
			quarter_turns_between_directions(
				Direction.NORTH, Direction.NORTHEAST
			)
		with self.assertRaises(ValueError):
			quarter_turns_between_directions(
				Direction.SOUTHWEST, Direction.EAST
			)

	def test__direction_to_delta__invalid(self):
		"""Test that direction to delta rejects invalid directions."""
		with self.assertRaises(AttributeError):
			direction_to_delta(None)

if __name__ == "__main__":
	unittest.main()
