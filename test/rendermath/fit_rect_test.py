import unittest

from math import sqrt

from src.rendermath.fit_rect import (
	fit_img_rect_on_tile_base,
	object_height_from_img_dims
)

class FitRectTest(unittest.TestCase):
	def test__basic_square_tile(self):
		img_dims = (100, 100)
		tile = [(50, 0), (150, 50), (100, 100), (0, 50)]
		expected_origin = (0, -50)
		expected_dims = (150, 150)
		result_origin, result_dims = fit_img_rect_on_tile_base(img_dims, tile)
		self.assertEqual(result_origin, expected_origin)
		self.assertEqual(result_dims, expected_dims)

	def test__object_height_from_img_dims__zero_height(self):
		img_dims = (100, 50)
		expected_height = 0
		result_height = object_height_from_img_dims(img_dims)
		self.assertEqual(result_height, expected_height)

	def test__object_height_from_img_dims__cubic(self):
		tile_z = sqrt(50**2 + 25**2)
		img_dims = (100, 50 + tile_z)
		expected_height = 1
		result_height = object_height_from_img_dims(img_dims)
		self.assertEqual(result_height, expected_height)

if __name__ == '__main__':
	unittest.main()
