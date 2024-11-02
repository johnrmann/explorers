import unittest

from src.math.map_range import map_range

class MapRangeTest(unittest.TestCase):
	def test__map_range__disjoint(self):
		r1 = (4, 8)
		r2 = (15, 16)
		self.assertEqual(map_range(6, r1, r2), 15.5)

if __name__ == "__main__":
	unittest.main()
