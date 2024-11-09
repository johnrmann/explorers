import unittest

from src.rendermath.fit_rect import fit_img_rect_on_tile_base

class FitRectTest(unittest.TestCase):
	def test__basic_square_tile(self):
		img_dims = (100, 100)
		tile = [(50, 0), (150, 50), (100, 100), (0, 50)]
		expected_origin = (0, -50)
		expected_dims = (150, 150)
		result_origin, result_dims = fit_img_rect_on_tile_base(img_dims, tile)
		self.assertEqual(result_origin, expected_origin)
		self.assertEqual(result_dims, expected_dims)

if __name__ == '__main__':
	unittest.main()
