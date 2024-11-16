import unittest

from math import sqrt

from src.math.vector2 import Vector2, vector2_lerp, vector2_bounding_rect
from src.math.vector2 import vector2_move_points_near_zero
from src.math.vector2 import (
	vector2_rotate_point,
	vector2_rotate_points,
	vector2_average,
)

class Vector2Test(unittest.TestCase):
	def test__print(self):
		p = Vector2(4,8)
		self.assertEqual(str(p), "(4.00, 8.00)")
	
	def test__equality(self):
		p = Vector2(1,1)
		q = Vector2(1,1)
		self.assertEqual(p == q, True)
		r = Vector2(2,3)
		s = Vector2(4,5)
		self.assertEqual(r == s, False)
	
	def test__equality__with_tuple(self):
		p = Vector2(1,1)
		q = (1,1)
		self.assertEqual(p, q)

	def test__addition(self):
		p = Vector2(4, 8)
		q = Vector2(15, 16)
		self.assertEqual(p + q, Vector2(19, 24))

	def test__addition__with_tuple(self):
		p = Vector2(4, 8)
		q = (15, 16)
		self.assertEqual(p + q, Vector2(19, 24))
	
	def test__is_cardinal(self):
		yes = [
			Vector2(2,0),
			Vector2(0,5),
		]
		for y in yes:
			self.assertTrue(y.is_cardinal())
		nopes = [
			Vector2(0,0),
			Vector2(1,1),
			Vector2(2,-1),
		]
		for nope in nopes:
			self.assertFalse(nope.is_cardinal())
	
	def test__is_diagonal(self):
		yes = Vector2(1, 1)
		self.assertTrue(yes.is_diagonal())
		nopes = [
			Vector2(0,0),
			Vector2(3,5),
			Vector2(5,0),
		]
		for nope in nopes:
			self.assertFalse(nope.is_diagonal())
	
	def test__magnitude2(self):
		self.assertEqual(Vector2(0,0).magnitude2(), 0)
		self.assertEqual(Vector2(1,0).magnitude2(), 1)
		self.assertEqual(Vector2(1,1).magnitude2(), 2)
		self.assertEqual(Vector2(0,-2).magnitude2(), 4)
	
	def test__magnitude(self):
		self.assertAlmostEqual(Vector2(0,0).magnitude(), 0)
		self.assertAlmostEqual(Vector2(1,0).magnitude(), 1)
		self.assertAlmostEqual(Vector2(1,1).magnitude(), sqrt(2))
		self.assertAlmostEqual(Vector2(0,-2).magnitude(), 2)
	
	def test__normalized(self):
		dn_x, dn_y = Vector2(1,1).normalized()
		self.assertAlmostEqual(dn_x, 1 / sqrt(2))
		self.assertAlmostEqual(dn_y, 1 / sqrt(2))
		dn_x, dn_y = Vector2(-1,1).normalized()
		self.assertAlmostEqual(dn_x, -1 / sqrt(2))
		self.assertAlmostEqual(dn_y, 1 / sqrt(2))
	
	def test__vector2_lerp__works(self):
		p = Vector2(0, 0)
		q = Vector2(10, 20)
		self.assertEqual(
			vector2_lerp(p, q, 0),
			p
		)
		self.assertEqual(
			vector2_lerp(p, q, 1),
			q
		)
		self.assertEqual(
			vector2_lerp(p, q, 0.5),
			Vector2(5,10),
		)

	def test__round(self):
		self.assertEqual(Vector2(1.2, 3.7).round(), Vector2(1, 4))
		self.assertEqual(Vector2(-1.5, 2.5).round(), Vector2(-2, 2))
		self.assertEqual(Vector2(0.0, 0.0).round(), Vector2(0, 0))
		self.assertEqual(Vector2(-2.3, -3.8).round(), Vector2(-2, -4))

	def test__vector2_bounding_rect__single_point(self):
		points = [Vector2(1, 1)]
		expected_origin = (1, 1)
		expected_dimensions = (0, 0)
		self.assertEqual(vector2_bounding_rect(points), (expected_origin, expected_dimensions))

	def test__vector2_bounding_rect__multiple_points(self):
		points = [Vector2(1, 1), Vector2(2, 3), Vector2(-1, -2)]
		expected_origin = (-1, -2)
		expected_dimensions = (3, 5)
		self.assertEqual(vector2_bounding_rect(points), (expected_origin, expected_dimensions))

	def test__vector2_bounding_rect__horizontal_line(self):
		points = [Vector2(1, 1), Vector2(3, 1), Vector2(2, 1)]
		expected_origin = (1, 1)
		expected_dimensions = (2, 0)
		self.assertEqual(vector2_bounding_rect(points), (expected_origin, expected_dimensions))

	def test__vector2_bounding_rect__vertical_line(self):
		points = [Vector2(1, 1), Vector2(1, 3), Vector2(1, 2)]
		expected_origin = (1, 1)
		expected_dimensions = (0, 2)
		self.assertEqual(vector2_bounding_rect(points), (expected_origin, expected_dimensions))

	def test__vector2_bounding_rect__empty_list(self):
		points = []
		with self.assertRaises(ValueError):
			vector2_bounding_rect(points)

	def test__vector2_move_points_near_zero__single_point(self):
		points = [Vector2(1, 1)]
		expected_points = [(0, 0)]
		self.assertEqual(vector2_move_points_near_zero(points), expected_points)

	def test__vector2_move_points_near_zero__multiple_points(self):
		points = [Vector2(1, 1), Vector2(2, 2)]
		expected_points = [(0, 0), (1, 1)]
		self.assertEqual(vector2_move_points_near_zero(points), expected_points)

	def test__vector2_move_points_near_zero__negative_points(self):
		points = [Vector2(-1, -1), Vector2(-2, -2)]
		expected_points = [(1, 1), (0, 0)]
		self.assertEqual(vector2_move_points_near_zero(points), expected_points)

	def test__vector2_move_points_near_zero__mixed_points(self):
		points = [Vector2(0, 1), Vector2(1, 0)]
		expected_points = [(0, 1), (1, 0)]
		self.assertEqual(vector2_move_points_near_zero(points), expected_points)

	def test__vector2_move_points_near_zero__empty_list(self):
		points = []
		with self.assertRaises(ValueError):
			vector2_move_points_near_zero(points)

	def test__vector2_rotate_point__no_rotation(self):
		point = (1,1)
		expected = (1,1)
		self.assertEqual(vector2_rotate_point(point, 0), expected)

	def test__vector2_rotate_point__one_quarter_turn(self):
		point = (1,1)
		expected = (1,-1)
		self.assertEqual(vector2_rotate_point(point, 1), expected)

	def test__vector2_rotate_point__two_quarter_turns(self):
		point = (1,1)
		expected = (-1,-1)
		self.assertEqual(vector2_rotate_point(point, 2), expected)

	def test__vector2_rotate_point__three_quarter_turns(self):
		point = (1,1)
		expected = (-1,1)
		self.assertEqual(vector2_rotate_point(point, 3), expected)

	def test__vector2_rotate_point__four_quarter_turns(self):
		point = (1,1)
		expected = (1,1)
		self.assertEqual(vector2_rotate_point(point, 4), expected)

	def test__vector2_rotate_point__five_quarter_turns(self):
		point = (1,1)
		expected = (1,-1)
		self.assertEqual(vector2_rotate_point(point, 5), expected)

	def test__vector2_rotate_points__no_rotation(self):
		points = [(1, 2), (3, 4)]
		expected_points = [(1, 2), (3, 4)]
		self.assertEqual(vector2_rotate_points(points, 0), expected_points)

	def test__vector2_rotate_points__one_quarter_turn(self):
		points = [(1, 2), (3, 4)]
		expected_points = [(2, -1), (4, -3)]
		self.assertEqual(vector2_rotate_points(points, 1), expected_points)

	def test__vector2_rotate_points__two_quarter_turns(self):
		points = [(1, 2), (3, 4)]
		expected_points = [(-1, -2), (-3, -4)]
		self.assertEqual(vector2_rotate_points(points, 2), expected_points)

	def test__vector2_rotate_points__three_quarter_turns(self):
		points = [(1, 2), (3, 4)]
		expected_points = [(-2, 1), (-4, 3)]
		self.assertEqual(vector2_rotate_points(points, 3), expected_points)

	def test__vector2_rotate_points__four_quarter_turns(self):
		points = [(1, 2), (3, 4)]
		expected_points = [(1, 2), (3, 4)]
		self.assertEqual(vector2_rotate_points(points, 4), expected_points)

	def test__vector2_rotate_points__five_quarter_turns(self):
		points = [(1, 2), (3, 4)]
		expected_points = [(2, -1), (4, -3)]
		self.assertEqual(vector2_rotate_points(points, 5), expected_points)

	def test__vector2_average__single_point(self):
		points = [Vector2(1, 1)]
		expected_average = (1, 1)
		self.assertEqual(vector2_average(points), expected_average)

	def test__vector2_average__multiple_points(self):
		points = [Vector2(1, 1), Vector2(3, 3)]
		expected_average = (2, 2)
		self.assertEqual(vector2_average(points), expected_average)

	def test__vector2_average__negative_points(self):
		points = [Vector2(-1, -1), Vector2(-3, -3)]
		expected_average = (-2, -2)
		self.assertEqual(vector2_average(points), expected_average)

	def test__vector2_average__mixed_points(self):
		points = [Vector2(1, -1), Vector2(-1, 1)]
		expected_average = (0, 0)
		self.assertEqual(vector2_average(points), expected_average)

	def test__vector2_average__empty_list(self):
		points = []
		with self.assertRaises(ZeroDivisionError):
			vector2_average(points)

if __name__ == "__main__":
	unittest.main()
