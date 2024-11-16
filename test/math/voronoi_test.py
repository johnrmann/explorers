import math
import unittest

from src.math.voronoi import *
from src.math.distance import *

class VoronoiTest(unittest.TestCase):
	def test__make_voronoi(self):
		d = (4,4)
		density = 4
		matrix = make_voronoi(d, density)
		labels = set()
		for y in range(4):
			for x in range(4):
				labels.add(matrix[y][x])
		self.assertEqual(len(labels), 4)

if __name__ == "__main__":
	unittest.main()
