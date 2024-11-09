import unittest

from src.rendermath.order import draw_order_vector, offset_tile_by_draw_order_vector
from src.math.vector2 import Vector2
from src.math.direction import Direction

class OrderTest(unittest.TestCase):
	def test__draw_order_vector(self):
		self.assertEqual(draw_order_vector(Direction.NORTHWEST), Vector2(1, 1))
		self.assertEqual(draw_order_vector(Direction.SOUTHEAST), Vector2(-1, -1))
		self.assertEqual(draw_order_vector(Direction.NORTHEAST), Vector2(-1, 1))
		self.assertEqual(draw_order_vector(Direction.SOUTHWEST), Vector2(1, -1))

	def test__offset_tile_by_draw_order_vector__identity(self):
		p = Vector2(0, 0)
		id, _ = offset_tile_by_draw_order_vector(p, Direction.NORTHWEST, 0)
		self.assertEqual(id.x, 0)
		self.assertEqual(id.y, 0)
	
	def test__offset_tile_by_draw_order_vector__odd_offset(self):
		p = Vector2(0,0)
		odd1, odd2 = offset_tile_by_draw_order_vector(p, Direction.NORTHWEST, 1)
		self.assertEqual((odd1.x, odd1.y), (1, 0))
		self.assertEqual((odd2.x, odd2.y), (0, 1))
	
	def test__offset_tile_by_draw_order_vector__even_offset(self):
		p = Vector2(0, 0)
		even, _ = offset_tile_by_draw_order_vector(p, Direction.NORTHWEST, 2)
		self.assertEqual(even, (1, 1))


if __name__ == '__main__':
	unittest.main()
