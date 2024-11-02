import math
import unittest

from src.math.voronoi import *
from src.math.distance import *

class VoronoiTest(unittest.TestCase):
	def test__make_voronoi(self):
		d = (4,4)
		ps = [(2,0),(2,3)]
		matrix = make_voronoi(d, ps)
		count0 = 0
		count1 = 0
		for row in matrix:
			for val in row:
				if val == 0:
					count0 += 1
				else:
					count1 += 1
		self.assertEqual(count0, 8)
		self.assertEqual(count1, 8)

if __name__ == "__main__":
	unittest.main()
