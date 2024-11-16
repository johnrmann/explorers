import unittest

from src.math.vector3 import (
	Vector3, vector3_rotate_point, vector3_rotate_points
)

class TestVector3(unittest.TestCase):

	def test__init__valid_values(self):
		v = Vector3(1, 2, 3)
		self.assertEqual(v.x, 1)
		self.assertEqual(v.y, 2)
		self.assertEqual(v.z, 3)

	def test__iter__correct_iteration(self):
		v = Vector3(4, 5, 6)
		self.assertEqual(list(v), [4, 5, 6])

	def test__vector3_rotate_point__no_rotation(self):
		point = Vector3(1,1,1)
		rotated = vector3_rotate_point(point, quarter_turns=0)
		self.assertEqual(rotated, Vector3(1,1,1))

	def test__vector3_rotate_points__no_rotation(self):
		points = [(1, 2, 3), (4, 5, 6)]
		rotated_points = list(vector3_rotate_points(points, quarter_turns=0))
		expected = [Vector3(1, 2, 3), Vector3(4, 5, 6)]
		for p, q in zip(rotated_points, expected):
			self.assertEqual(p, q)

	def test__vector3_rotate_points__one_quarter_turn(self):
		points = [(1, 2, 3), (4, 5, 6)]
		rotated_points = list(vector3_rotate_points(points, quarter_turns=1))
		expected = [Vector3(2, -1, 3), Vector3(5, -4, 6)]
		for p, q in zip(rotated_points, expected):
			px, py, pz = p
			qx, qy, qz = q
			self.assertEqual(px, qx)
			self.assertEqual(py, qy)
			self.assertEqual(pz, qz)

if __name__ == '__main__':
	unittest.main()
