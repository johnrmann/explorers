import unittest

from src.gui.line_graph import (
	is_2d_series,
	series_x_range,
	series_y_range,
	series_to_screen,
)

class LineGraphTest(unittest.TestCase):
	def test__is_2d_series(self):
		self.assertTrue(is_2d_series([(1, 2), (3, 4)]))
		self.assertFalse(is_2d_series([1, 2, 3]))

	def test__series_x_range__2d(self):
		self.assertEqual(series_x_range([(1, 2), (3, 4)]), (1, 3))

	def test__series_x_range__1d(self):
		self.assertEqual(series_x_range([1, 2, 3]), (0, 2))

	def test__series_y_range__2d(self):
		self.assertEqual(series_y_range([(1, 2), (3, 4)]), (2, 4))

	def test__series_y_range__1d(self):
		self.assertEqual(series_y_range([1, 2, 3]), (1, 3))

	def test__series_to_screen__simple(self):
		self.assertEqual(
			series_to_screen((0, 0), (100, 100), [(1, 2), (3, 4)]),
			[(0.0, 100.0), (100.0, 0.0)]
		)

	def test__series_to_screen__complex(self):
		self.assertEqual(
			series_to_screen((0, 0), (100, 100), [(0, 0), (2, 2), (4, 0)]),
			[(0.0, 100.0), (50.0, 0.0), (100.0, 100.0)]
		)

if __name__ == '__main__':
	unittest.main()
