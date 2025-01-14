import unittest

from src.rendermath.order import draw_order_vector, offset_tile_by_draw_order_vector
from src.math.vector2 import Vector2
from src.math.direction import Direction
from src.rendermath.order import screen_draw_order, cells_draw_order

class OrderTest(unittest.TestCase):
	def test__draw_order_vector(self):
		self.assertEqual(draw_order_vector(Direction.NORTHWEST), Vector2(1, 1))
		self.assertEqual(draw_order_vector(Direction.SOUTHEAST), Vector2(-1, -1))
		self.assertEqual(draw_order_vector(Direction.NORTHEAST), Vector2(-1, 1))
		self.assertEqual(draw_order_vector(Direction.SOUTHWEST), Vector2(1, -1))


	def test__offset_tile_by_draw_order_vector__identity(self):
		p = Vector2(0, 0)
		nxt, _ = offset_tile_by_draw_order_vector(p, Direction.NORTHWEST, 0)
		self.assertEqual(nxt.x, 0)
		self.assertEqual(nxt.y, 0)


	def test__offset_tile_by_draw_order_vector__odd_offset(self):
		p = Vector2(0,0)
		odd1, odd2 = offset_tile_by_draw_order_vector(p, Direction.NORTHWEST, 1)
		self.assertEqual((odd1.x, odd1.y), (1, 0))
		self.assertEqual((odd2.x, odd2.y), (0, 1))


	def test__offset_tile_by_draw_order_vector__even_offset(self):
		p = Vector2(0, 0)
		even, _ = offset_tile_by_draw_order_vector(p, Direction.NORTHWEST, 2)
		self.assertEqual(even, (1, 1))


	def test__cells_draw_order__single_cell(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.NORTHWEST
		size = 1
		expected = [(0, 0)]
		result = list(cells_draw_order(origin, size, cam_dir))
		self.assertEqual(result, expected)


	def test__cells_draw_order__2x2(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.NORTHWEST
		size = 2
		expected = [(0, 0), (0, 1), (1, 0), (1, 1)]
		result = list(cells_draw_order(origin, size, cam_dir))
		self.assertEqual(result, expected)


	def disable_test__cells_draw_order__2x2_northeast(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.NORTHEAST
		size = 2
		expected = [(1, 0), (0, 0), (1, 1), (0, 1)]
		result = list(cells_draw_order(origin, size, cam_dir))
		self.assertEqual(result, expected)


	def disable_test__cells_draw_order__2x2_southeast(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.SOUTHEAST
		size = 2
		expected = [(1, 1), (0, 1), (1, 0), (0, 0)]
		result = list(cells_draw_order(origin, size, cam_dir))
		self.assertEqual(result, expected)


	def disable_test__cells_draw_order__2x2_southwest(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.SOUTHWEST
		size = 2
		expected = [(0, 1), (1, 1), (0, 0), (1, 0)]
		result = list(cells_draw_order(origin, size, cam_dir))
		self.assertEqual(result, expected)


	def test__screen_draw_order__single_cell(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.NORTHWEST
		num_cols = 1
		num_rows = 1
		expected = [(0, 0)]
		result = list(screen_draw_order(origin, cam_dir, num_cols, num_rows))
		self.assertEqual(result, expected)


	def test__screen_draw_order__multiple_cells(self):
		origin = Vector2(0, 0)
		cam_dir = Direction.NORTHWEST
		num_cols = 2
		num_rows = 2
		expected = [(0, 0), (1, -1), (0, 1), (1, 0)]
		result = list(screen_draw_order(origin, cam_dir, num_cols, num_rows))
		self.assertEqual(result, expected)

if __name__ == '__main__':
	unittest.main()
