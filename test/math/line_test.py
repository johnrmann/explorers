import unittest

from src.math.vector2 import vector2_bounding_rect

from src.math.line import (
	is_line_segment_vertical,
	is_line_segment_horizontal,
	extrude_line_segment_y,
	extrude_line_segment_x,
	line_segment_bounding_rect
)

class TestLineFunctions(unittest.TestCase):
	def test__is_line_segment_vertical__true(self):
		self.assertTrue(is_line_segment_vertical(((1, 2), (1, 5))))

	def test__is_line_segment_vertical__false(self):
		self.assertFalse(is_line_segment_vertical(((1, 2), (3, 2))))

	def test__is_line_segment_horizontal__true(self):
		self.assertTrue(is_line_segment_horizontal(((1, 2), (3, 2))))

	def test__is_line_segment_horizontal__false(self):
		self.assertFalse(is_line_segment_horizontal(((1, 2), (1, 5))))

	def test__extrude_line_segment_y__raise_value_error(self):
		with self.assertRaises(ValueError):
			extrude_line_segment_y(((1, 2), (1, 5)), 3)

	def test__extrude_line_segment_y__valid_extrusion(self):
		self.assertEqual(
			extrude_line_segment_y(((1, 2), (3, 2)), 3),
			[(1, 2), (3, 2), (3, 5), (1, 5)]
		)

	def test__extrude_line_segment_x__raise_value_error(self):
		with self.assertRaises(ValueError):
			extrude_line_segment_x(((1, 2), (3, 2)), 3)

	def test__extrude_line_segment_x__valid_extrusion(self):
		self.assertEqual(
			extrude_line_segment_x(((1, 2), (1, 5)), 3),
			[(1, 2), (1, 5), (4, 5), (4, 2)]
		)

	def test__line_segment_bounding_rect__valid_bounding_rect(self):
		linesegs = [((1, 2), (3, 4)), ((-1, -2), (5, 6))]
		self.assertEqual(
			line_segment_bounding_rect(linesegs),
			vector2_bounding_rect([(1, 2), (3, 4), (-1, -2), (5, 6)])
		)

if __name__ == '__main__':
	unittest.main()
