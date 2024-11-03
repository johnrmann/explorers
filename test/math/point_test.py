import unittest

from src.math.point import point_plus

class PointTest(unittest.TestCase):
	def test__point_plus(self):
		p = (4, 8)
		q = (15, 16)
		self.assertEqual(point_plus(p, q), (19, 24))

if __name__ == "__main__":
	unittest.main()
