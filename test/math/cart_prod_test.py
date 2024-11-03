import unittest

from src.math.cart_prod import spatial_cart_prod
from src.math.direction import Direction

class CartProdTest(unittest.TestCase):
	def test__spatial_cart_prod(self):
		xs = range(2)
		ys = range(2)
		prod = spatial_cart_prod(xs, ys)
		self.assertEqual(prod[0], (0,0))
		self.assertEqual(prod[1], (1,0))
		self.assertEqual(prod[2], (0,1))
		self.assertEqual(prod[3], (1,1))
	
	def test__spatial_cart_prod__uneven_y(self):
		xs = range(2)
		ys = range(3)
		prod = spatial_cart_prod(xs, ys)
		self.assertEqual(prod[0], (0,0))
		self.assertEqual(prod[1], (1,0))
		self.assertEqual(prod[2], (0,1))
		self.assertEqual(prod[3], (1,1))
		self.assertEqual(prod[4], (0,2))
		self.assertEqual(prod[5], (1,2))
	
	def test__spatial_cart_prod__uneven_x(self):
		xs = range(3)
		ys = range(2)
		prod = spatial_cart_prod(xs, ys)
		self.assertEqual(prod[0], (0,0))
		self.assertEqual(prod[1], (1,0))
		self.assertEqual(prod[2], (2,0))
		self.assertEqual(prod[3], (0,1))
		self.assertEqual(prod[4], (1,1))
		self.assertEqual(prod[5], (2,1))
	
	def test__spatial_cart_prod__northeast(self):
		xs = range(2)
		ys = range(2)
		prod = spatial_cart_prod(xs, ys, origin=Direction.NORTHEAST)
		self.assertEqual(prod[0], (1,0))
		self.assertEqual(prod[1], (0,0))
		self.assertEqual(prod[2], (1,1))
		self.assertEqual(prod[3], (0,1))
	
	def test__spatial_cart_prod__southwest(self):
		xs = range(2)
		ys = range(2)
		prod = spatial_cart_prod(xs, ys, origin=Direction.SOUTHWEST)
		self.assertEqual(prod[2], (0,0))
		self.assertEqual(prod[3], (1,0))
		self.assertEqual(prod[0], (0,1))
		self.assertEqual(prod[1], (1,1))
	
	def test__spatial_cart_prod__southeast(self):
		xs = range(2)
		ys = range(2)
		prod = spatial_cart_prod(xs, ys, origin=Direction.SOUTHEAST)
		self.assertEqual(prod[3], (0,0))
		self.assertEqual(prod[2], (1,0))
		self.assertEqual(prod[1], (0,1))
		self.assertEqual(prod[0], (1,1))
