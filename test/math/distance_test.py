import unittest

from src.math.vector2 import Vector2
from src.math.distance import (
	distance2,
	distance,
	manhattan_distance,
	planet_distance2,
	min_planet_distance2,
	looped_distance,
	washington_distance,
	planet_manhattan_distance,
	planet_washington_distance,
	ROOT_2
)

class DistanceTest(unittest.TestCase):
	def test__distance2(self):
		p = (0,0)
		q = (1,1)
		self.assertAlmostEqual(distance2(p, q), 2)

	def test__distance(self):
		p = (0,0)
		q = (1,1)
		self.assertAlmostEqual(distance(p, q), ROOT_2)

	def test__manhattan_distance__flat(self):
		p = (0,0)
		q1 = (5,0)
		q2 = (0,5)
		self.assertEqual(manhattan_distance(p, q1), 5)
		self.assertEqual(manhattan_distance(p, q2), 5)

	def test__manhattan_distance__works(self):
		p = (0,0)
		q = (5,5)
		self.assertEqual(manhattan_distance(p, q), 10)

	def test__washington_distance__trivial(self):
		p = Vector2(0, 0)
		q = Vector2(1, 1)
		self.assertAlmostEqual(washington_distance(p, q), ROOT_2)

	def test__washington_distance__flat(self):
		p = Vector2(0, 0)
		q1 = Vector2(5, 0)
		q2 = Vector2(0, 5)
		self.assertEqual(washington_distance(p, q1), 5)
		self.assertEqual(washington_distance(p, q2), 5)

	def test__washington_distance__diagonal(self):
		p = Vector2(0, 0)
		q = Vector2(3, 3)
		self.assertAlmostEqual(washington_distance(p, q), 3 * ROOT_2)

	def test__washington_distance__mixed(self):
		p = Vector2(0, 0)
		q = Vector2(3, 4)
		self.assertAlmostEqual(washington_distance(p, q), (3 * ROOT_2) + 1)

	def test__planet_distance2__trivial(self):
		d = (4,4)
		p = (1,1)
		q = (2,2)
		self.assertEqual(planet_distance2(p, q, d), 2)

	def test__planet_distance2__loops_x(self):
		d = (8,8)
		p = (7,7)
		q = (0,7)
		self.assertEqual(planet_distance2(p, q, d), 1)
		q = (1,7)
		self.assertEqual(planet_distance2(p, q, d), 4)

	def test__planet_distance2__doesnt_loop_y(self):
		d = (8,8)
		p = (1,1)
		q = (1,6)
		self.assertEqual(planet_distance2(p, q, d), 25)

	def test__planet_distance2__loops_x_doesnt_loop_y(self):
		d = (8,8)
		p = (1,1)
		q = (6,6)
		self.assertEqual(planet_distance2(p, q, d), 9 + 25)

	def test__planet_manhattan_distance__trivial(self):
		d = (4,4)
		p = (1,1)
		q = (2,3)
		self.assertEqual(planet_manhattan_distance(p, q, d), 3)

	def test__planet_manhattan_distance__loops_x(self):
		d = (8,8)
		p = (7,7)
		q = (0,7)
		self.assertEqual(planet_manhattan_distance(p, q, d), 1)
		q = (1,7)
		self.assertEqual(planet_manhattan_distance(p, q, d), 2)

	def test__planet_washington_distance__trivial(self):
		d = Vector2(4, 4)
		p = Vector2(1, 1)
		q = Vector2(2, 2)
		self.assertAlmostEqual(planet_washington_distance(p, q, d), ROOT_2)

	def test__planet_washington_distance__loops_x(self):
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(0, 7)
		self.assertAlmostEqual(planet_washington_distance(p, q, d), 1)
		q = Vector2(1, 7)
		self.assertAlmostEqual(planet_washington_distance(p, q, d), 2)

	def test__planet_washington_distance__doesnt_loop_y(self):
		d = Vector2(8, 8)
		p = Vector2(1, 1)
		q = Vector2(1, 6)
		self.assertAlmostEqual(planet_washington_distance(p, q, d), 5)

	def test__planet_washington_distance__loops_x_doesnt_loop_y(self):
		d = Vector2(8, 8)
		p = Vector2(1, 1)
		q = Vector2(6, 6)
		self.assertAlmostEqual(
			planet_washington_distance(p, q, d),
			(5 * ROOT_2)
		)

	def test__min_planet_distance2(self):
		d = (8,8)
		p = (1,1)
		qs = [(7,1), (5,5), (2,7)]
		self.assertEqual(min_planet_distance2(p, qs, d), (7,1))

	def test__looped_distance__no_loop(self):
		d = Vector2(8, 8)
		p = Vector2(1, 1)
		q = Vector2(6, 6)
		self.assertEqual(looped_distance(distance2, p, q, d), distance2(p, q))

	def test__looped_distance__loop_x(self):
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(0, 7)
		self.assertEqual(looped_distance(distance2, p, q, d, loop_x=True), 1)

	def test__looped_distance__loop_y(self):
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(7, 0)
		self.assertEqual(looped_distance(distance2, p, q, d, loop_y=True), 1)

	def test__looped_distance__loop_x_and_y(self):
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(0, 0)
		self.assertEqual(
			looped_distance(distance2, p, q, d, loop_x=True, loop_y=True),
			2
		)

	def test__looped_distance__manhattan_no_loop(self):
		d = Vector2(8, 8)
		p = Vector2(1, 1)
		q = Vector2(6, 6)
		self.assertEqual(
			looped_distance(manhattan_distance, p, q, d),
			manhattan_distance(p, q)
		)

	def test__looped_distance__manhattan_loop_x(self):
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(0, 7)
		self.assertEqual(
			looped_distance(manhattan_distance, p, q, d, loop_x=True),
			1
		)

	def test__looped_distance__manhattan_loop_y(self):
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(7, 0)
		self.assertEqual(
			looped_distance(manhattan_distance, p, q, d, loop_y=True),
			1
		)

	def test__looped_distance__manhattan_loop_x_and_y(self):
		ny_dist = manhattan_distance
		d = Vector2(8, 8)
		p = Vector2(7, 7)
		q = Vector2(0, 0)
		self.assertEqual(
			looped_distance(ny_dist, p, q, d, loop_x=True, loop_y=True),
		2)

if __name__ == "__main__":
	unittest.main()
