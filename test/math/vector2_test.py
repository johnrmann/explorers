import unittest

from math import sqrt

from src.math.vector2 import Vector2, vector2_lerp

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

if __name__ == "__main__":
	unittest.main()
