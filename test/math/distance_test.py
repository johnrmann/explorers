import math
import unittest

from src.math.distance import *

ROOT_2 = math.sqrt(2)

class DistanceTest(unittest.TestCase):
	def test__distance2(self):
		p = (0,0)
		q = (1,1)
		self.assertAlmostEqual(distance2(p, q), 2)
	
	def test__distance(self):
		p = (0,0)
		q = (1,1)
		self.assertAlmostEqual(distance(p, q), ROOT_2)
	
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
	
	def test__min_planet_distance2(self):
		d = (8,8)
		p = (1,1)
		qs = [(7,1), (5,5), (2,7)]
		self.assertEqual(min_planet_distance2(p, qs, d), (7,1))

if __name__ == "__main__":
	unittest.main()
